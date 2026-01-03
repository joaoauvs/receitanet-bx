# Bot de Automação ReceitaNet BX

Este projeto é um robô de automação para o aplicativo **Receitanet BX**, projetado para baixar arquivos SPED (Sistema Público de Escrituração Digital), tais como:

*   SPED Fiscal (EFD ICMS/IPI)
*   SPED Contribuições (EFD Contribuições)
*   SPED Contábil (ECD)
*   SPED ECF (Escrituração Contábil Fiscal)

O robô interage com o aplicativo desktop utilizando reconhecimento de imagem e automação de teclado/mouse.

## Pré-requisitos

*   **Sistema Operacional**: Windows (necessário para o Receitanet BX).
*   **Python**: 3.8 ou superior.
*   **Receitanet BX**: O aplicativo deve estar instalado e acessível.
*   **Certificado Digital**: Um certificado digital válido (A1 ou A3) deve estar instalado para acessar os arquivos.

## Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-repo/receitanet-bx-bot.git
    cd receitanet-bx-bot
    ```

2.  **Instale as dependências:**

    Recomenda-se o uso de um ambiente virtual.

    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

    *Nota: Se o `requirements.txt` estiver faltando, as principais dependências são `pyautogui`, `opencv-python` e `pillow`.*

## Configuração

O robô utiliza um conjunto de imagens para identificar elementos da interface. Estas estão localizadas em `src/images`. Certifique-se de que a resolução da tela e o tema correspondam às imagens capturadas, ou substitua-as por suas próprias capturas se a detecção falhar.

## Uso

O robô lê parâmetros de entrada via entrada padrão (stdin) no formato JSON.

**Esquema JSON:**

```json
{
  "Cnpj": "00.000.000/0000-00",
  "Sistema": "SPED Fiscal",
  "DataInicial": "01/01/2023",
  "DataFinal": "31/12/2023"
}
```

## Dicas
- Os caminhos de imagens já apontam para `src/images`. Se mover o diretório, ajuste os caminhos em `receitanet.py` e `sped.py`.
- Os logs são gerenciados por `src/modules/log.py` e gravados no diretório definido em tempo de execução.
- Para depuração, prefira executar o script com privilégios de administrador para evitar bloqueios de automação.

## Licença
Projeto de uso interno. Ajuste este trecho conforme a política da sua organização.
