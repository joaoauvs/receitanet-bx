import json
import logging
import re
from datetime import datetime, timedelta
from typing import Union


class Validar:
    @staticmethod
    def validar_dicionario(mensagem):
        """
        Valida se todos os campos do dicionário possuem valores.

        Args:
            mensagem (dict): Dicionário a ser validado.

        Returns:
            bool: Retorna True se todos os campos têm valores e False caso contrário.
        """
        for key, value in mensagem.items():
            if not value:
                return False
        return True

    @staticmethod
    def retornar_campos_vazios(mensagem):
        """
        Retorna uma lista de campos do dicionário que estão vazios.

        Args:
            mensagem (dict): Dicionário a ser verificado.

        Returns:
            list: Lista contendo os campos vazios.
        """
        return [key for key, value in mensagem.items() if not value]

    def _generate_first_digit(self, doc: Union[str, list]) -> str:
        """Gerar o primeiro dígito verificador do CNPJ."""
        sum = 0

        for i in range(12):
            sum += int(doc[i]) * self.weights_first[i]

        sum = sum % 11

        if sum < 2:
            sum = 0
        else:
            sum = 11 - sum

        return str(sum)
    
    def _generate_second_digit(self, doc: Union[str, list]) -> str:
        """Gerar o segundo dígito verificador do CNPJ."""
        sum = 0

        for i in range(13):
            sum += int(doc[i]) * self.weights_second[i]

        sum = sum % 11

        if sum < 2:
            sum = 0
        else:
            sum = 11 - sum

        return str(sum)

    @staticmethod
    def validar_cnpj(cnpj: str) -> Union[bool, str]:
        def _generate_first_digit(doc: str) -> str:
            """Gerar o primeiro dígito verificador do CNPJ."""
            weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            sum = 0

            for i in range(12):
                sum += int(doc[i]) * weights_first[i]

            sum = sum % 11

            if sum < 2:
                sum = 0
            else:
                sum = 11 - sum

            return str(sum)

        def _generate_second_digit(doc: str) -> str:
            """Gerar o segundo dígito verificador do CNPJ."""
            weights_second = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            sum = 0

            for i in range(13):
                sum += int(doc[i]) * weights_second[i]

            sum = sum % 11

            if sum < 2:
                sum = 0
            else:
                sum = 11 - sum

            return str(sum)

        cnpj = re.sub(r'[^0-9]', '', cnpj)

        if len(cnpj) != 14:
            return False

        for i in range(10):
            if cnpj.count("{}".format(i)) == 14:
                return False

        if _generate_first_digit(cnpj) == cnpj[12] and _generate_second_digit(cnpj) == cnpj[13]:
            return cnpj
        else:
            return False

        


    @staticmethod
    def is_start_date_greater_than_end_date(start_date, end_date):
        try:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            return start_date <= end_date
        except Exception as e:
            raise logging.error(f'Error checking if start date is greater than end date: {e}')