import logging
import os
import shutil
from datetime import datetime


class File:
    """Classe responsável por operações relacionadas a arquivos."""

    @staticmethod
    def _create_directory_if_not_exists(directory):
        """
        Cria um diretório se ele não existir.

        Args:
            directory (str): Caminho do diretório a ser criado.
        """
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def move_file(source_path, destination_path):
        """
        Move um arquivo de um caminho de origem para um caminho de destino.

        Args:
        - source_path (str): Caminho completo do arquivo de origem.
        - destination_path (str): Caminho onde o arquivo deve ser movido.

        Returns:
        None
        """
        if os.path.exists(destination_path) and os.path.isfile(destination_path):
            os.remove(destination_path)

        shutil.move(source_path, destination_path)

    @staticmethod
    def move_files_by_extension(source_path, destination_path, extension):
        """
        Move arquivos com uma extensão específica de origem para destino.

        Args:
            source_path (str): Caminho do diretório de origem.
            destination_path (str): Caminho do diretório de destino.
            extension (str): Extensão dos arquivos a serem movidos (ex: ".pdf").
        """
        try:
            logging.info("Movendo arquivos!")
            File._create_directory_if_not_exists(destination_path)

            for file in os.listdir(source_path):
                if file.upper().endswith(extension.upper()):
                    source_file = os.path.join(source_path, file)
                    shutil.move(source_file, destination_path)
        except Exception as e:
            raise logging.warning(f"Erro: {e}")

    @staticmethod
    async def clear_folder(source_path):
        """
        Deleta todos os arquivos e diretórios dentro do diretório.

        Args:
            source_path (str): Caminho do diretório a ser limpo.
        """
        try:
            logging.info("Deletando arquivos!")
            File._create_directory_if_not_exists(source_path)

            with os.scandir(source_path) as entries:
                for entry in entries:
                    if entry.is_file():
                        os.remove(entry.path)
                    elif entry.is_dir():
                        os.rmdir(entry.path)
        except Exception as e:
            raise Exception(f"Erro ao deletar arquivos: {e}")

    @staticmethod
    def delete_files_extension(directory, extension):
        """
        Deleta arquivos com uma extensão específica no diretório.

        Args:
            directory (str): Caminho do diretório onde os arquivos serão deletados.
            extension (str): Extensão dos arquivos a serem deletados (ex: ".pdf").
        """
        for filename in os.listdir(directory):
            if filename.lower().endswith(extension):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)

    @staticmethod
    def delete_file(filename):
        """
        Deleta um arquivo especificado.

        Args:
            filename (str): Caminho do arquivo a ser deletado.

        Raises:
            OSError: Se ocorrer um erro ao deletar o arquivo.
        """
        try:
            os.remove(filename)
        except OSError as error:
            raise OSError(f"Erro ao deletar o arquivo {filename}: {error}")

    @staticmethod
    def delete_files_directory(directory):
        """
        Deleta arquivos no diretório, mas mantém o diretório.

        Args:
            directory (str): Caminho do diretório.
        """
        logging.debug(f"Cleaning the directory {directory}")
        File._create_directory_if_not_exists(directory)
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)

    @staticmethod
    def delete_files_and_directory(directory):
        """
        Deleta arquivos e o próprio diretório.

        Args:
            directory (str): Caminho do diretório.
        """
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(directory)

    def delete_files_and_subdirectories(directory):
        """
        Deleta arquivos e subpastas, mas não o diretório raiz.

        Args:
            directory (str): Caminho do diretório.
        """
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    @staticmethod
    def check_files_exist(destination_path, prefix):
        """
        Verifica se existem arquivos com um prefixo no diretório.

        Args:
            destination_path (str): Caminho do diretório.
            prefix (str): Prefixo dos arquivos a serem verificados.

        Returns:
            bool: True se existir arquivo com o prefixo, False caso contrário.
        """
        files = [
            f
            for f in os.listdir(destination_path)
            if os.path.isfile(os.path.join(destination_path, f))
        ]
        return any(file.lower().startswith(prefix.lower()) for file in files)

    @staticmethod
    def get_files_directory(directory):
        """
        Retorna todos os arquivos de um diretório.

        Args:
            directory (str): Caminho do diretório.

        Returns:
            list: Lista com nomes dos arquivos no diretório.
        """
        logging.debug(f"Listing files in directory {directory}")
        return [
            arquivo
            for arquivo in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, arquivo))
        ]

    @staticmethod
    def move_file_to_backup(
        file: str, dir_backup: str, name_file: str = "Arquivo_Original"
    ) -> None:
        """
        Move o arquivo para a pasta de backup.

        Args:
            file (str): Caminho completo do arquivo.
            dir_backup (str): Caminho da pasta de backup.
            name_file (str, optional): Prefixo do arquivo. Padrão: Original.
        """
        logging.debug(f"Moving file {file} to backup folder")
        File._create_directory_if_not_exists(dir_backup)
        file_extension = os.path.splitext(file)[1]
        base_name = os.path.splitext(os.path.basename(file))[0]
        date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_name_destin = f"{name_file}_{base_name}_{date_time}{file_extension}"
        shutil.move(file, os.path.join(dir_backup, file_name_destin))
