import json
import logging
import re
from datetime import datetime, timedelta


class Data():
    def formatar_data(data):
        try:
            if re.search(r'\d{2}/\d{2}/\d{4}', data):
                data = datetime.strptime(data, '%d/%m/%Y')
                data = data.strftime('%d/%m/%Y')
            elif re.search(r'\d{2}-\d{2}-\d{4}', data):
                data = datetime.strptime(data, '%d-%m-%Y')
                data = data.strftime('%d/%m/%Y')
            elif re.search(r'\d{4}-\d{2}-\d{2}', data):
                data = datetime.strptime(data, '%Y-%m-%d')
                data = data.strftime('%d/%m/%Y')
            elif re.search(r'\d{4}/\d{2}/\d{2}', data):
                data = datetime.strptime(data, '%Y/%m/%d')
                data = data.strftime('%d/%m/%Y')
            else:
                return False
            return data
        except Exception as e:
            raise logging.error(f'Erro ao formatar a data: {e}')

    def primeiro_ultimo_dia_mes_anterior():
        try:
            today = datetime.today()
            first = today.replace(day=1) - timedelta(days=1)
            lastMonth = first.month
            lastYear = first.year
            primeiro_dia = first.strftime('01/%m/%Y')
            ultimo_dia = first.strftime('%d/%m/%Y')
            return primeiro_dia, ultimo_dia
        except Exception as e:
            raise logging.error(f'Erro ao pegar o primeiro e o ultimo dia do mes anterior: {e}')

    def primeiro_ultimo_dia_ano_anterior():
        try:
            today = datetime.today()
            first = today.replace(day=1) - timedelta(days=1)
            lastMonth = first.month
            lastYear = first.year - 1
            primeiro_dia = first.strftime(f'01/01/{lastYear}')
            ultimo_dia = first.strftime(f'31/12/{lastYear}')
            return primeiro_dia, ultimo_dia
        except Exception as e:
            raise logging.error(f'Erro ao pegar o primeiro e o ultimo dia do ano anterior: {e}')