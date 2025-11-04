import logging
from os import path

from receitanet import ReceitaNetBx
from resources.core import DesktopBot
from resources.modules.common import attempts, get_message, time_execution
from resources.modules.data import Data
from resources.modules.file import File
from src.modules.log import LogManager
from resources.modules.validate import Validar
from sped import Sped


class Bot(DesktopBot):
    """
    Classe responsável por gerenciar o funcionamento do bot para o ReceitaNetBX.
    """

    def __init__(self, sistema, contribuinte, data_inicial, data_final) -> None:
        """
        Construtor da classe Bot.

        Args:
            sistema (str): Nome do sistema para processamento.
            contribuinte (str): CNPJ do contribuinte.
            data_inicial (str): Data inicial do período.
            data_final (str): Data final do período.
        """
        super().__init__()
        self.sistema = sistema
        self.contribuinte = contribuinte
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.dir_docs = path.expanduser("~") + "/Documents/Arquivos ReceitanetBX"
        self.sped = Sped(contribuinte=self.contribuinte, data_inicial=self.data_inicial, data_final=self.data_final)
        self.sistemas = {"SPED Contribuições": self.sped.download_sped_contribuicoes, "SPED Contábil": self.sped.download_sped_contabil, "SPED ECF": self.sped.download_sped_ecf, "SPED Fiscal": self.sped.download_sped_fiscal}

    @time_execution
    @attempts(max_attempts=3, waiting_time=5)
    def main(self):
        """Método principal que realiza o processamento."""
        receitanet = ReceitaNetBx()
        try:
            File.delete_files_and_subdirectories(self.dir_docs)
            if not Validar.is_start_date_greater_than_end_date(data_inicial, data_final):
                return
            if self.sistema not in self.sistemas:
                return
            receitanet.login(contribuinte=self.contribuinte)
            self.sistemas[self.sistema]()
            return
        finally:
            receitanet.fechar_aplicativo()
            File.delete_files_and_subdirectories(self.dir_docs)


if __name__ == "__main__":
    DEVELOP_MODE = False
    try:
        LogManager()

        mensagem = {"Cnpj": "44.616.568/0001-07", "Sistema": "SPED Contribuições", "DataInicial": "01/01/2018", "DataFinal": "20/07/2024"} if DEVELOP_MODE else get_message()

        logging.info(f"[MENSAGEM RECEBIDA]: {mensagem}")

        cnpj_value = mensagem.get("Cnpj") or mensagem.get("cnpj")
        sistema = mensagem.get("Sistema") or mensagem.get("sistema")

        if cnpj := Validar.validar_cnpj(cnpj_value):
            data_inicial = mensagem.get("DataInicial") if mensagem.get("DataInicial") is not None else mensagem.get("datainicial")
            data_final = mensagem.get("DataFinal") if mensagem.get("DataFinal") is not None else mensagem.get("datafinal")
            data_inicial = Data.formatar_data(data_inicial)
            data_final = Data.formatar_data(data_final)
            Bot(sistema=sistema, contribuinte=cnpj, data_inicial=data_inicial, data_final=data_final).main()
        else:
            logging.warning("CNPJ inválido fornecido")
    except Exception as e:
        logging.error(f"[FALHA AO INICIAR O BOT]: {type(e).__name__} - {str(e)}")
