import json
import logging
import sys
import time
from datetime import datetime
from functools import wraps


def get_message() -> dict:
    """
    Le a mensagem de entrada via stdin (formato JSON).

    Returns:
        dict: Payload convertido em dicionario.
    """
    return json.loads(sys.stdin.read())


def time_execution(func):
    """
    Calcula o tempo de execucao da funcao decorada.

    Args:
        func (callable): Funcao a ser medida.

    Returns:
        callable: Funcao decorada.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logging.info("Execucao iniciada as %s", start_time.strftime("%H:%M:%S"))

        result = func(*args, **kwargs)

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        logging.info("Execucao finalizada as %s", end_time.strftime("%H:%M:%S"))
        logging.info(
            "Tempo total: %02d hora(s), %02d minuto(s) e %02d segundo(s)",
            int(hours),
            int(minutes),
            int(seconds),
        )

        return result

    return wrapper


def attempts(max_attempts=3, waiting_time=1):
    """
    Tenta executar a funcao decorada com numero limitado de tentativas.

    Args:
        max_attempts (int): Numero maximo de tentativas.
        waiting_time (int | float): Intervalo em segundos entre as tentativas.

    Returns:
        callable: Funcao decorada.
    """

    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tentativa = 1
            while tentativa <= max_attempts:
                try:
                    logging.info("Tentativa %d de %d.", tentativa, max_attempts)
                    return func(*args, **kwargs)
                except Exception as exc:
                    logging.info(
                        "Tentativa %d de %d falhou. Erro: %s - %s",
                        tentativa,
                        max_attempts,
                        type(exc).__name__,
                        exc,
                    )
                    tentativa += 1
                    time.sleep(waiting_time)
            raise RuntimeError(
                f"Nao foi possivel concluir apos {max_attempts} tentativas."
            )

        return wrapper

    return decorador
