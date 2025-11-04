import logging
import re
from datetime import datetime
from typing import Union


class Validar:
    """Funcoes auxiliares para validar campos recebidos do payload."""

    @staticmethod
    def validar_dicionario(mensagem: dict) -> bool:
        """
        Valida se todos os campos do dicionario possuem valores.

        Args:
            mensagem (dict): Dados recebidos.

        Returns:
            bool: True quando todos os campos estao preenchidos.
        """
        return all(mensagem.values())

    @staticmethod
    def retornar_campos_vazios(mensagem: dict):
        """
        Lista os campos vazios do dicionario informado.

        Args:
            mensagem (dict): Dados recebidos.

        Returns:
            list[str]: Campos sem valor.
        """
        return [chave for chave, valor in mensagem.items() if not valor]

    def _generate_first_digit(self, doc: Union[str, list]) -> str:
        """Calcula o primeiro digito verificador do CNPJ."""
        soma = 0
        for idx in range(12):
            soma += int(doc[idx]) * self.weights_first[idx]

        soma %= 11
        return "0" if soma < 2 else str(11 - soma)

    def _generate_second_digit(self, doc: Union[str, list]) -> str:
        """Calcula o segundo digito verificador do CNPJ."""
        soma = 0
        for idx in range(13):
            soma += int(doc[idx]) * self.weights_second[idx]

        soma %= 11
        return "0" if soma < 2 else str(11 - soma)

    @staticmethod
    def validar_cnpj(cnpj: str) -> Union[bool, str]:
        """
        Valida e sanitiza um numero de CNPJ.

        Args:
            cnpj (str): Numero de CNPJ com ou sem formatacao.

        Returns:
            Union[bool, str]: CNPJ somente com digitos ou False quando invalido.
        """

        def _generate_first_digit(doc: str) -> str:
            pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            soma = sum(int(doc[idx]) * pesos[idx] for idx in range(12))
            soma %= 11
            return "0" if soma < 2 else str(11 - soma)

        def _generate_second_digit(doc: str) -> str:
            pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            soma = sum(int(doc[idx]) * pesos[idx] for idx in range(13))
            soma %= 11
            return "0" if soma < 2 else str(11 - soma)

        cnpj_limpo = re.sub(r"[^0-9]", "", cnpj or "")

        if len(cnpj_limpo) != 14:
            return False

        if any(cnpj_limpo.count(str(i)) == 14 for i in range(10)):
            return False

        if _generate_first_digit(cnpj_limpo) == cnpj_limpo[12] and _generate_second_digit(cnpj_limpo) == cnpj_limpo[13]:
            return cnpj_limpo
        return False

    @staticmethod
    def is_start_date_greater_than_end_date(start_date: str, end_date: str) -> bool:
        """
        Verifica se a data inicial e anterior ou igual a data final.

        Args:
            start_date (str): Data inicial no formato DD/MM/AAAA.
            end_date (str): Data final no formato DD/MM/AAAA.

        Returns:
            bool: True quando a ordem informada e valida; False caso contrario.
        """
        try:
            data_inicial = datetime.strptime(start_date, "%d/%m/%Y")
            data_final = datetime.strptime(end_date, "%d/%m/%Y")
            return data_inicial <= data_final
        except Exception as exc:
            logging.error("Erro ao comparar datas: %s", exc)
            return False
