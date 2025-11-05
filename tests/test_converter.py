from src.modules.convert import Converter


def test_format_date_handles_known_patterns():
    assert Converter.format_date("02/03/2024") == "02/03/2024"
    assert Converter.format_date("02-03-2024") == "02/03/2024"
    assert Converter.format_date("2024-03-02") == "02/03/2024"
    assert Converter.format_date("2024/03/02") == "02/03/2024"


def test_format_date_unknown_pattern_returns_false():
    assert Converter.format_date("2024.03.02") is False


def test_convert_date_to_string_first_day_of_month():
    assert Converter.convert_date_to_string_first_day_of_month("Jan/2024") == "01/01/2024"


def test_convert_date_to_string_last_day_of_month():
    assert Converter.convert_date_to_string_last_day_of_month("Fev/2024") == "29/02/2024"


def test_convert_date_to_year_month_returns_human_readable_month():
    ano, mes = Converter.convert_date_to_year_month("Mar/2024")
    assert ano == 2024
    assert mes == "Marco"


def test_convert_month_returns_full_name():
    assert Converter.convert_month("Abr/2025") == "Abril/2025"


@staticmethod
def convert_date_to_string_last_day_of_month(valor):
    # Convert Portuguese month abbreviation to English
    mes_abrev, ano = valor.split("/")
    mes_abrev_lower = mes_abrev.lower()

    # Map Portuguese abbreviations to English
    meses_abreviados = {"jan": "jan", "fev": "feb", "mar": "mar", "abr": "apr", "mai": "may", "jun": "jun", "jul": "jul", "ago": "aug", "set": "sep", "out": "oct", "nov": "nov", "dez": "dec"}

    mes_en = meses_abreviados.get(mes_abrev_lower, mes_abrev_lower)
    valor_en = f"{mes_en}/{ano}"

    data = datetime.strptime(valor_en, "%b/%Y")
    ultimo_dia = calendar.monthrange(data.year, data.month)[1]
    return data.replace(day=ultimo_dia).strftime("%d/%m/%Y")
