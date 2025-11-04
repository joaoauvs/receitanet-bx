import logging
import time
from os import path

from receitanet import ReceitaNetBx
from resources.core import DesktopBot


class Sped(DesktopBot):
    """
    Classe Sped herda de DesktopBot e contém métodos para fazer o download de diferentes tipos de Sped.
    """

    def __init__(self, contribuinte, data_inicial, data_final):
        """
        Inicializa a classe Sped com os parâmetros necessários para fazer o download de um Sped.

        Args:
            contribuinte (str): CNPJ do contribuinte.
            data_inicial (str): Data inicial do período.
            data_final (str): Data final do período.
        """
        super().__init__()
        self.contribuinte = contribuinte
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.receitanet = ReceitaNetBx()
        self.dir_baixa = path.abspath(path.dirname(__file__)) + "/resources/images/baixa"
        self.dir_selector_box = path.abspath(path.dirname(__file__)) + "/resources/images/seletor-box"
        self.add_image("button-criterios-acima", self.dir_baixa + "/button-criterios-acima.png")
        self.add_image("button-pesquisar", self.dir_baixa + "/button-pesquisar.png")
        self.add_image("button-solicitar-arquivos-marcados", self.dir_baixa + "/button-solicitar-arquivos-marcados.png")
        self.add_image("resultado-pesquisa", self.dir_baixa + "/resultado-pesquisa.png")

    def wait_for_element(self, element, timeout=30, matching=0.97):
        """
        Método para esperar um elemento aparecer na tela com um timeout.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.find(element, matching=matching):
                return True
            time.sleep(0.5)
        return False

    def _solicitar_arquivos_criterios_acima(self, tipo):
        """
        Solicita arquivos usando os critérios já definidos acima.

        Args:
            tipo (str): Tipo de arquivo SPED a ser baixado.
        """
        logging.info("Clicando no botão Solicitar Arquivos Usando os Critérios Acima")
        self.find_click_image(identifier="button-criterios-acima", match=0.97)
        if self.receitanet.validar_solicitacao():
            self.receitanet.baixar_arquivos()
            self.receitanet.manipular_arquivos(tipo, self.contribuinte)

    def _pesquisar_e_solicitar_arquivos(self, tipo):
        """
        Pesquisa por arquivos disponíveis e solicita o download dos encontrados.

        Args:
            tipo (str): Tipo de arquivo SPED a ser baixado.
        """
        logging.info("Selecionando o Button -> PESQUISAR <-")
        self.click_image("button-pesquisar")
        if self.wait_for_element("resultado-pesquisa"):
            logging.info("Arquivo encontrado")
            self.find_click_list_image(path=self.dir_selector_box)
            if self.wait_for_element("button-solicitar-arquivos-marcados"):
                logging.info("Selecionando o Button -> SOLICITAR ARQUIVOS MARCADOS <-")
                self.click_image("button-solicitar-arquivos-marcados")
                if self.receitanet.validar_solicitacao():
                    self.receitanet.baixar_arquivos()
                    self.receitanet.manipular_arquivos(tipo, self.contribuinte)
        else:
            logging.info("Não existe arquivo para baixar")
            self.receitanet.validar_solicitacao()

    def _processar_outros_speds(self, tipo):
        """
        Processa o download de arquivos SPED (exceto Fiscal).

        Args:
            tipo (str): Tipo de arquivo SPED (ECF, Contribuições, Contábil).
        """
        self.receitanet.input_data(self.data_inicial, self.data_final)

        if tipo in ["SPED ECF", "SPED Contribuições"]:
            self._solicitar_arquivos_criterios_acima(tipo)

        if tipo == "SPED Contábil":
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
                logging.info("Validando se Box -> SELECIONAR <- existe")
                self.find_click_list_image(path=self.dir_selector_box)
                time.sleep(10)
                logging.info("Selecionando o Button -> SOLICITAR ARQUIVOS MARCADOS <-")
                self.click_image("button-solicitar-arquivos-marcados")
                if self.receitanet.validar_solicitacao():
                    self.receitanet.baixar_arquivos()
                    self.receitanet.manipular_arquivos(tipo, self.contribuinte)
            else:
                logging.info("Não existe arquivo para baixar")
                self.receitanet.validar_solicitacao()
        except Exception as e:
            raise Exception(f"Erro ao baixar o {tipo}: {e}")

    def process_download(self, tipo, sistema, sistema_anterior, tipo_arquivo, validacao, periodo, periodo_anterior=None):
        """
        Método genérico para processar o download de qualquer tipo de SPED.

        Args:
            tipo (str): Tipo de arquivo SPED (ex: 'SPED Fiscal', 'SPED Contribuições').
            sistema (str): Identificador do sistema na interface.
            sistema_anterior (str): Sistema anterior para navegação.
            tipo_arquivo (str): Tipo de arquivo a ser selecionado.
            validacao (str): Tipo de validação do arquivo.
            periodo (str): Período dos dados.
            periodo_anterior (str, optional): Período anterior para navegação.
        """
        logging.info(f"* INICIANDO O PROCESSO DE BAIXA DO {tipo} *")
        try:
            self.receitanet.selecionar_sistema(sistema=sistema, sistema_Anterior=sistema_anterior)
            self.receitanet.selecionar_arquivo(tipo_Arquivo=tipo_arquivo, validacao=validacao)
            self.receitanet.selecionar_periodo(periodo=periodo, periodo_Anterior=periodo_anterior)

            if tipo == "SPED Fiscal":
                self.receitanet.input_campos_fiscais(primeiro_dia=self.data_inicial, ultimo_dia=self.data_final)
                self._finalizar_processo(tipo)
            else:
                self._processar_outros_speds(tipo)

            logging.info(f"* FUNÇÃO {tipo} FINALIZADA *")
        except Exception as e:
            raise Exception(f"Erro ao baixar o {tipo}: {e}")

    def download_sped_contabil(self):
        """
        Realiza o download do arquivo SPED Contábil (ECD).
        """
        self.process_download(
            tipo="SPED Contábil",
            sistema="combobox-sped-contabil",
            sistema_anterior="combobox-sped-contribuicoes",
            tipo_arquivo="combobox-escrituracao-contabil-digital",
            validacao="combobox-escrituracao-contabil-digital",
            periodo="validacao-periodo-contabil",
        )

    def download_sped_contribuicoes(self):
        """
        Realiza o download do arquivo SPED Contribuições (EFD Contribuições).
        """
        self.process_download(
            tipo="SPED Contribuições",
            sistema="combobox-sped-contribuicoes",
            sistema_anterior=None,
            tipo_arquivo="combobox-escrituracao",
            validacao="combobox-validacao-escrituracao",
            periodo="combobox-periodo-escrituracao",
            periodo_anterior="combobox-entrega-da-incorporada",
        )

    def download_sped_ecf(self):
        """
        Realiza o download do arquivo SPED ECF (Escrituração Contábil Fiscal).
        """
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
        """
        Realiza o download do arquivo SPED Fiscal (EFD ICMS/IPI).
        """
        self.process_download(
            tipo="SPED Fiscal",
            sistema="combobox-sped-fiscal",
            sistema_anterior="combobox-sped-ecf",
            tipo_arquivo="combobox-escrituracao-fiscal",
            validacao="combobox-escrituracao-fiscal",
            periodo="validacao-periodo-fiscal",
        )
