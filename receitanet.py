"""Automação para interagir com o aplicativo ReceitaNet BX."""

import logging
import shutil
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from src.config.settings import Settings
from src.core.bot import DesktopBot
from src.modules.exceptions import DownloadError, LoginError, UIError


class ReceitaNetBx(DesktopBot):
    """
    Classe destinada a automatizar tarefas relacionadas ao aplicativo "ReceitaNet BX".

    Attributes:
        dir_docs (Path): Diretório padrão para documentos relacionados ao ReceitanetBX.
        nome_app (str): Nome do aplicativo.
        dir_app (Path): Caminho para o atalho do aplicativo.
        image_paths (Dict[str, Path]): Dicionário contendo os caminhos para as imagens utilizadas.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe ReceitaNetBx.
        """
        super().__init__()
        self.found = threading.Event()
        self.dir_docs = Path(Settings.RECEITANET_DOCS_DIR)
        self.nome_app = "Receitanet BX"
        self.dir_app = Path(Settings.RECEITANET_APP_PATH)

        base_dir = Path(__file__).resolve().parent
        resources_dir = base_dir / "src" / "images"

        self.dir_login = resources_dir / "login"
        self.list_btn_entrar = resources_dir / "button-entrar"
        self.certificado_alz = resources_dir / "icon-certificado-alz"
        self.certificado_auditoria = resources_dir / "icon-certificado-auditoria"
        self.select_todos = resources_dir / "selecionar-todos"
        self.dir_pop_ups = resources_dir / "pop-ups"
        self.dir_baixa = resources_dir / "baixa"
        self.dir_sped_fiscal = resources_dir / "sped-fiscal"
        self.dir_combobox_sistema = resources_dir / "combobox-sistemas"
        self.dir_combobox_arquivo = resources_dir / "combobox-arquivos"
        self.dir_combobox_periodo = resources_dir / "combobox-periodos"
        self.dir_selecione_sistema = self.dir_combobox_sistema / "selecione sistema"
        self.dir_selecione_arquivo = self.dir_combobox_arquivo / "selecione arquivo"
        self.dir_selecione_periodo = self.dir_combobox_periodo / "selecione periodo"
        self.list_btn_baixar = self.dir_baixa / "button-baixar"
        self.list_icon_marcar = self.dir_baixa / "icon-marcar"
        self.result: Optional[Dict[str, str]] = None
        self._popup_lock = threading.Lock()
        self.load_images()

    def action(self, execution=None):
        """Método exigido pela classe base (não utilizado diretamente)."""
        raise NotImplementedError("Utilize a classe Bot para orquestrar a automação.")

    def abrir_aplicativo(self) -> None:
        """
        Abre o aplicativo Receitanet BX.
        """
        logging.info("Abrindo o aplicativo > ReceitanetBX <")
        try:
            self.execute(str(self.dir_app))
            self.focus_window_app(self.nome_app)
        except Exception as exc:  # pylint: disable=broad-except
            raise UIError("Erro ao abrir o aplicativo.") from exc

    def fechar_aplicativo(self) -> None:
        """
        Fecha o aplicativo Receitanet BX.
        """
        try:
            logging.info("Fechando o aplicativo")
            subprocess.Popen("taskkill /f /im javaw.exe", shell=True)
        except Exception as exc:  # pylint: disable=broad-except
            raise UIError("Erro ao fechar o aplicativo.") from exc

    def load_images(self) -> None:
        """
        Carrega as imagens necessárias para a execução do robô.
        """
        try:
            mappings: List[Tuple[str, Path, str]] = [
                ("atualizar-lista", self.dir_login, "atualizar-lista.png"),
                ("box-buscar-todos", self.dir_sped_fiscal, "box-buscar-todos.png"),
                ("box-ultimo-arquivo", self.dir_sped_fiscal, "box-ultimo-arquivo.png"),
                ("button-pesquisar", self.dir_baixa, "button-pesquisar.png"),
                (
                    "button-solicitar-arquivos-marcados",
                    self.dir_baixa,
                    "button-solicitar-arquivos-marcados.png",
                ),
                (
                    "combobox-dados-agregados",
                    self.dir_combobox_arquivo,
                    "dados-agregados-escrituracao.png",
                ),
                (
                    "combobox-entrega",
                    self.dir_combobox_periodo,
                    "periodo-de-entrega.png",
                ),
                (
                    "combobox-entrega-da-incorporada",
                    self.dir_combobox_periodo,
                    "periodo-de-entrega-da-incorporada.png",
                ),
                (
                    "combobox-escrituracao",
                    self.dir_combobox_arquivo,
                    "escrituracao.png",
                ),
                (
                    "combobox-escrituracao-contabil-digital",
                    self.dir_combobox_arquivo,
                    "escrituracao-contabil-digital.png",
                ),
                (
                    "combobox-escrituracao-da-incorporada",
                    self.dir_combobox_periodo,
                    "periodo-de-escrituracao-da-incorporada.png",
                ),
                (
                    "combobox-escrituracao-fiscal",
                    self.dir_combobox_arquivo,
                    "escrituracao-fiscal.png",
                ),
                ("combobox-perfil", self.dir_login, "combobox-contribuinte.png"),
                (
                    "combobox-periodo-escrituracao",
                    self.dir_combobox_periodo,
                    "periodo-escrituracao.png",
                ),
                (
                    "combobox-periodo-entrega",
                    self.dir_combobox_periodo,
                    "periodo-de-entrega.png",
                ),
                ("combobox-sped-contabil", self.dir_combobox_sistema, "contabil.png"),
                (
                    "combobox-sped-contribuicoes",
                    self.dir_combobox_sistema,
                    "contribuicoes.png",
                ),
                ("combobox-sped-ecf", self.dir_combobox_sistema, "ecf.png"),
                ("combobox-sped-fiscal", self.dir_combobox_sistema, "fiscal.png"),
                (
                    "combobox-termos-junta-comercial",
                    self.dir_combobox_arquivo,
                    "termos-junta-comercial.png",
                ),
                (
                    "combobox-validacao-escrituracao",
                    self.dir_combobox_arquivo,
                    "validacao-escrituracao.png",
                ),
                ("fim-download", self.dir_baixa, "fim-download.png"),
                ("icon-acompanhamento", self.dir_baixa, "icon-acompanhamento.png"),
                ("icon-marcar", self.dir_baixa, "icon-marcar.png"),
                ("icon-pesquisa", self.dir_baixa, "icon-pesquisa.png"),
                ("input-cnjp", self.dir_sped_fiscal, "input-cnpj.png"),
                ("input-data-fim", self.dir_baixa, "data-fim.png"),
                ("input-data-fim-fiscal", self.dir_sped_fiscal, "input-data-fim.png"),
                (
                    "input-data-fim-incorporada",
                    self.dir_baixa,
                    "data-fim-incorporada.png",
                ),
                ("input-data-inicio", self.dir_baixa, "data-inicio.png"),
                (
                    "input-data-inicio-fiscal",
                    self.dir_sped_fiscal,
                    "input-data-inicio.png",
                ),
                (
                    "input-data-inicio-incorporada",
                    self.dir_baixa,
                    "data-inicio-incorporada.png",
                ),
                ("input-pf", self.dir_login, "input-cpf.png"),
                ("input-pj", self.dir_login, "input-cnpj.png"),
                ("input-procurador", self.dir_baixa, "cnpj-incorporada.png"),
                ("login-efetuado", self.dir_login, "validate-login.png"),
                ("msg-aguardando", self.dir_baixa, "msg-aguardando.png"),
                ("msg-erro-data", self.dir_baixa, "msg-erro-data.png"),
                (
                    "msg-falha-comunicacao",
                    self.dir_baixa,
                    "msg-falha-comunicacao-servidor.png",
                ),
                (
                    "msg-nao-existe-procuracao",
                    self.dir_baixa,
                    "msg-nao-existe-procuracao.png",
                ),
                (
                    "msg-procuracao-vencida",
                    self.dir_baixa,
                    "msg-procuracao-vencida.png",
                ),
                ("pop-up-error", self.dir_pop_ups, "erro.png"),
                ("pop-up-nao-encontrado", self.dir_pop_ups, "nao-encontrado.png"),
                ("pop-up-pedido", self.dir_pop_ups, "pedido.png"),
                ("popup-nenhum-arquivo", self.dir_pop_ups, "nenhum-arquivo.png"),
                ("procurador-pf", self.dir_login, "procurador-pf.png"),
                ("procurador-pj", self.dir_login, "procurador-pj.png"),
                ("resultado-pesquisa", self.dir_baixa, "resultado-pesquisa.png"),
                ("selecionar-procurador", self.dir_login, "combobox-procurador.png"),
                (
                    "validacao-periodo-contabil",
                    self.dir_combobox_periodo,
                    "validacao-periodo-contabil.png",
                ),
                (
                    "validacao-periodo-fiscal",
                    self.dir_combobox_periodo,
                    "validacao-periodo-fiscal.png",
                ),
                ("verificar-pedidos", self.dir_baixa, "verificar-pedidos.png"),
            ]

            for identifier, directory, filename in mappings:
                self.add_image(identifier, str(directory / filename))
        except Exception as exc:  # pylint: disable=broad-except
            raise UIError("Falha ao carregar imagens de referência.") from exc

    def verificar_popup(
        self,
        nome_popup: str,
        acao: str,
        log_msg: str,
        status: str,
        resultado: str,
    ) -> None:
        """
        Verifica se um popup específico existe na tela e executa uma ação.

        Args:
            nome_popup (str): Nome/identificador do popup a ser verificado.
            acao (str): Ação a ser realizada se o popup for encontrado.
            log_msg (str): Mensagem para log.
            status (str): Status da operação.
            resultado (str): Resultado da operação.
        """
        if not self.found.is_set() and self.find(nome_popup, matching=0.8):
            with self._popup_lock:
                if (
                    not self.found.is_set()
                ):  # Double check to avoid race conditions
                    self.click()
                    self.enter()
                    logging.info(log_msg)
                    self.result = {
                        "acao": acao,
                        "status": status,
                        "resultado": resultado,
                    }
                    self.found.set()  # Signals that a condition has been met

    def login(self, contribuinte: str) -> None:
        """
        Realiza o login no aplicativo Receitanet BX.

        Args:
            contribuinte (str): CNPJ do contribuinte.
        """
        max_attempts = 4
        logging.info("* INICIANDO FUNÇÃO -> LOGIN CERTIFICADO <- *")
        for _attempt in range(1, max_attempts + 1):
            try:
                self.abrir_aplicativo()
                self.load_images()
                logging.info("Realizando login com certificado A1")
                logging.info("Selecionando -> Certificado A1 <-")
                self.find_click_list_image(path=str(self.certificado_alz), match=0.7)
                logging.info(
                    "Selecionando Combo Box -> Selecione um Perfil de Acesso <-"
                )
                self.find_click_image(identifier="combobox-perfil", match=0.8)
                logging.info("Selecionando Combo Box -> Procurador <-")
                self.find_click_image(identifier="selecionar-procurador", match=0.8)
                logging.info("Procurador PJ")
                self.find_click_image(identifier="procurador-pf", match=0.8)
                logging.info("Selecionando -> Procurador PJ <-")
                self.find_click_image(identifier="procurador-pj", match=0.8)
                logging.info("Selecionando Input -> CNPJ <-")
                self.find_click_image(identifier="input-pj", match=0.8)
                logging.info("Inserindo CNPJ do Procurador")
                self.control_a()
                self.paste(contribuinte)
                self.tab()
                time.sleep(1)
                logging.info("Selecionando Botão -> Entrar <-")
                self.find_click_list_image(
                    path=str(self.list_btn_entrar), match=0.7
                )
                logging.info("Validando se o login foi efetuado")
                try:
                    if self.wait_find_image(identifier="login-efetuado", match=0.7, tempo=30):
                        self.maximize_window()
                        time.sleep(1)
                        logging.info("* LOGIN EFETUADO COM SUCESSO")
                        break
                except FileNotFoundError:
                    self.fechar_aplicativo()
                    time.sleep(2)
            except Exception as e:
                logging.warning("Erro ao logar no Receitanet BX: %s", e)
                self.fechar_aplicativo()
                time.sleep(2)
        else:
            raise LoginError(
                "[FALHA]: Ocorreu um erro ao tentar logar com certificado A1"
            )

    def selecionar_sistema(
        self, sistema: str, sistema_anterior: Optional[str] = None
    ) -> None:
        """
        Seleciona o sistema desejado.

        Args:
            sistema (str): Sistema desejado.
            sistema_anterior (Optional[str]): Sistema anterior ao desejado.
        """
        logging.info("* SELECIONANDO O SISTEMA E O TIPO DE ARQUIVO *")
        try:
            self.mudar_tela_pesquisa()
            if self.validate_list_exists(path=str(self.dir_selecione_sistema)):
                self.find_click_list_image(path=str(self.dir_selecione_sistema))
                self.click_image(sistema)
            else:
                if self.validate_exists(identifier=sistema):
                    pass
                elif sistema_anterior and self.validate_exists(
                    identifier=sistema_anterior
                ):
                    self.click_image(sistema_anterior)
                    self.click_image(sistema)
                else:
                    raise UIError(f"Erro ao selecionar sistema: {sistema}")
            logging.info("Sistema selecionado: %s", sistema)
        except UIError:
            raise
        except Exception as e:
            raise UIError("[FALHA]: Ao selecionar o sistema.") from e

    def selecionar_arquivo(
        self,
        tipo_arquivo: str,
        validacao: Optional[str] = None,
        tipo_arquivo_anterior: Optional[str] = None,
    ) -> None:
        """
        Seleciona o tipo de arquivo desejado.

        Args:
            tipo_arquivo (str): Tipo de arquivo desejado.
            validacao (Optional[str]): Tipo de arquivo de validação.
            tipo_arquivo_anterior (Optional[str]): Tipo de arquivo anterior ao desejado.
        """
        logging.info("* SELECIONANDO O TIPO DE ARQUIVO *")
        try:
            if self.validate_list_exists(path=str(self.dir_selecione_arquivo)):
                self.find_click_list_image(path=str(self.dir_selecione_arquivo))
                self.click_image(tipo_arquivo, confidence=0.8)
            else:
                logging.info("Selecionando tipo de arquivo anterior")
                if validacao and self.validate_exists(identifier=validacao):
                    pass
                elif tipo_arquivo_anterior and self.validate_exists(
                    identifier=tipo_arquivo_anterior
                ):
                    self.click_image(tipo_arquivo_anterior)
                    self.click_image(tipo_arquivo)
                else:
                    raise UIError(
                        f"Erro ao selecionar tipo de arquivo: {tipo_arquivo}"
                    )
            logging.info("Tipo de arquivo selecionado: %s", tipo_arquivo)
        except UIError:
            raise
        except Exception as e:
            raise UIError("[FALHA]: Ao selecionar o tipo de arquivo.") from e

    def selecionar_periodo(
        self, periodo: str, periodo_anterior: Optional[str] = None
    ) -> None:
        """
        Seleciona o período desejado.

        Args:
            periodo (str): Período desejado.
            periodo_anterior (Optional[str]): Período anterior ao desejado.
        """
        try:
            logging.info("Selecionando período: %s", periodo)
            if self.validate_list_exists(path=str(self.dir_selecione_periodo)):
                self.find_click_list_image(path=str(self.dir_selecione_periodo))
                self.click_image(periodo)
            else:
                if self.validate_exists(identifier=periodo):
                    pass
                elif periodo_anterior and self.validate_exists(
                    identifier=periodo_anterior
                ):
                    self.click_image(periodo_anterior, confidence=0.8)
                    self.click_image(periodo, confidence=0.8)
                else:
                    raise UIError(f"Erro ao selecionar período: {periodo}")
        except UIError:
            raise
        except Exception as e:
            raise UIError("[FALHA]: Ao selecionar o período.") from e

    def mudar_tela_pesquisa(self) -> None:
        """
        Muda para a tela de pesquisa.
        """
        try:
            self.wait_window_app(self.nome_app, extension="javaw.exe")
            self.find("icon-pesquisa", matching=0.9)
            self.click()
            self.double_click()
        except Exception as exc:
            logging.error("Erro ao alterar para tela de pesquisa: %s", exc)
            raise UIError("Falha ao alternar para a aba de pesquisa.") from exc

    def input_data(self, primeiro_dia: str, ultimo_dia: str) -> None:
        """
        Insere a data inicial e a data final.

        Args:
            primeiro_dia (str): Data inicial.
            ultimo_dia (str): Data final.
        """
        logging.info("* INICIANDO A FUNÇÃO -> INPUT DATA <- *")
        try:
            logging.info("Selecionando o Input -> Data Inicio <-")
            if self.validate_exists(identifier="input-data-inicio"):
                self.double_click()
                time.sleep(0.5)
                self.type_key(primeiro_dia)
                self.tab()
                logging.info("Selecionando o Input -> Data Fim <-")
                if self.validate_exists(identifier="input-data-fim"):
                    self.double_click()
                    time.sleep(0.5)
                    self.type_key(ultimo_dia)
                    self.enter()
                else:
                    raise UIError(f"Erro ao inserir a data final: {ultimo_dia}")
            else:
                raise UIError(f"Erro ao inserir a data inicial: {primeiro_dia}")
            logging.info("* INPUT DATA EFETUADO COM SUCESSO")
        except UIError:
            raise
        except Exception as e:
            raise UIError("[FALHA]: Ao inserir a data.") from e

    def input_incorporada(
        self, primeiro_dia: str, ultimo_dia: str, contribuinte: str
    ) -> None:
        """
        Insere a data inicial, a data final e o CNPJ da incorporada.

        Args:
            primeiro_dia (str): Data inicial.
            ultimo_dia (str): Data final.
            contribuinte (str): CNPJ da incorporada.
        """
        logging.info("* INICIANDO O INPUT DOS DADOS DA INCORPORADA *")
        try:
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
        except UIError:
            raise
        except Exception as e:
            raise UIError("[FALHA]: Ao inserir os dados da incorporada.") from e

    def input_campos_fiscais(self, primeiro_dia: str, ultimo_dia: str) -> None:
        """
        Insere a data inicial e a data final.

        Args:
            primeiro_dia (str): Data inicial.
            ultimo_dia (str): Data final.
        """
        logging.info("INSERINDO DADOS: CNPJ, DATA DE INICIO E DATA DE FIM")
        try:
            if self.validate_exists(identifier="box-buscar-todos", match=0.87):
                logging.info(
                    "Clicando no box -> Buscar Arquivos de Todos os Estabelecimentos <-"
                )
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
                            logging.info(
                                "Clicando no box -> Último Arquivo Transmitido <-"
                            )
                            self.click_image("box-ultimo-arquivo")
                            self.click_image("button-pesquisar")
                        else:
                            logging.warning(
                                "Não foi encontrado o box -> Último Arquivo Transmitido <-"
                            )
                    else:
                        raise UIError(f"Erro ao inserir a data final: {ultimo_dia}")
                else:
                    raise UIError(f"Erro ao inserir a data inicial: {primeiro_dia}")
            else:
                raise UIError(
                    "Erro ao clicar no box -> Buscar Arquivos de Todos os Estabelecimentos <-"
                )
        except UIError:
            raise
        except Exception as e:
            raise UIError("[FALHA]: Ao inserir os dados.") from e

    def validar_solicitacao(self) -> Dict[str, str]:
        """
        Valida se a solicitação foi registrada com sucesso.

        Returns:
            Dict[str, str]: Dicionário de resultados se bem-sucedido, gera DownloadError caso contrário.
        """
        # Reseta o estado antes de cada chamada para permitir reutilização da instância.
        self.found.clear()
        self.result = None

        try:
            while True:
                if not self.validate_exists(identifier="msg-aguardando"):
                    break

            popups = [
                (
                    "msg-falha-comunicacao",
                    False,
                    "Falha na comunicação com o sistema do Receita Net!",
                    "Falha",
                    "Falha na comunicação com o sistema do Receita Net!",
                ),
                (
                    "pop-up-pedido",
                    True,
                    "Pedido Registrado Com Sucesso",
                    "Processando...",
                    "Pedido Registrado Com Sucesso!",
                ),
                (
                    "pop-up-error",
                    False,
                    "Erro ao registrar o pedido",
                    "Falha",
                    "Erro ao registrar o pedido!",
                ),
                (
                    "pop-up-nao-encontrado",
                    False,
                    "Não foi encontrado nenhum arquivo correspondente a pesquisa!",
                    "Processado",
                    "Não foi localizado nenhum arquivo!",
                ),
                (
                    "popup-nenhum-arquivo",
                    False,
                    "Não foi encontrado nenhum arquivo correspondente a pesquisa!",
                    "Processado",
                    "Não foi localizado nenhum arquivo!",
                ),
                (
                    "msg-erro-data",
                    False,
                    "A Data final deve ser igual ou menor que a data atual!",
                    "Falha",
                    "A Data final deve ser igual ou menor que a data atual!",
                ),
                (
                    "msg-procuracao-vencida",
                    False,
                    "A procuração está vencida!",
                    "Falha",
                    "Procuração eletrônica vencida!",
                ),
                (
                    "msg-nao-existe-procuracao",
                    False,
                    "Não existe procuração para este CNPJ!",
                    "Falha",
                    "Sem procuração para este CNPJ!",
                ),
            ]

            threads = []
            for popup in popups:
                thread = threading.Thread(
                    target=self.verificar_popup,
                    args=(popup[0], popup[1], popup[2], popup[3], popup[4]),
                )
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            if self.found.is_set() and self.result:
                return self.result
            raise DownloadError("Nenhuma condição de popup foi satisfeita")
        except DownloadError:
            raise
        except Exception as e:
            raise DownloadError("Erro ao validar a solicitação.") from e

    def baixar_arquivos(self) -> None:
        """
        Faz o download dos arquivos solicitados.
        """
        logging.info("* INICIANDO A FUNÇÃO -> BAIXAR ARQUIVOS <- *")
        try:
            logging.info("Selecionando o Icon -> ACOMPANHAMENTO <-")
            self.find_click_image(identifier="icon-acompanhamento", match=0.9)
            # logging.info("Selecionando o Icon -> VER PEDIDOS E ARQUIVOS <-")
            # self.find_click_image(identifier="verificar-pedidos", match=0.9)
            logging.info("Selecionando o Box do Pedido")
            self.find_click_list_image(
                path=str(self.list_icon_marcar), match=0.7, max_attempts=10
            )
            # time.sleep(20)
            logging.info("Selecionando o Box de Selecionar Todos")
            self.find_click_list_image(
                path=str(self.select_todos), match=0.9, max_attempts=10
            )
            # time.sleep(90)
            logging.info("Selecionando o Button -> Baixar <-")
            self.find_click_list_image(
                path=str(self.list_icon_marcar), match=0.7, max_attempts=10
            )
            self.find_click_list_image(
                path=str(self.list_btn_baixar), match=0.7, max_attempts=10
            )
            while True:
                if self.find("fim-download", matching=0.90):
                    logging.info("Download Finalizado")
                    break
        except DownloadError:
            raise
        except Exception as e:
            raise DownloadError("[FALHA]: Ao baixar os arquivos.") from e

    def _to_datetime(self, date_str: str, time_str: str) -> datetime:
        """
        Converte strings de data e hora para objeto datetime.

        Args:
            date_str (str): String da data no formato DD/MM/YYYY.
            time_str (str): String do horário no formato HH:MM:SS.

        Returns:
            datetime: Objeto datetime criado a partir das strings.
        """
        return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")

    def _buscar_arquivos_recentes(
        self, tipo: str
    ) -> Dict[str, Tuple[datetime, str]]:
        """
        Busca os arquivos mais recentes por período no diretório de documentos.

        Args:
            tipo (str): Tipo de arquivo SPED (Contribuições, ECF, etc.).

        Returns:
            Dict[str, Tuple[datetime, str]]: Dicionário com períodos como chaves e tuplas de (datetime, nome_arquivo) para os arquivos mais recentes.
        """
        arquivos_recentes_por_periodo: Dict[str, Tuple[datetime, str]] = {}
        for arquivo in self.dir_docs.rglob("*.txt"):
            transmissao_dia: Optional[str] = None
            transmissao_hora: Optional[str] = None
            periodo: Optional[str] = None

            if "Contribuições" in tipo:
                itens = arquivo.stem.split("_")
                if len(itens) > 5:
                    periodo = f"{itens[1][4:6]}/{itens[1][:4]}"
                    transmissao_dia = f"{itens[5][6:8]}/{itens[5][4:6]}/{itens[5][:4]}"
                    transmissao_hora = (
                        f"{itens[5][8:10]}:{itens[5][10:12]}:{itens[5][12:]}"
                    )
            elif "ECF" in tipo:
                itens = arquivo.stem.split("-")
                if len(itens) > 4:
                    transmissao_dia = f"{itens[4][6:8]}/{itens[4][4:6]}/{itens[4][:4]}"
                    transmissao_hora = (
                        f"{itens[4][8:10]}:{itens[4][10:12]}:{itens[4][12:14]}"
                    )
                    periodo = f"{itens[3][4:6]}/{itens[3][:4]}"
            else:
                continue

            if not all([transmissao_dia, transmissao_hora, periodo]):
                continue

            # Ensure they are strings for mypy, though 'all' check does it logically
            if transmissao_dia and transmissao_hora and periodo:
                data_hora_atual = self._to_datetime(transmissao_dia, transmissao_hora)

                if (
                    periodo not in arquivos_recentes_por_periodo
                    or data_hora_atual > arquivos_recentes_por_periodo[periodo][0]
                ):
                    arquivos_recentes_por_periodo[periodo] = (
                        data_hora_atual,
                        arquivo.name,
                    )
        return arquivos_recentes_por_periodo

    def manipular_arquivos(self, tipo: str, contribuinte: str) -> None:
        """
        Move o arquivo transmitido mais recentemente para a pasta de destino e exclui os demais.

        Args:
            tipo (str): Tipo de arquivo.
            contribuinte (str): CNPJ do contribuinte.
        """
        logging.info("* INICIANDO A FUNÇÃO -> MANIPULAR ARQUIVOS <- *")
        try:
            diretorio = Path(Settings.RECEITANET_ONEDRIVE_DIR) / contribuinte / tipo
            diretorio.mkdir(parents=True, exist_ok=True)

            if "Contribuicoes" in tipo or "ECF" in tipo:
                arquivos_recentes_por_periodo = self._buscar_arquivos_recentes(tipo)

                for _periodo, (
                    _data_hora_atual,
                    arquivo_nome,
                ) in arquivos_recentes_por_periodo.items():
                    shutil.move(
                        str(self.dir_docs / arquivo_nome),
                        str(diretorio / arquivo_nome),
                    )
            else:
                for arquivo in self.dir_docs.rglob("*"):
                    if arquivo.is_file():
                        shutil.move(str(arquivo), str(diretorio / arquivo.name))
            logging.info("* ARQUIVOS MOVIDOS COM SUCESSO *")
        except DownloadError:
            raise
        except Exception as e:
            raise DownloadError("[FALHA]: Ao manipular os arquivos.") from e
