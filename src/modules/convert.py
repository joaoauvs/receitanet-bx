import calendar
import json
import re
from datetime import datetime, timedelta


class Converter:

    @staticmethod
    def format_date(date):
        try:
            if re.search(r'\d{2}/\d{2}/\d{4}', date):
                date = datetime.strptime(date, '%d/%m/%Y')
                date = date.strftime('%d/%m/%Y')
            elif re.search(r'\d{2}-\d{2}-\d{4}', date):
                date = datetime.strptime(date, '%d-%m-%Y')
                date = date.strftime('%d/%m/%Y')
            elif re.search(r'\d{4}-\d{2}-\d{2}', date):
                date = datetime.strptime(date, '%Y-%m-%d')
                date = date.strftime('%d/%m/%Y')
            elif re.search(r'\d{4}/\d{2}/\d{2}', date):
                date = datetime.strptime(date, '%Y/%m/%d')
                date = date.strftime('%d/%m/%Y')
            else:
                return False
            return date
        except Exception as e:
            raise Exception(f'Error formatting the date: {e}')

    @staticmethod
    def convert_date_to_string_first_day_of_month(date):
        date = date.lower()
        date_object = datetime.strptime(date, '%b/%Y')
        return date_object.strftime("01/%m/%Y")

    @staticmethod
    def convert_date_to_string_last_day_of_month(date):
        date = date.lower()
        date_object = datetime.strptime(date, '%b/%Y')
        last_day = calendar.monthrange(date_object.year, date_object.month)[1]
        return date_object.strftime(f"{last_day}/%m/%Y")
    
    @staticmethod
    def convert_date_to_year_month(date):
        date = date.lower()
        date_object = datetime.strptime(date, '%b/%Y')
        months = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        return date_object.year, months[date_object.month - 1]

    @staticmethod
    def convert_month(date):
        months = {
            'Jan': 'Janeiro',
            'Fev': 'Fevereiro',
            'Mar': 'Março',
            'Abr': 'Abril',
            'Mai': 'Maio',
            'Jun': 'Junho',
            'Jul': 'Julho',
            'Ago': 'Agosto',
            'Set': 'Setembro',
            'Out': 'Outubro',
            'Nov': 'Novembro',
            'Dez': 'Dezembro'
        }
        month, year = date.split("/")
        return f"{months[month]}/{year}"