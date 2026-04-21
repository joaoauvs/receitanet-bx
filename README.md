# ReceitaNet BX — Robô de Automação SPED

Robô de automação desktop para download de arquivos **SPED** (Sistema Público de Escrituração Digital) via o aplicativo **Receitanet BX** da Receita Federal.

Utiliza reconhecimento de imagem (OpenCV) e automação de teclado/mouse (PyAutoGUI + PyWinAuto) para interagir com a interface gráfica do aplicativo e baixar automaticamente os arquivos solicitados.

## Tipos de SPED suportados

| Tipo | Sigla | Descrição |
|------|-------|-----------|
| `SPED Fiscal` | EFD ICMS/IPI | Escrituração Fiscal Digital |
| `SPED Contribuicoes` | EFD Contribuições | PIS/COFINS |
| `SPED Contabil` | ECD | Escrituração Contábil Digital |
| `SPED ECF` | ECF | Escrituração Contábil Fiscal |

## Pré-requisitos

- **Sistema Operacional:** Windows 10/11 (obrigatório — o Receitanet BX só roda no Windows)
- **Python:** 3.8 ou superior
- **Receitanet BX 1.9.24** instalado em `C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Programas RFB/Receitanet BX/`
- **Certificado digital A1** instalado e válido
- **OneDrive** sincronizado em `~/OneDrive - Alianzo/` (diretório de saída dos arquivos)

## Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd receitanet-bx

# 2. Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

## Uso

O robô lê os parâmetros via **stdin** no formato JSON:

```bash
echo '{"Cnpj": "00.000.000/0001-00", "Sistema": "SPED Fiscal", "DataInicial": "01/01/2024", "DataFinal": "31/12/2024"}' | python main.py
```

### Esquema do payload

```json
{
  "Cnpj": "00.000.000/0001-00",
  "Sistema": "SPED Fiscal",
  "DataInicial": "01/01/2024",
  "DataFinal": "31/12/2024"
}
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Cnpj` | string | CNPJ do contribuinte (com ou sem formatação) |
| `Sistema` | string | Um dos quatro tipos suportados (ver tabela acima) |
| `DataInicial` | string | Data de início — formatos aceitos: `DD/MM/AAAA`, `AAAA-MM-DD`, `DD-MM-AAAA` |
| `DataFinal` | string | Data de fim — mesmos formatos |

> As chaves aceitam tanto `PascalCase` (`Cnpj`) quanto `lowercase` (`cnpj`).

## Arquitetura

```
receitanet-bx/
├── main.py              # Ponto de entrada — Bot (orquestrador)
├── receitanet.py        # ReceitaNetBx — interação com a UI do aplicativo
├── sped.py              # Sped — rotinas de download por tipo de SPED
│
└── src/
    ├── base/
    │   ├── bot.py       # BaseBot (classe base abstrata)
    │   └── state.py     # State / SingleState (singleton de estado)
    │
    ├── core/
    │   ├── bot.py       # DesktopBot — motor de automação (imagem, mouse, teclado)
    │   ├── cv2find.py   # Detecção de imagem via OpenCV
    │   └── application/ # Integração PyWinAuto
    │
    ├── modules/
    │   ├── common.py    # Decoradores: @time_execution, @attempts
    │   ├── convert.py   # Converter — conversão de datas
    │   ├── data.py      # Data — formatação de datas
    │   ├── exceptions.py# Hierarquia de exceções do domínio
    │   ├── file.py      # File — operações de arquivo
    │   ├── log.py       # LogManager — gerenciamento de logs diários
    │   ├── types.py     # SpedType (enum) — constantes do domínio
    │   └── validate.py  # Validar — CNPJ, datas, campos
    │
    └── images/          # Templates PNG para reconhecimento de UI (~100 imagens)
        ├── login/
        ├── baixa/
        ├── combobox-sistemas/
        ├── combobox-arquivos/
        ├── combobox-periodos/
        ├── sped-fiscal/
        └── pop-ups/
```

### Hierarquia de classes

```
BaseBot
  └── DesktopBot          # motor de automação (find, click, type, etc.)
        ├── ReceitaNetBx  # UI do Receitanet BX (login, seleção, download)
        └── Sped          # orquestra downloads por tipo de SPED

Bot                       # orquestrador principal (sem herança de DesktopBot)
```

### Hierarquia de exceções

```
SpedError
  ├── LoginError       # falha no login com certificado
  ├── DownloadError    # falha no download ou manipulação de arquivos
  ├── ValidationError  # dados de entrada inválidos
  └── UIError          # elemento de interface não encontrado
```

## Fluxo de execução

```
stdin (JSON)
    ↓ Bot.main()
    ├─ Valida CNPJ e datas
    ├─ Resolve SpedType pelo nome normalizado
    ↓ ReceitaNetBx.login()
    ├─ Abre o aplicativo
    ├─ Seleciona certificado A1
    ├─ Faz login com CNPJ
    ↓ Sped.process_download()
    ├─ Seleciona sistema, arquivo e período
    ├─ Insere datas nos campos
    ├─ Pesquisa / solicita arquivos
    ├─ Valida popup de resultado
    ├─ Baixa os arquivos
    └─ Move para ~/OneDrive - Alianzo/ReceitaNet-Bx/{CNPJ}/{tipo}/
```

## Logs

Os logs são gerados diariamente no diretório `logs/` com o formato `DD-MM-AAAA.log`.

```
logs/
└── 20-04-2026.log
```

## Reconhecimento de imagem

O robô usa templates PNG em `src/images/` para localizar elementos da UI. Se a detecção falhar, verifique:

1. A **resolução de tela** corresponde às imagens capturadas (1920×1080 recomendado)
2. O **tema do Windows** não foi alterado
3. A versão do **Receitanet BX** é a 1.9.24

Para recapturar imagens, faça screenshots dos elementos e substitua os arquivos correspondentes em `src/images/`.

## Modo de desenvolvimento

Em `main.py`, altere `DEVELOP_MODE = True` para usar um payload fixo sem ler do stdin:

```python
DEVELOP_MODE = True  # usa o payload hardcoded para testes locais
```

## Testes

```bash
python -m pytest tests/ -v
```

Os testes unitários cobrem os módulos utilitários (`validate`, `data`, `convert`, `common`).

## Dependências principais

| Pacote | Uso |
|--------|-----|
| `opencv-python` | Reconhecimento de imagem por template matching |
| `pyautogui` | Automação de mouse e teclado |
| `pywinauto` | Interação com janelas Win32 |
| `pillow` | Manipulação de imagens / screenshots |
| `pandas` | Processamento de dados (módulos auxiliares) |

Lista completa em `requirements.txt`.

## Licença

Projeto de uso interno. Consulte a política da sua organização antes de redistribuir.
