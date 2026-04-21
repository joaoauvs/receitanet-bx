import logging
import unicodedata
from pathlib import Path
from typing import Callable, Dict, Optional

from receitanet import ReceitaNetBx
from sped import Sped
from src.modules.common import attempts, get_message, time_execution
from src.modules.data import Data
from src.modules.exceptions import SpedError, ValidationError
from src.modules.file import File
from src.modules.log import LogManager
from src.modules.types import SpedType
from src.modules.validate import Validar


class Bot:
    """Orquestra a execução do robô ReceitaNet BX."""

    def __init__(
        self, sistema: str, contribuinte: str, data_inicial: str, data_final: str
    ) -> None:
        """
        Inicializa o orquestrador com os dados da solicitação.

        Args:
            sistema (str): Identificador do sistema solicitado.
            contribuinte (str): CNPJ do contribuinte.
            data_inicial (str): Data inicial do período (DD/MM/AAAA).
            data_final (str): Data final do período (DD/MM/AAAA).
        """
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
        self._handlers: Dict[SpedType, Callable[[], None]] = {
            SpedType.CONTRIBUICOES: self.sped.download_sped_contribuicoes,
            SpedType.CONTABIL: self.sped.download_sped_contabil,
            SpedType.ECF: self.sped.download_sped_ecf,
            SpedType.FISCAL: self.sped.download_sped_fiscal,
        }

    @staticmethod
    def _normalize_system_name(name: str) -> str:
        """
        Remove acentos e padroniza o nome do sistema para comparação com SpedType.

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

    def _resolve_sped_type(self, sistema_key: str) -> SpedType:
        """
        Converte a chave normalizada no SpedType correspondente.

        Args:
            sistema_key (str): Nome do sistema normalizado.

        Returns:
            SpedType: Enum correspondente.

        Raises:
            ValidationError: Quando o sistema não é suportado.
        """
        try:
            return SpedType(sistema_key)
        except ValueError:
            raise ValidationError(f"Sistema não suportado: '{sistema_key}'")

    @time_execution
    @attempts(max_attempts=3, waiting_time=5)
    def main(self) -> None:
        """Executa o fluxo principal do robô."""
        receitanet = ReceitaNetBx()
        try:
            File.delete_files_and_subdirectories(str(self.dir_docs))

            if not Validar.is_start_date_greater_than_end_date(
                self.data_inicial, self.data_final
            ):
                logging.warning(
                    "Período inválido informado: %s > %s",
                    self.data_inicial,
                    self.data_final,
                )
                return

            sistema_key = self._normalize_system_name(self.sistema)
            sped_type = self._resolve_sped_type(sistema_key)
            handler = self._handlers[sped_type]

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
            data_inicial_raw = mensagem.get("DataInicial") or mensagem.get("datainicial")
            data_final_raw = mensagem.get("DataFinal") or mensagem.get("datafinal")
            data_inicial = Data.formatar_data(data_inicial_raw)
            data_final = Data.formatar_data(data_final_raw)

            if not data_inicial or not data_final:
                logging.warning(
                    "Datas inválidas fornecidas: %s - %s",
                    data_inicial_raw,
                    data_final_raw,
                )
            elif not sistema:
                logging.warning("Sistema não fornecido na mensagem.")
            else:
                bot = Bot(
                    sistema=sistema,
                    contribuinte=cnpj,
                    data_inicial=data_inicial,
                    data_final=data_final,
                )
                bot.main()
        else:
            logging.warning("CNPJ inválido fornecido")
    except SpedError as e:
        logging.error("[FALHA NO ROBÔ]: %s - %s", type(e).__name__, str(e))
    except Exception as e:
        logging.error(
            "[FALHA AO INICIAR O ROBO]: %s - %s",
            type(e).__name__,
            str(e),
        )
