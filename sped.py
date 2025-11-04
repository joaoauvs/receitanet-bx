import logging
import time
from os import path

from receitanet import ReceitaNetBx
from src.core.bot import DesktopBot


class Sped(DesktopBot):
    """Rotinas de download para os diferentes tipos de arquivos SPED."""

    def __init__(self, contribuinte, data_inicial, data_final):
        """
        Inicializa o fluxo com os dados do contribuinte.

        Args:
            contribuinte (str): CNPJ utilizado na consulta.
            data_inicial (str): Data inicial do periodo.
            data_final (str): Data final do periodo.
        """
        super().__init__()
        self.contribuinte = contribuinte
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.receitanet = ReceitaNetBx()
        base_dir = path.abspath(path.dirname(__file__))
        images_dir = path.join(base_dir, "src", "images")
        self.dir_baixa = path.join(images_dir, "baixa")
        self.dir_selector_box = path.join(images_dir, "seletor-box")
        self.add_image("button-criterios-acima", path.join(self.dir_baixa, "button-criterios-acima.png"))
        self.add_image("button-pesquisar", path.join(self.dir_baixa, "button-pesquisar.png"))
        self.add_image("button-solicitar-arquivos-marcados", path.join(self.dir_baixa, "button-solicitar-arquivos-marcados.png"))
        self.add_image("resultado-pesquisa", path.join(self.dir_baixa, "resultado-pesquisa.png"))

    def wait_for_element(self, element, timeout=30, matching=0.97):
        """
        Aguarda um elemento aparecer na tela ate um tempo limite.

        Args:
            element (str): Identificador do elemento.
            timeout (int): Tempo maximo de espera em segundos.
            matching (float): Precisao minima da correspondencia.

        Returns:
            bool: True se o elemento for encontrado dentro do tempo limite.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.find(element, matching=matching):
                return True
            time.sleep(0.5)
        return False

    def _solicitar_arquivos_criterios_acima(self, tipo):
        """
        Solicita os arquivos aplicando os criterios previamente definidos.

        Args:
            tipo (str): Tipo de arquivo SPED a ser baixado.
        """
        logging.info("Clicando no botao Solicitar Arquivos usando os criterios acima")
        self.find_click_image(identifier="button-criterios-acima", match=0.97)
        if self.receitanet.validar_solicitacao():
            self.receitanet.baixar_arquivos()
            self.receitanet.manipular_arquivos(tipo, self.contribuinte)

    def _pesquisar_e_solicitar_arquivos(self, tipo):
        """
        Pesquisa e solicita o download dos arquivos encontrados.

        Args:
            tipo (str): Tipo de arquivo SPED a ser baixado.
        """
        logging.info("Selecionando o button -> PESQUISAR <-")
        self.click_image("button-pesquisar")
        if self.wait_for_element("resultado-pesquisa"):
            logging.info("Arquivo encontrado")
            self.find_click_list_image(path=self.dir_selector_box)
            if self.wait_for_element("button-solicitar-arquivos-marcados"):
                logging.info("Selecionando o button -> SOLICITAR ARQUIVOS MARCADOS <-")
                self.click_image("button-solicitar-arquivos-marcados")
                if self.receitanet.validar_solicitacao():
                    self.receitanet.baixar_arquivos()
                    self.receitanet.manipular_arquivos(tipo, self.contribuinte)
        else:
            logging.info("Nao existe arquivo para baixar")
            self.receitanet.validar_solicitacao()

    def _processar_outros_speds(self, tipo):
        """
        Processa o download dos arquivos SPED que nao sao fiscais.

        Args:
            tipo (str): Tipo de arquivo SPED (ECF, Contribuicoes, Contabil).
        """
        self.receitanet.input_data(self.data_inicial, self.data_final)

        if tipo in ["SPED ECF", "SPED Contribuicoes"]:
            self._solicitar_arquivos_criterios_acima(tipo)

        if tipo == "SPED Contabil":
            self._pesquisar_e_solicitar_arquivos(tipo)

    def _finalizar_processo(self, tipo):
        """
        Finaliza o processo de download verificando resultados e solicitando arquivos.

        Args:
            tipo (str): Tipo de arquivo SPED sendo processado.
        """
        try:
            if self.find("resultado-pesquisa", matching=0.9):
                logging.info("Arquivo encontrado")
                time.sleep(5)
                logging.info("Validando se existe o seletor para marcar arquivos")
                self.find_click_list_image(path=self.dir_selector_box)
                time.sleep(10)
                logging.info("Selecionando o button -> SOLICITAR ARQUIVOS MARCADOS <-")
                self.click_image("button-solicitar-arquivos-marcados")
                if self.receitanet.validar_solicitacao():
                    self.receitanet.baixar_arquivos()
                    self.receitanet.manipular_arquivos(tipo, self.contribuinte)
            else:
                logging.info("Nao existe arquivo para baixar")
                self.receitanet.validar_solicitacao()
        except Exception as exc:
            raise Exception(f"Erro ao baixar o {tipo}: {exc}") from exc

    def process_download(self, tipo, sistema, sistema_anterior, tipo_arquivo, validacao, periodo, periodo_anterior=None):
        """
        Processa o download de qualquer modalidade de SPED.

        Args:
            tipo (str): Identificador do arquivo (ex.: 'SPED Fiscal').
            sistema (str): Identificador do sistema na interface.
            sistema_anterior (str): Sistema anterior para navegacao.
            tipo_arquivo (str): Tipo de arquivo a ser selecionado.
            validacao (str): Identificador do tipo de validacao.
            periodo (str): Identificador do periodo.
            periodo_anterior (str | None): Identificador do periodo anterior, quando necessario.
        """
        logging.info("* INICIANDO O PROCESSO DE BAIXA DO %s *", tipo)
        try:
            self.receitanet.selecionar_sistema(sistema=sistema, sistema_Anterior=sistema_anterior)
            self.receitanet.selecionar_arquivo(tipo_Arquivo=tipo_arquivo, validacao=validacao)
            self.receitanet.selecionar_periodo(periodo=periodo, periodo_Anterior=periodo_anterior)

            if tipo == "SPED Fiscal":
                self.receitanet.input_campos_fiscais(primeiro_dia=self.data_inicial, ultimo_dia=self.data_final)
                self._finalizar_processo(tipo)
            else:
                self._processar_outros_speds(tipo)

            logging.info("* FUNCAO %s FINALIZADA *", tipo)
        except Exception as exc:
            raise Exception(f"Erro ao baixar o {tipo}: {exc}") from exc

    def download_sped_contabil(self):
        """Realiza o download do arquivo SPED Contabil (ECD)."""
        self.process_download(
            tipo="SPED Contabil",
            sistema="combobox-sped-contabil",
            sistema_anterior="combobox-sped-contribuicoes",
            tipo_arquivo="combobox-escrituracao-contabil-digital",
            validacao="combobox-escrituracao-contabil-digital",
            periodo="validacao-periodo-contabil",
        )

    def download_sped_contribuicoes(self):
        """Realiza o download do arquivo SPED Contribuicoes (EFD Contribuicoes)."""
        self.process_download(
            tipo="SPED Contribuicoes",
            sistema="combobox-sped-contribuicoes",
            sistema_anterior=None,
            tipo_arquivo="combobox-escrituracao",
            validacao="combobox-validacao-escrituracao",
            periodo="combobox-periodo-escrituracao",
            periodo_anterior="combobox-entrega-da-incorporada",
        )

    def download_sped_ecf(self):
        """Realiza o download do arquivo SPED ECF (Escrituracao Contabil Fiscal)."""
        self.process_download(
            tipo="SPED ECF",
            sistema="combobox-sped-ecf",
            sistema_anterior="combobox-sped-contabil",
            tipo_arquivo="combobox-escrituracao",
            validacao="combobox-validacao-escrituracao",
            periodo="combobox-periodo-escrituracao",
            periodo_anterior="combobox-entrega",
        )

    def download_sped_fiscal(self):
        """Realiza o download do arquivo SPED Fiscal (EFD ICMS/IPI)."""
        self.process_download(
            tipo="SPED Fiscal",
            sistema="combobox-sped-fiscal",
            sistema_anterior="combobox-sped-ecf",
            tipo_arquivo="combobox-escrituracao-fiscal",
            validacao="combobox-escrituracao-fiscal",
            periodo="validacao-periodo-fiscal",
        )
