import calendar
import re
from datetime import datetime


class Converter:
    """Conversoes utilitarias para datas em diferentes formatos."""

    @staticmethod
    def format_date(valor: str):
        """
        Converte uma data para o formato DD/MM/AAAA.

        Args:
            valor (str): Data informada.

        Returns:
            str | bool: Data convertida ou False quando o formato e desconhecido.
        """
        try:
            if re.search(r"\d{2}/\d{2}/\d{4}", valor):
                data = datetime.strptime(valor, "%d/%m/%Y")
            elif re.search(r"\d{2}-\d{2}-\d{4}", valor):
                data = datetime.strptime(valor, "%d-%m-%Y")
            elif re.search(r"\d{4}-\d{2}-\d{2}", valor):
                data = datetime.strptime(valor, "%Y-%m-%d")
            elif re.search(r"\d{4}/\d{2}/\d{2}", valor):
                data = datetime.strptime(valor, "%Y/%m/%d")
            else:
                return False
            return data.strftime("%d/%m/%Y")
        except Exception as exc:
            raise ValueError(f"Erro ao converter a data: {exc}") from exc

    @staticmethod
    def convert_date_to_string_first_day_of_month(valor: str) -> str:
        """
        Converte um texto no formato Abreviacao/Ano para o primeiro dia do mes.

        Args:
            valor (str): Texto como `Jan/2024`.

        Returns:
            str: Data no formato DD/MM/AAAA.
        """
        data = datetime.strptime(valor.lower(), "%b/%Y")
        return data.strftime("01/%m/%Y")

    @staticmethod
    def convert_date_to_string_last_day_of_month(valor: str) -> str:
        """
        Converte um texto no formato Abreviacao/Ano para o ultimo dia do mes.

        Args:
            valor (str): Texto como `Jan/2024`.

        Returns:
            str: Data no formato DD/MM/AAAA contendo o ultimo dia do mes.
        """
        data = datetime.strptime(valor.lower(), "%b/%Y")
        ultimo_dia = calendar.monthrange(data.year, data.month)[1]
        return data.replace(day=ultimo_dia).strftime("%d/%m/%Y")

    @staticmethod
    def convert_date_to_year_month(valor: str):
        """
        Retorna o ano e o nome completo do mes a partir de uma string abreviada.

        Args:
            valor (str): Texto como `Jan/2024`.

        Returns:
            tuple[int, str]: Ano e nome do mes.
        """
        data = datetime.strptime(valor.lower(), "%b/%Y")
        meses = [
            "Janeiro",
            "Fevereiro",
            "Marco",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]
        return data.year, meses[data.month - 1]

    @staticmethod
    def convert_month(valor: str) -> str:
        """
        Converte uma abreviacao de mes para o nome completo.

        Args:
            valor (str): Texto como `Jan/2024`.

        Returns:
            str: Nome do mes seguido do ano (ex.: `Janeiro/2024`).
        """
        meses = {
            "Jan": "Janeiro",
            "Fev": "Fevereiro",
            "Mar": "Marco",
            "Abr": "Abril",
            "Mai": "Maio",
            "Jun": "Junho",
            "Jul": "Julho",
            "Ago": "Agosto",
            "Set": "Setembro",
            "Out": "Outubro",
            "Nov": "Novembro",
            "Dez": "Dezembro",
        }
        mes, ano = valor.split("/")
        return f"{meses[mes]}/{ano}"
