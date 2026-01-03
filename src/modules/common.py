import json
import logging
import sys
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Union


def get_message() -> Dict[str, Any]:
    """
    Lê a mensagem de entrada via stdin (formato JSON).

    Returns:
        Dict[str, Any]: Payload convertido em dicionário.
    """
    return json.loads(sys.stdin.read())


def time_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorador que calcula o tempo de execução da função decorada.

    Args:
        func (Callable): Função a ser medida.

    Returns:
        Callable: Função decorada.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = datetime.now()
        logging.info("Execução iniciada às %s", start_time.strftime("%H:%M:%S"))

        result = func(*args, **kwargs)

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        logging.info("Execução finalizada às %s", end_time.strftime("%H:%M:%S"))
        logging.info(
            "Tempo total: %02d hora(s), %02d minuto(s) e %02d segundo(s)",
            int(hours),
            int(minutes),
            int(seconds),
        )

        return result

    return wrapper


def attempts(
    max_attempts: int = 3, waiting_time: Union[int, float] = 1
) -> Callable[..., Any]:
    """
    Decorador que tenta executar a função decorada um número limitado de vezes.

    Args:
        max_attempts (int): Número máximo de tentativas. Padrão: 3.
        waiting_time (Union[int, float]): Intervalo em segundos entre as tentativas. Padrão: 1.

    Returns:
        Callable: Função decorada.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 1
            while attempt <= max_attempts:
                try:
                    logging.info("Tentativa %d de %d.", attempt, max_attempts)
                    return func(*args, **kwargs)
                except Exception as exc:
                    logging.info(
                        "Tentativa %d de %d falhou. Erro: %s - %s",
                        attempt,
                        max_attempts,
                        type(exc).__name__,
                        exc,
                    )
                    attempt += 1
                    time.sleep(waiting_time)
            raise RuntimeError(
                f"Não foi possível concluir após {max_attempts} tentativas."
            )

        return wrapper

    return decorator
