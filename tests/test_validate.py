from src.modules.validate import Validar


def test_validar_dicionario_returns_true_when_all_fields_present():
    mensagem = {"a": 1, "b": "valor"}
    assert Validar.validar_dicionario(mensagem) is True


def test_validar_dicionario_returns_false_when_field_missing():
    mensagem = {"a": 1, "b": ""}
    assert Validar.validar_dicionario(mensagem) is False


def test_retornar_campos_vazios_lists_empty_fields():
    mensagem = {"a": "", "b": None, "c": "ok"}
    assert Validar.retornar_campos_vazios(mensagem) == ["a", "b"]


def test_validar_cnpj_returns_numeric_string_for_valid_document():
    assert Validar.validar_cnpj("44.616.568/0001-07") == "44616568000107"


def test_validar_cnpj_returns_false_for_invalid_document():
    assert Validar.validar_cnpj("11.111.111/1111-11") is False
    assert Validar.validar_cnpj("123") is False


def test_is_start_date_greater_than_end_date():
    assert (
        Validar.is_start_date_greater_than_end_date("01/01/2024", "31/01/2024") is True
    )
    assert (
        Validar.is_start_date_greater_than_end_date("31/01/2024", "01/01/2024") is False
    )
