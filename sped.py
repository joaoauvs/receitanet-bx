import logging
import time
from pathlib import Path
from typing import Optional

from receitanet import ReceitaNetBx
from src.core.bot import DesktopBot
from src.modules.exceptions import DownloadError
from src.modules.types import SpedType


class Sped(DesktopBot):
    """Rotinas de download para os diferentes tipos de arquivos SPED."""

    def __init__(self, contribuinte: str, data_inicial: str, data_final: str) -> None:
        """
        Inicializa o fluxo com os dados do contribuinte.

        Args:
            contribuinte (str): CNPJ utilizado na consulta.
            data_inicial (str): Data inicial do período.
            data_final (str): Data final do período.
        """
        super().__init__()
        self.contribuinte = contribuinte
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.receitanet = ReceitaNetBx()
        
        base_dir = Path(__file__).resolve().parent
        images_dir = base_dir / "src" / "images"
        self.dir_baixa = images_dir / "baixa"
        self.dir_selector_box = images_dir / "seletor-box"
        
        self.add_image(
            "button-criterios-acima",
            str(self.dir_baixa / "button-criterios-acima.png")
        )
        self.add_image(
            "button-pesquisar",
            str(self.dir_baixa / "button-pesquisar.png")
        )
        btn_solicitar = self.dir_baixa / "button-solicitar-arquivos-marcados.png"
        self.add_image("button-solicitar-arquivos-marcados", str(btn_solicitar))
        resultado_pesquisa = self.dir_baixa / "resultado-pesquisa.png"
        self.add_image("resultado-pesquisa", str(resultado_pesquisa))

    def wait_for_element(
        self, element: str, timeout: int = 30, matching: float = 0.97
    ) -> bool:
        """
        Aguarda um elemento aparecer na tela dentro de um tempo limite.

        Args:
            element (str): Identificador do elemento.
            timeout (int): Tempo máximo de espera em segundos.
            matching (float): Precisão mínima de correspondência.

        Returns:
            bool: True se o elemento for encontrado dentro do tempo limite.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.find(element, matching=matching):
                return True
            time.sleep(0.5)
        return False

    def _solicitar_arquivos_criterios_acima(self, tipo: str) -> None:
        """
        Solicita arquivos aplicando os critérios definidos acima.

        Args:
            tipo (str): Tipo de arquivo SPED a ser baixado.
        """
        msg = "Clicando botão Solicitar Arquivos critérios acima"
        logging.info(msg)
        self.find_click_image(identifier="button-criterios-acima", match=0.97)
        if self.receitanet.validar_solicitacao():
            self.receitanet.baixar_arquivos()
            self.receitanet.manipular_arquivos(tipo, self.contribuinte)

    def _pesquisar_e_solicitar_arquivos(self, tipo: str) -> None:
        """
        Pesquisa e solicita o download dos arquivos encontrados.

        Args:
            tipo (str): Tipo de arquivo SPED a ser baixado.
        """
        logging.info("Selecionando o botão -> PESQUISAR <-")
        self.click_image("button-pesquisar")
        if self.wait_for_element("resultado-pesquisa"):
            logging.info("Arquivo encontrado")
            self.find_click_list_image(path=str(self.dir_selector_box))
            has_btn = self.wait_for_element(
                "button-solicitar-arquivos-marcados"
            )
            if has_btn:
                msg = "Selecionando botão -> SOLICITAR ARQUIVOS MARCADOS <-"
                logging.info(msg)
                self.click_image("button-solicitar-arquivos-marcados")
                if self.receitanet.validar_solicitacao():
                    self.receitanet.baixar_arquivos()
                    self.receitanet.manipular_arquivos(tipo, self.contribuinte)
        else:
            logging.info("Nenhum arquivo para baixar")
            self.receitanet.validar_solicitacao()

    def _processar_outros_speds(self, sped_type: SpedType) -> None:
        """
        Processa o download de arquivos SPED que não são fiscais.

        Args:
            sped_type (SpedType): Tipo de arquivo SPED.
        """
        tipo = sped_type.label
        self.receitanet.input_data(self.data_inicial, self.data_final)

        if sped_type in (SpedType.ECF, SpedType.CONTRIBUICOES):
            self._solicitar_arquivos_criterios_acima(tipo)

        if sped_type is SpedType.CONTABIL:
            self._pesquisar_e_solicitar_arquivos(tipo)

    def _finalizar_processo(self, tipo: str) -> None:
        """
        Finaliza o processo de download verificando os resultados.

        Args:
            tipo (str): Label do tipo de arquivo SPED sendo processado.
        """
        try:
            if self.find("resultado-pesquisa", matching=0.9):
                logging.info("Arquivo encontrado")
                time.sleep(5)
                logging.info("Validando se existe o marcador no seletor")
                self.find_click_list_image(path=str(self.dir_selector_box))
                time.sleep(10)
                logging.info("Selecionando botão -> SOLICITAR ARQUIVOS MARCADOS <-")
                self.click_image("button-solicitar-arquivos-marcados")
                if self.receitanet.validar_solicitacao():
                    self.receitanet.baixar_arquivos()
                    self.receitanet.manipular_arquivos(tipo, self.contribuinte)
            else:
                logging.info("Nenhum arquivo para baixar")
                self.receitanet.validar_solicitacao()
        except DownloadError:
            raise
        except Exception as exc:
            raise DownloadError(f"Erro ao baixar {tipo}: {exc}") from exc

    def process_download(
        self,
        sped_type: SpedType,
        sistema: str,
        sistema_anterior: Optional[str],
        tipo_arquivo: str,
        validacao: Optional[str],
        periodo: str,
        periodo_anterior: Optional[str] = None,
    ) -> None:
        """
        Processa o download de qualquer modalidade SPED.

        Args:
            sped_type (SpedType): Tipo de SPED a ser baixado.
            sistema (str): Identificador do sistema na interface.
            sistema_anterior (Optional[str]): Sistema anterior para navegação.
            tipo_arquivo (str): Tipo de arquivo a ser selecionado.
            validacao (Optional[str]): Identificador do tipo de validação.
            periodo (str): Identificador do período.
            periodo_anterior (Optional[str]): Identificador do período anterior, quando necessário.
        """
        tipo = sped_type.label
        logging.info("* INICIANDO PROCESSO DE DOWNLOAD DO %s *", tipo)
        try:
            self.receitanet.selecionar_sistema(
                sistema=sistema, sistema_anterior=sistema_anterior
            )
            self.receitanet.selecionar_arquivo(
                tipo_arquivo=tipo_arquivo, validacao=validacao
            )
            self.receitanet.selecionar_periodo(
                periodo=periodo, periodo_anterior=periodo_anterior
            )

            if sped_type is SpedType.FISCAL:
                self.receitanet.input_campos_fiscais(
                    primeiro_dia=self.data_inicial, ultimo_dia=self.data_final
                )
                self._finalizar_processo(tipo)
            else:
                self._processar_outros_speds(sped_type)

            logging.info("* FUNÇÃO %s FINALIZADA *", tipo)
        except DownloadError:
            raise
        except Exception as exc:
            raise DownloadError(f"Erro ao baixar {tipo}: {exc}") from exc

    def download_sped_contabil(self) -> None:
        """Realiza o download do SPED Contábil (ECD)."""
        self.process_download(
            sped_type=SpedType.CONTABIL,
            sistema="combobox-sped-contabil",
            sistema_anterior="combobox-sped-contribuicoes",
            tipo_arquivo="combobox-escrituracao-contabil-digital",
            validacao="combobox-escrituracao-contabil-digital",
            periodo="validacao-periodo-contabil",
        )

    def download_sped_contribuicoes(self) -> None:
        """Realiza o download do SPED Contribuições (EFD Contribuições)."""
        self.process_download(
            sped_type=SpedType.CONTRIBUICOES,
            sistema="combobox-sped-contribuicoes",
            sistema_anterior=None,
            tipo_arquivo="combobox-escrituracao",
            validacao="combobox-validacao-escrituracao",
            periodo="combobox-periodo-escrituracao",
            periodo_anterior="combobox-entrega-da-incorporada",
        )

    def download_sped_ecf(self) -> None:
        """Realiza o download do SPED ECF (Escrituração Contábil Fiscal)."""
        self.process_download(
            sped_type=SpedType.ECF,
            sistema="combobox-sped-ecf",
            sistema_anterior="combobox-sped-contabil",
            tipo_arquivo="combobox-escrituracao",
            validacao="combobox-validacao-escrituracao",
            periodo="combobox-periodo-escrituracao",
            periodo_anterior="combobox-entrega",
        )

    def download_sped_fiscal(self) -> None:
        """Realiza o download do SPED Fiscal (EFD ICMS/IPI)."""
        self.process_download(
            sped_type=SpedType.FISCAL,
            sistema="combobox-sped-fiscal",
            sistema_anterior="combobox-sped-ecf",
            tipo_arquivo="combobox-escrituracao-fiscal",
            validacao="combobox-escrituracao-fiscal",
            periodo="validacao-periodo-fiscal",
        )
