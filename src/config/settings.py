import locale
import os
import platform
from enum import Enum
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from src.core.log import Logger

# Configuração de locale compatível com Windows e Linux
try:
    if platform.system() == "Windows":
        locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
    else:
        # Linux/Unix
        try:
            locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        except locale.Error:
            # Fallback para sistemas que não têm pt_BR
            try:
                locale.setlocale(locale.LC_TIME, "C.UTF-8")
            except locale.Error:
                # Último fallback
                locale.setlocale(locale.LC_TIME, "C")
except locale.Error:
    # Se não conseguir configurar nenhum locale, usa o padrão do sistema
    pass

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    load_dotenv()

Logger.configure_logger()

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ExecutionMode(Enum):
    PRODUCTION = "production"
    DEVELOP = "develop"
    TEST = "test"


class Settings:
    """
    Classe para gerenciar as configurações centrais do projeto sem expor
    endpoints sensíveis diretamente no código.
    """

    PROJECT_NAME = PROJECT_ROOT.name
    VERSION = os.getenv("PROJECT_VERSION", "1.0.0")
    LOG_DIR = str(Path(os.getenv("LOG_PATH", PROJECT_ROOT / "logs")).resolve())

    RECEITANET_APP_PATH = os.getenv(
        "RECEITANET_APP_PATH",
        "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Programas RFB/Receitanet BX/Receitanet BX 1.9.24.lnk"
    )
    RECEITANET_DOCS_DIR = os.getenv(
        "RECEITANET_DOCS_DIR",
        str(Path.home() / "Documents" / "Arquivos ReceitanetBX")
    )
    RECEITANET_ONEDRIVE_DIR = os.getenv(
        "RECEITANET_ONEDRIVE_DIR",
        str(Path.home() / "OneDrive - Alianzo" / "ReceitaNet-Bx")
    )
