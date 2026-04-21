"""Tipos e constantes do domínio ReceitaNet BX."""

from enum import Enum


class SpedType(str, Enum):
    """Tipos de SPED suportados.

    O valor do enum é a chave normalizada usada no lookup (minúsculas, sem acento).
    Use `.label` para o nome de exibição e caminhos de arquivo.
    """

    FISCAL = "sped fiscal"
    CONTRIBUICOES = "sped contribuicoes"
    CONTABIL = "sped contabil"
    ECF = "sped ecf"

    @property
    def label(self) -> str:
        """Nome de exibição usado em logs e como identificador de tipo de arquivo."""
        _labels: dict[str, str] = {
            "sped fiscal": "SPED Fiscal",
            "sped contribuicoes": "SPED Contribuicoes",
            "sped contabil": "SPED Contabil",
            "sped ecf": "SPED ECF",
        }
        return _labels[self.value]
