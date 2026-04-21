"""Hierarquia de exceções do domínio ReceitaNet BX."""


class SpedError(Exception):
    """Exceção base para erros do robô ReceitaNet BX."""


class LoginError(SpedError):
    """Falha no processo de login com certificado digital."""


class DownloadError(SpedError):
    """Falha durante o processo de download de arquivo SPED."""


class ValidationError(SpedError):
    """Dados de entrada inválidos (CNPJ, datas, sistema)."""


class UIError(SpedError):
    """Elemento de interface não encontrado ou interação falhou."""
