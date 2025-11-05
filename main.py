import logging
import unicodedata
from os import path

from receitanet import ReceitaNetBx
from src.core.bot import DesktopBot
from src.modules.common import attempts, get_message, time_execution
from src.modules.data import Data
from src.modules.file import File
from src.modules.log import LogManager
from src.modules.validate import Validar
from sped import Sped


class Bot(DesktopBot):
    """Orquestra a execucao do robo ReceitaNet BX."""

    def __init__(self, sistema, contribuinte, data_inicial, data_final) -> None:
        """
        Inicializa a instancia do robo com os dados recebidos.

        Args:
            sistema (str): Identificador do sistema solicitado.
            contribuinte (str): CNPJ do contribuinte.
            data_inicial (str): Data inicial do periodo.
            data_final (str): Data final do periodo.
        """
        super().__init__()
        self.sistema = sistema
        self.contribuinte = contribuinte
        self.data_inicial = data_inicial
        self.data_final = data_final
        home = path.expanduser("~")
        self.dir_docs = f"{home}/Documents/Arquivos ReceitanetBX"
        self.sped = Sped(
            contribuinte=self.contribuinte,
            data_inicial=self.data_inicial,
            data_final=self.data_final
        )
        self.sistemas = {
            "sped contribuicoes": self.sped.download_sped_contribuicoes,
            "sped contabil": self.sped.download_sped_contabil,
            "sped ecf": self.sped.download_sped_ecf,
            "sped fiscal": self.sped.download_sped_fiscal,
        }

    @staticmethod
    def _normalize_system_name(name: str) -> str:
        """
        Remove acentos e padroniza o nome do sistema para comparacao.

        Args:
            name (str): Nome informado na mensagem.

        Returns:
            str: Nome normalizado em minusculas sem acentuacao.
        """
        if not name:
            return ""
        normalized = unicodedata.normalize("NFKD", name)
        ascii_name = normalized.encode("ASCII", "ignore").decode("ASCII")
        return ascii_name.strip().lower()

    @time_execution
    @attempts(max_attempts=3, waiting_time=5)
    def main(self) -> None:
        """Executa o fluxo principal do robo."""
        receitanet = ReceitaNetBx()
        try:
            File.delete_files_and_subdirectories(self.dir_docs)
            is_valid = Validar.is_start_date_greater_than_end_date(
                self.data_inicial, self.data_final
            )
            if not is_valid:
                logging.warning(
                    "Periodo informado invalido: %s > %s",
                    self.data_inicial,
                    self.data_final
                )
                return
            sistema_key = self._normalize_system_name(self.sistema)
            handler = self.sistemas.get(sistema_key)
            if handler is None:
                logging.warning("Sistema nao suportado: %s", self.sistema)
                return
            receitanet.login(contribuinte=self.contribuinte)
            handler()
        finally:
            receitanet.fechar_aplicativo()
            File.delete_files_and_subdirectories(self.dir_docs)


if __name__ == "__main__":
    DEVELOP_MODE = False
    try:
        LogManager()

        mensagem = {
            "Cnpj": "44.616.568/0001-07",
            "Sistema": "SPED Contribuicoes",
            "DataInicial": "01/01/2018",
            "DataFinal": "20/07/2024",
        } if DEVELOP_MODE else get_message()

        logging.info("[MENSAGEM RECEBIDA]: %s", mensagem)

        cnpj_value = mensagem.get("Cnpj") or mensagem.get("cnpj")
        sistema = mensagem.get("Sistema") or mensagem.get("sistema")

        if cnpj := Validar.validar_cnpj(cnpj_value):
            data_inicial_raw = (
                mensagem.get("DataInicial")
                if mensagem.get("DataInicial") is not None
                else mensagem.get("datainicial")
            )
            data_final_raw = (
                mensagem.get("DataFinal")
                if mensagem.get("DataFinal") is not None
                else mensagem.get("datafinal")
            )
            data_inicial = Data.formatar_data(data_inicial_raw)
            data_final = Data.formatar_data(data_final_raw)

            if not data_inicial or not data_final:
                logging.warning(
                    "Datas invalidas fornecidas: %s - %s",
                    data_inicial_raw,
                    data_final_raw
                )
            else:
                bot = Bot(
                    sistema=sistema,
                    contribuinte=cnpj,
                    data_inicial=data_inicial,
                    data_final=data_final
                )
                bot.main()
        else:
            logging.warning("CNPJ invalido fornecido")
    except Exception as e:
        logging.error(
            "[FALHA AO INICIAR O BOT]: %s - %s",
            type(e).__name__,
            str(e)
        )
