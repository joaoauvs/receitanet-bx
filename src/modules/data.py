import logging
import re
from datetime import datetime, timedelta


class Data:
    """Utilitarios para manipulacao e formatacao de datas."""

    @staticmethod
    def formatar_data(valor: str):
        """
        Normaliza datas para o formato DD/MM/AAAA.

        Args:
            valor (str): Data informada no payload.

        Returns:
            str | bool: Data formatada ou False quando o formato nao e reconhecido.
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
        except Exception as e:
            logging.error("Erro ao formatar a data: %s", e)
            raise

    @staticmethod
    def primeiro_ultimo_dia_mes_anterior():
        """
        Calcula o primeiro e o ultimo dia do mes anterior ao atual.

        Returns:
            tuple[str, str]: Primeiro e ultimo dia no formato DD/MM/AAAA.
        """
        try:
            hoje = datetime.today()
            ultimo_dia_mes_anterior = hoje.replace(day=1) - timedelta(days=1)
            primeiro_dia = ultimo_dia_mes_anterior.replace(day=1).strftime("%d/%m/%Y")
            ultimo_dia = ultimo_dia_mes_anterior.strftime("%d/%m/%Y")
            return primeiro_dia, ultimo_dia
        except Exception as e:
            logging.error("Erro ao calcular os dias do mes anterior: %s", e)
            raise

    @staticmethod
    def primeiro_ultimo_dia_ano_anterior():
        """
        Calcula o primeiro e o ultimo dia do ano anterior ao atual.

        Returns:
            tuple[str, str]: Primeiro e ultimo dia no formato DD/MM/AAAA.
        """
        try:
            ano_anterior = datetime.today().year - 1
            primeiro_dia = f"01/01/{ano_anterior}"
            ultimo_dia = f"31/12/{ano_anterior}"
            return primeiro_dia, ultimo_dia
        except Exception as e:
            logging.error("Erro ao calcular os dias do ano anterior: %s", e)
            raise
