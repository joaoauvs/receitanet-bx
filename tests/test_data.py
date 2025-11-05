from datetime import datetime, timedelta

from src.modules.data import Data


def test_formatar_data_accepts_multiple_formats():
    assert Data.formatar_data("01/02/2024") == "01/02/2024"
    assert Data.formatar_data("01-02-2024") == "01/02/2024"
    assert Data.formatar_data("2024-02-01") == "01/02/2024"
    assert Data.formatar_data("2024/02/01") == "01/02/2024"


def test_formatar_data_invalid_string_returns_false():
    assert Data.formatar_data("2024.02.01") is False


def test_primeiro_ultimo_dia_mes_anterior_matches_expected():
    hoje = datetime.today()
    ultimo_dia_mes_anterior = hoje.replace(day=1) - timedelta(days=1)
    esperado_primeiro = ultimo_dia_mes_anterior.replace(day=1).strftime("%d/%m/%Y")
    esperado_ultimo = ultimo_dia_mes_anterior.strftime("%d/%m/%Y")

    resultado = Data.primeiro_ultimo_dia_mes_anterior()
    assert resultado == (esperado_primeiro, esperado_ultimo)


def test_primeiro_ultimo_dia_ano_anterior_matches_expected():
    ano_anterior = datetime.today().year - 1
    esperado_primeiro = f"01/01/{ano_anterior}"
    esperado_ultimo = f"31/12/{ano_anterior}"

    resultado = Data.primeiro_ultimo_dia_ano_anterior()
    assert resultado == (esperado_primeiro, esperado_ultimo)
