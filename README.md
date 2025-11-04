# ReceitaNet BX Bot

Automacao em Python para baixar arquivos do aplicativo **ReceitaNet BX** de forma assistida.
O robo manipula a interface utilizando o framework BotCity e mantem um fluxo de logs
e arquivos organizados na pasta `Documents/Arquivos ReceitanetBX` do usuario.

## Pre-requisitos
- Windows 10 ou superior (64 bits).
- Python 3.10+ instalado e disponivel no `PATH`.
- Aplicativo **Receitanet BX** instalado na maquina (o atalho padrao e utilizado).
- Conta com certificado digital previamente configurado no Receitanet BX.

## Instalacao
1. Crie e ative um ambiente virtual (recomendado):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Instale as dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

## Uso
O robo le os parametros da execucao via `stdin` (formato JSON). Um exemplo completo:

```json
{
  "Cnpj": "44.616.568/0001-07",
  "Sistema": "SPED Contribuicoes",
  "DataInicial": "01/01/2024",
  "DataFinal": "31/01/2024"
}
```

Execute o robo redirecionando o JSON:

```powershell
type mensagem.json | python main.py
```

Durante o desenvolvimento voce pode ativar o modo interno alterando `DEVELOP_MODE = True`
em `main.py`. Quando ativado, uma mensagem de exemplo definida no codigo e utilizada e
nao e necessario enviar JSON pelo `stdin`.

## Estrutura do Projeto
- `main.py`: ponto de entrada do robo e orquestracao das execucoes.
- `receitanet.py`: automacoes de interface especificas do aplicativo Receitanet BX.
- `sped.py`: fluxo de download para cada modalidade de SPED.
- `src/modules`: utilitarios e servicos auxiliares (datas, arquivos, validacoes, logs).
- `src/images`: imagens utilizadas para localizar elementos na interface.
- `logs/`: diretorio criado automaticamente para armazenar arquivos de log (quando configurado).

## Dicas
- Os caminhos de imagens ja apontam para `src/images`. Se mover o diretorio, ajuste os
  caminhos em `receitanet.py` e `sped.py`.
- Os logs sao gerenciados por `src/modules/log.py` e gravados no diretorio definido
  em tempo de execucao.
- Para depuracao, prefira executar o script com privilegios de administrador para
  evitar bloqueios de automacao.

## Licenca
Projeto de uso interno. Ajuste este trecho conforme a politica da sua organizacao.
