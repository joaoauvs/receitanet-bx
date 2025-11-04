import logging
import os
import random
import shutil
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

from src.core.bot import DesktopBot


class ReceitaNetBx(DesktopBot):
    """
    Classe destinada a automatizar tarefas relacionadas ao aplicativo "Receitanet BX".

    Attributes:
        id_execucao (int): Identificador único da execução.
        dir_docs (str): Diretório padrão para documentos relacionados ao ReceitanetBX.
        nome_app (str): Nome do aplicativo.
        dir_app (str): Diretório do atalho do aplicativo.
        image_paths (dict): Dicionário contendo os caminhos para as imagens utilizadas.
    """

    def __init__(self):
        """
        Inicializa a classe ReceitaNetBx.
        """
        super().__init__()
        self.found = threading.Event()
        self.dir_docs = Path.home() / "Documents/Arquivos ReceitanetBX"
        self.nome_app = "Receitanet BX"
        self.dir_app = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Programas RFB\Receitanet BX\Receitanet BX 1.9.24.lnk"

        base_dir = os.path.abspath(os.path.dirname(__file__))
        resources_dir = os.path.join(base_dir, "src", "images")

        self.dir_login = os.path.join(resources_dir, "login")
        self.list_btn_entrar = os.path.join(resources_dir, "button-entrar")
        self.certificado_alz = os.path.join(resources_dir, "icon-certificado-alz")
        self.certificado_auditoria = os.path.join(resources_dir, "icon-certificado-auditoria")
        self.select_todos = os.path.join(resources_dir, "selecionar-todos")
        self.dir_pop_ups = os.path.join(resources_dir, "pop-ups")
        self.dir_baixa = os.path.join(resources_dir, "baixa")
        self.dir_sped_fiscal = os.path.join(resources_dir, "sped-fiscal")
        self.dir_combobox_sistema = os.path.join(resources_dir, "combobox-sistemas")
        self.dir_combobox_arquivo = os.path.join(resources_dir, "combobox-arquivos")
        self.dir_combobox_periodo = os.path.join(resources_dir, "combobox-periodos")
        self.dir_selecione_sistema = os.path.join(self.dir_combobox_sistema, "selecione sistema")
        self.dir_selecione_arquivo = os.path.join(self.dir_combobox_arquivo, "selecione arquivo")
        self.dir_selecione_periodo = os.path.join(self.dir_combobox_periodo, "selecione periodo")
        self.list_btn_baixar = os.path.join(self.dir_baixa, "button-baixar")
        self.list_icon_marcar = os.path.join(self.dir_baixa, "icon-marcar")
        self.result = None

    def abrir_aplicativo(self):
        """
        Abre o aplicativo Receitanet BX.
        """
        logging.info("Abrindo app > ReceitanetBX <")
        try:
            self.execute(self.dir_app)
            self.focus_window_app(self.nome_app)
        except Exception as e:
            raise Exception(f"Erro ao abrir o aplicativo: {e}")

    def fechar_aplicativo(self):
        """
        Fecha o aplicativo Receitanet BX.
        """
        try:
            logging.info("Encerrando aplicativo")
            subprocess.Popen("taskkill /f /im javaw.exe")
        except Exception as e:
            raise Exception(f"Erro ao encerrar aplicativo: {e}")

    def load_images(self):
        """
        Carrega as imagens necessárias para a execução do robô.
        """
        try:
            self.add_image("atualizar-lista", os.path.join(self.dir_login, "atualizar-lista.png"))
            self.add_image("box-buscar-todos", os.path.join(self.dir_sped_fiscal, "box-buscar-todos.png"))
            self.add_image("box-ultimo-arquivo", os.path.join(self.dir_sped_fiscal, "box-ultimo-arquivo.png"))
            self.add_image("button-pesquisar", os.path.join(self.dir_baixa, "button-pesquisar.png"))
            self.add_image("button-solicitar-arquivos-marcados", os.path.join(self.dir_baixa, "button-solicitar-arquivos-marcados.png"))
            self.add_image("combobox-dados-agregados", os.path.join(self.dir_combobox_arquivo, "dados-agregados-escrituracao.png"))
            self.add_image("combobox-entrega", os.path.join(self.dir_combobox_periodo, "periodo-de-entrega.png"))
            self.add_image("combobox-entrega-da-incorporada", os.path.join(self.dir_combobox_periodo, "periodo-de-entrega-da-incorporada.png"))
            self.add_image("combobox-escrituracao", os.path.join(self.dir_combobox_arquivo, "escrituracao.png"))
            self.add_image("combobox-escrituracao-contabil-digital", os.path.join(self.dir_combobox_arquivo, "escrituracao-contabil-digital.png"))
            self.add_image("combobox-escrituracao-da-incorporada", os.path.join(self.dir_combobox_periodo, "periodo-de-escrituracao-da-incorporada.png"))
            self.add_image("combobox-escrituracao-fiscal", os.path.join(self.dir_combobox_arquivo, "escrituracao-fiscal.png"))
            self.add_image("combobox-perfil", os.path.join(self.dir_login, "combobox-contribuinte.png"))
            self.add_image("combobox-periodo-escrituracao", os.path.join(self.dir_combobox_periodo, "periodo-escrituracao.png"))
            self.add_image("combobox-periodo-entrega", os.path.join(self.dir_combobox_periodo, "periodo-de-entrega.png"))
            self.add_image("combobox-sped-contabil", os.path.join(self.dir_combobox_sistema, "contabil.png"))
            self.add_image("combobox-sped-contribuicoes", os.path.join(self.dir_combobox_sistema, "contribuicoes.png"))
            self.add_image("combobox-sped-ecf", os.path.join(self.dir_combobox_sistema, "ecf.png"))
            self.add_image("combobox-sped-fiscal", os.path.join(self.dir_combobox_sistema, "fiscal.png"))
            self.add_image("combobox-termos-junta-comercial", os.path.join(self.dir_combobox_arquivo, "termos-junta-comercial.png"))
            self.add_image("combobox-validacao-escrituracao", os.path.join(self.dir_combobox_arquivo, "validacao-escrituracao.png"))
            self.add_image("fim-download", os.path.join(self.dir_baixa, "fim-download.png"))
            self.add_image("icon-acompanhamento", os.path.join(self.dir_baixa, "icon-acompanhamento.png"))
            self.add_image("icon-marcar", os.path.join(self.dir_baixa, "icon-marcar.png"))
            self.add_image("icon-pesquisa", os.path.join(self.dir_baixa, "icon-pesquisa.png"))
            self.add_image("input-cnjp", os.path.join(self.dir_sped_fiscal, "input-cnpj.png"))
            self.add_image("input-data-fim", os.path.join(self.dir_baixa, "data-fim.png"))
            self.add_image("input-data-fim-fiscal", os.path.join(self.dir_sped_fiscal, "input-data-fim.png"))
            self.add_image("input-data-fim-incorporada", os.path.join(self.dir_baixa, "data-fim-incorporada.png"))
            self.add_image("input-data-inicio", os.path.join(self.dir_baixa, "data-inicio.png"))
            self.add_image("input-data-inicio-fiscal", os.path.join(self.dir_sped_fiscal, "input-data-inicio.png"))
            self.add_image("input-data-inicio-incorporada", os.path.join(self.dir_baixa, "data-inicio-incorporada.png"))
            self.add_image("input-pf", os.path.join(self.dir_login, "input-cpf.png"))
            self.add_image("input-pj", os.path.join(self.dir_login, "input-cnpj.png"))
            self.add_image("input-procurador", os.path.join(self.dir_baixa, "cnpj-incorporada.png"))
            self.add_image("login-efetuado", os.path.join(self.dir_login, "validate-login.png"))
            self.add_image("msg-aguardando", os.path.join(self.dir_baixa, "msg-aguardando.png"))
            self.add_image("msg-erro-data", os.path.join(self.dir_baixa, "msg-erro-data.png"))
            self.add_image("msg-falha-comunicacao", self.dir_baixa + "/msg-falha-comunicacao-servidor.png")
            self.add_image("msg-nao-existe-procuracao", self.dir_baixa + "/msg-nao-existe-procuracao.png")
            self.add_image("msg-procuracao-vencida", self.dir_baixa + "/msg-procuracao-vencida.png")
            self.add_image("pop-up-error", self.dir_pop_ups + "/erro.png")
            self.add_image("pop-up-nao-encontrado", self.dir_pop_ups + "/nao-encontrado.png")
            self.add_image("pop-up-pedido", self.dir_pop_ups + "/pedido.png")
            self.add_image("popup-nenhum-arquivo", self.dir_pop_ups + "/nenhum-arquivo.png")
            self.add_image("procurador-pf", self.dir_login + "/procurador-pf.png")
            self.add_image("procurador-pj", self.dir_login + "/procurador-pj.png")
            self.add_image("resultado-pesquisa", self.dir_baixa + "/resultado-pesquisa.png")
            self.add_image("selecionar-procurador", self.dir_login + "/combobox-procurador.png")
            self.add_image("validacao-periodo-contabil", self.dir_combobox_periodo + "/validacao-periodo-contabil.png")
            self.add_image("validacao-periodo-fiscal", self.dir_combobox_periodo + "/validacao-periodo-fiscal.png")
            self.add_image("verificar-pedidos", self.dir_baixa + "/verificar-pedidos.png")
        except Exception as e:
            raise Exception(f"[FALHA AO CARREGAR IMAGENS]: {e}")

    def verificar_popup(self, nome_popup, acao, log_msg, status, resultado):
        """
        Verifica se existe um popup específico na tela e executa uma ação.

        Args:
            nome_popup (str): Nome/identificador do popup a ser verificado.
            acao (str): Ação a ser executada se o popup for encontrado.
            log_msg (str): Mensagem para logging.
            status (str): Status da operação.
            resultado (str): Resultado da operação.
        """
        if not self.found.is_set() and self.find(nome_popup, matching=0.8):
            with threading.Lock():
                if not self.found.is_set():  # Verifica novamente para evitar condições de corrida
                    self.click()
                    self.enter()
                    logging.info(log_msg)
                    self.result = acao
                    self.found.set()  # Sinaliza que uma condição foi satisfeita

    def login(self, contribuinte):
        """
        Faz o login no aplicativo Receitanet BX.

        Args:
            contribuinte (str): CNPJ do contribuinte.
        """
        max_tentativas = 4
        logging.info("* INICIANDO A FUNÇÃO -> LOGIN CERTIFICADO <- *")
        for attempt_count in range(1, max_tentativas + 1):
            try:
                self.abrir_aplicativo()
                self.load_images()
                logging.info("Logando com certificado A1")
                logging.info("Selecionando o -> Certificado A1 <-")
                self.find_click_list_image(path=self.certificado_alz, match=0.7)
                logging.info("Selecionando a Combo Box -> Selecione um Perfil de Acesso <-")
                self.find_click_image(identifier="combobox-perfil", match=0.8)
                logging.info("Selecionando a Combo Box -> Procurador <-")
                self.find_click_image(identifier="selecionar-procurador", match=0.8)
                logging.info("Procurador PJ")
                self.find_click_image(identifier="procurador-pf", match=0.8)
                logging.info("Selecionando o -> Procurador PJ <-")
                self.find_click_image(identifier="procurador-pj", match=0.8)
                logging.info("Selecionando o Input -> CNPJ <-")
                self.find_click_image(identifier="input-pj", match=0.8)
                logging.info("Inserindo o CNPJ do procurador")
                self.control_a()
                self.paste(contribuinte)
                self.tab()
                time.sleep(3)
                logging.info("Selecionando o Button -> Entrar <-")
                self.find_click_list_image(path=self.list_btn_entrar, match=0.7)
                logging.info("Validando se o login foi efetuado")
                time.sleep(5)
                if self.validate_exists(identifier="login-efetuado", match=0.7):
                    self.maximize_window()
                    time.sleep(5)
                    logging.info("* LOGIN EFETUADO COM SUCESSO")
                    break
                else:
                    self.fechar_aplicativo()
                    time.sleep(5)
            except Exception as e:
                logging.warning(f"Erro ao logar no Receitanet BX: {e}")
                self.fechar_aplicativo()
                time.sleep(5)
        else:
            raise Exception("[FALHA]: Ocorreu um erro ao tentar logar com o certificado A1")

    def selecionar_sistema(self, sistema, sistema_Anterior=None):
        """
        Seleciona o sistema e o tipo de arquivo desejado.

        Args:
            sistema (str): Sistema desejado.
            sistema_Anterior (str): Sistema anterior ao desejado.
        """
        logging.info("* SELECIONANDO O SISTEMA E O TIPO DE ARQUIVO *")
        try:
            self.load_images()
            self.mudar_tela_pesquisa()
            if self.validate_list_exists(path=self.dir_selecione_sistema):
                self.find_click_list_image(path=self.dir_selecione_sistema)
                self.click_image(sistema)
            else:
                if self.validate_exists(identifier=sistema):
                    pass
                elif self.validate_exists(identifier=sistema_Anterior):
                    self.click_image(sistema_Anterior)
                    self.click_image(sistema)
                else:
                    raise Exception(f"Erro ao selecionar o sistema: {sistema}")
            logging.info(f"Sistema selecionado: {sistema}")
        except Exception as e:
            raise Exception(f"[FALHA]: Ao selecionar o sistema: {e}")

    def selecionar_arquivo(self, tipo_Arquivo, validacao=None, tipo_Arquivo_Anterior=None):
        """
        Seleciona o tipo de arquivo desejado.

        Args:
            tipo_Arquivo (str): Tipo de arquivo desejado.
            validacao (str): Tipo de arquivo de validação.
            tipo_Arquivo_Anterior (str): Tipo de arquivo anterior ao desejado.
        """
        logging.info("* SELECIONANDO O TIPO DE ARQUIVO *")
        try:
            self.load_images()
            if self.validate_list_exists(path=self.dir_selecione_arquivo):
                self.find_click_list_image(path=self.dir_selecione_arquivo)
                self.click_image(tipo_Arquivo, confidence=0.8)
            else:
                logging.info("Selecionando o tipo de arquivo anterior")
                if self.validate_exists(identifier=validacao):
                    pass
                elif self.validate_exists(identifier=tipo_Arquivo_Anterior):
                    self.click_image(tipo_Arquivo_Anterior)
                    self.click_image(tipo_Arquivo)
                else:
                    raise Exception(f"Erro ao selecionar o tipo de arquivo: {tipo_Arquivo}")
            logging.info(f"Tipo de arquivo selecionado: {tipo_Arquivo}")
        except Exception as e:
            raise Exception(f"[FALHA]: Ao selecionar o tipo de arquivo: {e}")

    def selecionar_periodo(self, periodo, periodo_Anterior=None):
        """
        Seleciona o período desejado.

        Args:
            periodo (str): Período desejado.
            periodo_Anterior (str): Período anterior ao desejado.
        """
        try:
            self.load_images()
            logging.info(f"Selecionando o periodo: {periodo}")
            if self.validate_list_exists(path=self.dir_selecione_periodo):
                self.find_click_list_image(path=self.dir_selecione_periodo)
                self.click_image(periodo)
            else:
                if self.validate_exists(identifier=periodo):
                    pass
                elif self.validate_exists(identifier=periodo_Anterior):
                    self.click_image(periodo_Anterior, confidence=0.8)
                    self.click_image(periodo, confidence=0.8)
                else:
                    raise Exception(f"Erro ao selecionar o periodo: {periodo}")
        except Exception as e:
            raise Exception(f"[FALHA]: Ao selecionar o periodo: {e}")

    def mudar_tela_pesquisa(self):
        """
        Muda para a tela de pesquisa.
        """
        try:
            self.load_images()
            self.wait_window_app(self.nome_app, extension="javaw.exe")
            self.find("icon-pesquisa", matching=0.9)
            self.click()
            self.double_click()
        except Exception as e:
            raise (logging.warning(f"Erro ao trocar para pesquisar: {e}"))

    def input_data(self, primeiro_dia, ultimo_dia):
        """
        Insere a data inicial e a data final.

        Args:
            primeiro_dia (str): Data inicial.
            ultimo_dia (str): Data final.
        """
        logging.info("* INICIANDO A FUNÇÃO -> INPUT DATA <- *")
        try:
            self.load_images()
            logging.info("Selecionando o Input -> Data Inicio <-")
            if self.validate_exists(identifier="input-data-inicio"):
                self.double_click()
                time.sleep(2)
                self.type_key(primeiro_dia)
                self.tab()
                logging.info("Selecionando o Input -> Data Fim <-")
                if self.validate_exists(identifier="input-data-fim"):
                    self.double_click()
                    time.sleep(2)
                    self.type_key(ultimo_dia)
                    self.enter()
                else:
                    raise Exception(f"Erro ao inserir a data final: {ultimo_dia}")
            else:
                raise Exception(f"Erro ao inserir a data inicial: {primeiro_dia}")
            logging.info("* INPUT DATA EFETUADO COM SUCESSO")
        except Exception as e:
            raise Exception(f"[FALHA]: Ao inserir a data: {e}")

    def input_incorporada(self, primeiro_dia, ultimo_dia, contribuinte):
        """
        Insere a data inicial, a data final e o CNPJ da incorporada.

        Args:
            primeiro_dia (str): Data inicial.
            ultimo_dia (str): Data final.
            contribuinte (str): CNPJ da incorporada.
        """
        logging.info("* INICIANDO O INPUT DOS DADOS DA INCORPORADA *")
        try:
            self.load_images()
            logging.info("Inserindo a Data Inicio")
            logging.info("Inserindo a -> DATA INICIO <-")
            self.validate_exists(identifier="input-data-inicio-incorporada", match=0.8)
            self.double_click()
            self.type_key(primeiro_dia)
            self.tab()
            logging.info("Inserindo a -> DATA FIM <-")
            self.validate_exists(identifier="input-data-fim-incorporada", match=0.8)
            self.double_click()
            self.type_key(ultimo_dia)
            self.tab()
            logging.info("Inserindo o -> CNPJ <-")
            self.validate_exists(identifier="input-procurador", match=0.8)
            self.double_click()
            self.type_key(contribuinte)
            self.enter()
            logging.info("* INPUT DOS DADOS DA INCORPORADA FINALIZADO! *")
        except Exception as e:
            raise Exception(f"[FALHA]: Ao inserir os dados da incorporada: {e}")

    def input_campos_fiscais(self, primeiro_dia, ultimo_dia):
        """
        Insere a data inicial e a data final.

        Args:
            primeiro_dia (str): Data inicial.
            ultimo_dia (str): Data final.
        """
        logging.info("INSERINDO DADOS: CNPJ, DATA DE INICIO E DATA DE FIM")
        try:
            if self.validate_exists(identifier="box-buscar-todos", match=0.87):
                logging.info("Clicando no box -> Buscar Arquivos de Todos os Estabelecimentos <-")
                self.click_image("box-buscar-todos", 0.9)
                self.tab()
                self.tab()
                self.tab()
                logging.info("Validando se o campo Data de Inicio está ativo")
                if self.validate_exists(identifier="input-data-inicio-fiscal"):
                    self.double_click()
                    logging.info("INSERINDO DADOS: DATA DE INICIO")
                    self.type_key(primeiro_dia)
                    self.tab()
                    logging.info("Selecionando o Input -> Data Fim <-")
                    if self.validate_exists(identifier="input-data-fim-fiscal"):
                        self.double_click()
                        logging.info("INSERINDO DADOS: DATA DE FIM")
                        self.type_key(ultimo_dia)
                        if self.validate_exists(identifier="box-ultimo-arquivo"):
                            logging.info("Clicando no box -> Último Arquivo Transmitido <-")
                            self.click_image("box-ultimo-arquivo")
                            self.click_image("button-pesquisar")
                        else:
                            logging.warning("Não foi encontrado o box -> Último Arquivo Transmitido <-")
                    else:
                        raise Exception(f"Erro ao inserir a data final: {ultimo_dia}")
                else:
                    raise Exception(f"Erro ao inserir a data inicial: {primeiro_dia}")
            else:
                raise Exception(f"Erro ao clicar no box -> Buscar Arquivos de Todos os Estabelecimentos <-")
        except Exception as e:
            raise Exception(f"[FALHA]: Ao inserir os dados: {e}")

    def validar_solicitacao(self):
        """
        Valida se a solicitação foi registrada com sucesso.

        Returns:
            bool: True se a solicitação foi registrada com sucesso, False caso contrário.
        """
        try:
            self.load_images()
            while True:
                if not self.validate_exists(identifier="msg-aguardando"):
                    break

            popups = [
                ("msg-falha-comunicacao", False, "Falha na comunicação com o sistema do Receita Net!", "Falha", "Falha na comunicação com o sistema do Receita Net!"),
                ("pop-up-pedido", True, "Pedido Registrado Com Sucesso", "Processando...", "Pedido Registrado Com Sucesso!"),
                ("pop-up-error", False, "Erro ao registrar o pedido", "Falha", "Erro ao registrar o pedido!"),
                ("pop-up-nao-encontrado", False, "Não foi encontrado nenhum arquivo correspondente a pesquisa!", "Processado", "Não foi localizado nenhum arquivo!"),
                ("popup-nenhum-arquivo", False, "Não foi encontrado nenhum arquivo correspondente a pesquisa!", "Processado", "Não foi localizado nenhum arquivo!"),
                ("msg-erro-data", False, "A Data final deve ser igual ou menor que a data atual!", "Falha", "A Data final deve ser igual ou menor que a data atual!"),
                ("msg-procuracao-vencida", False, "A procuração está vencida!", "Falha", "Procuração eletrônica vencida!"),
                ("msg-nao-existe-procuracao", False, "Não existe procuração para este CNPJ!", "Falha", "Sem procuração para este CNPJ!"),
            ]

            # Criação e inicialização das threads
            threads = []
            for popup in popups:
                thread = threading.Thread(target=self.verificar_popup, args=(popup[0], popup[1], popup[2], popup[3], popup[4]))
                threads.append(thread)
                thread.start()

            # Aguarda todas as threads completarem
            for thread in threads:
                thread.join()

            if self.found.is_set():
                return self.result
            else:
                raise Exception("Nenhuma condição de popup foi satisfeita")
        except Exception as e:
            raise Exception(f"Erro ao validar a solicitação: {e}")

    def baixar_arquivos(self):
        """
        Faz o download dos arquivos solicitados.
        """
        logging.info("* INICIANDO A FUNÇÃO -> BAIXAR ARQUIVOS <- *")
        try:
            self.load_images()
            logging.info("Selecionando o Icon -> ACOMPANHAMENTO <-")
            self.find_click_image(identifier="icon-acompanhamento", match=0.9)
            logging.info("Selecionando o Icon -> VER PEDIDOS E ARQUIVOS <-")
            # self.find_click_image(identifier="verificar-pedidos", match=0.9)
            logging.info("Selecionando o Box do Pedido")
            self.find_click_list_image(path=self.list_icon_marcar, match=0.7, max_attempts=10)
            # time.sleep(20)
            logging.info("Selecionando o Box de Selecionar Todos")
            self.find_click_list_image(path=self.select_todos, match=0.9, max_attempts=10)
            # time.sleep(90)
            logging.info("Selecionando o Button -> Baixar <-")
            self.find_click_list_image(path=self.list_icon_marcar, match=0.7, max_attempts=10)
            self.find_click_list_image(path=self.list_btn_baixar, match=0.7, max_attempts=10)
            while True:
                if self.find("fim-download", matching=0.90):
                    logging.info("Download Finalizado")
                    break
        except Exception as e:
            raise Exception(f"[FALHA]: Ao baixar os arquivos: {e}")

    def _to_datetime(self, date_str, time_str):
        """
        Converte strings de data e hora para objeto datetime.

        Args:
            date_str (str): String da data no formato DD/MM/YYYY.
            time_str (str): String do horário no formato HH:MM:SS.

        Returns:
            datetime: Objeto datetime criado a partir das strings.
        """
        return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")

    def _buscar_arquivos_recentes(self, tipo):
        """
        Busca os arquivos mais recentes por período no diretório de documentos.

        Args:
            tipo (str): Tipo de arquivo SPED (Contribuições, ECF, etc.).

        Returns:
            dict: Dicionário com períodos como chaves e caminhos dos arquivos mais recentes.
        """
        arquivos_recentes_por_periodo = {}
        for arquivo in self.dir_docs.rglob("*.txt"):
            if "Contribuições" in tipo:
                itens = arquivo.stem.split("_")
                periodo = f"{itens[1][4:6]}/{itens[1][:4]}"
                transmissao_dia = f"{itens[5][6:8]}/{itens[5][4:6]}/{itens[5][:4]}"
                transmissao_hora = f"{itens[5][8:10]}:{itens[5][10:12]}:{itens[5][12:]}"
            elif "ECF" in tipo:
                itens = arquivo.stem.split("-")
                transmissao_dia = f"{itens[4][6:8]}/{itens[4][4:6]}/{itens[4][:4]}"
                transmissao_hora = f"{itens[4][8:10]}:{itens[4][10:12]}:{itens[4][12:14]}"
                periodo = f"{itens[3][4:6]}/{itens[3][:4]}"

            data_hora_atual = self._to_datetime(transmissao_dia, transmissao_hora)

            if periodo not in arquivos_recentes_por_periodo or data_hora_atual > arquivos_recentes_por_periodo[periodo][0]:
                arquivos_recentes_por_periodo[periodo] = (data_hora_atual, arquivo.name)
        return arquivos_recentes_por_periodo

    def manipular_arquivos(self, tipo, contribuinte):
        """
        Move o arquivo transmitido mais recentemente para a pasta de destino e exclui os demais.

        Args:
            tipo (str): Tipo de arquivo.
            contribuinte (str): CNPJ do contribuinte.
        """
        logging.info("* INICIANDO A FUNÇÃO -> MANIPULAR ARQUIVOS <- *")
        try:
            diretorio = Path.home() / f"OneDrive - Alianzo/ReceitaNet-Bx/{contribuinte}/{tipo}"
            diretorio.mkdir(parents=True, exist_ok=True)

            if "Contribuições" in tipo or "ECF" in tipo:
                arquivos_recentes_por_periodo = self._buscar_arquivos_recentes(tipo)

                for periodo, (data_hora_atual, arquivo) in arquivos_recentes_por_periodo.items():
                    shutil.move(self.dir_docs / arquivo, diretorio / arquivo)
            else:
                for arquivo in self.dir_docs.rglob("*"):
                    if arquivo.is_file():
                        shutil.move(arquivo, diretorio / arquivo.name)
            logging.info("* ARQUIVOS MOVIDOS COM SUCESSO *")
        except Exception as e:
            raise Exception(f"[FALHA]: Ao manipular os arquivos: {e}")
