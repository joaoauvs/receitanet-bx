import logging
import unicodedata
from pathlib import Path
from typing import Callable, Dict, Optional

from receitanet import ReceitaNetBx
from sped import Sped
from src.core.bot import DesktopBot
from src.modules.common import attempts, get_message, time_execution
from src.modules.data import Data
from src.modules.file import File
from src.modules.log import LogManager
from src.modules.validate import Validar


class Bot(DesktopBot):
    """Orquestra a execução do robô ReceitaNet BX."""

    def __init__(
        self, sistema: str, contribuinte: str, data_inicial: str, data_final: str
    ) -> None:
        """
        Inicializa a instância do robô com os dados recebidos.

        Args:
            sistema (str): Identificador do sistema solicitado.
            contribuinte (str): CNPJ do contribuinte.
            data_inicial (str): Data inicial do período.
            data_final (str): Data final do período.
        """
        super().__init__()
        self.sistema = sistema
        self.contribuinte = contribuinte
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.dir_docs = Path.home() / "Documents" / "Arquivos ReceitanetBX"
        self.sped = Sped(
            contribuinte=self.contribuinte,
            data_inicial=self.data_inicial,
            data_final=self.data_final,
        )
        self.sistemas: Dict[str, Callable[[], None]] = {
            "sped contribuicoes": self.sped.download_sped_contribuicoes,
            "sped contabil": self.sped.download_sped_contabil,
            "sped ecf": self.sped.download_sped_ecf,
            "sped fiscal": self.sped.download_sped_fiscal,
        }

    @staticmethod
    def _normalize_system_name(name: str) -> str:
        """
        Remove acentos e padroniza o nome do sistema para comparação.

        Args:
            name (str): Nome informado na mensagem.

        Returns:
            str: Nome normalizado em minúsculas e sem acentos.
        """
        if not name:
            return ""
        normalized = unicodedata.normalize("NFKD", name)
        ascii_name = normalized.encode("ASCII", "ignore").decode("ASCII")
        return ascii_name.strip().lower()

    @time_execution
    @attempts(max_attempts=3, waiting_time=5)
    def main(self) -> None:
        """Executa o fluxo principal do robô."""
        receitanet = ReceitaNetBx()
        try:
            File.delete_files_and_subdirectories(str(self.dir_docs))
            is_valid = Validar.is_start_date_greater_than_end_date(
                self.data_inicial, self.data_final
            )
            if not is_valid:
                logging.warning(
                    "Período inválido informado: %s > %s",
                    self.data_inicial,
                    self.data_final,
                )
                return
            sistema_key = self._normalize_system_name(self.sistema)
            handler = self.sistemas.get(sistema_key)
            if handler is None:
                logging.warning("Sistema não suportado: %s", self.sistema)
                return
            receitanet.login(contribuinte=self.contribuinte)
            handler()
        finally:
            receitanet.fechar_aplicativo()
            File.delete_files_and_subdirectories(str(self.dir_docs))


if __name__ == "__main__":
    DEVELOP_MODE = False
    try:
        LogManager()

        mensagem = (
            {
                "Cnpj": "44.616.568/0001-07",
                "Sistema": "SPED Contribuicoes",
                "DataInicial": "01/01/2018",
                "DataFinal": "20/07/2024",
            }
            if DEVELOP_MODE
            else get_message()
        )

        logging.info("[MENSAGEM RECEBIDA]: %s", mensagem)

        cnpj_value: Optional[str] = mensagem.get("Cnpj") or mensagem.get("cnpj")
        sistema: Optional[str] = mensagem.get("Sistema") or mensagem.get("sistema")

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
                    "Datas inválidas fornecidas: %s - %s",
                    data_inicial_raw,
                    data_final_raw,
                )
            else:
                if sistema:
                    bot = Bot(
                        sistema=sistema,
                        contribuinte=cnpj,
                        data_inicial=data_inicial,
                        data_final=data_final,
                    )
                    bot.main()
                else:
                    logging.warning("Sistema não fornecido na mensagem.")
        else:
            logging.warning("CNPJ inválido fornecido")
    except Exception as e:
        logging.error(
            "[FALHA AO INICIAR O ROBO]: %s - %s",
            type(e).__name__,
            str(e),
        )
