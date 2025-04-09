import pytest
import pandas as pd

from energy_data_parser.energy_charts import (
    EnergyChartsParser, 
    Country, 
    CountryNotYetImplementedError
)


@pytest.fixture
def parser():
    return EnergyChartsParser()


@pytest.fixture
def mocked_parser(mocker):
    parser = EnergyChartsParser()

    mocker.patch.object(
        parser,
        "query_API",
        return_value={
            "unix_seconds": [1672531200, 1672534800],
            "production_types": [
                {"name": "solar", "data": [100, 200]},
                {"name": "wind", "data": [300, 400]},
            ],
        },
    )
    return parser


def test_parser_initialization(parser):
    assert isinstance(parser, EnergyChartsParser)


def test_fetch_generation_with_mocked_api(mocked_parser):
    country = Country.GERMANY
    start_date = pd.Timestamp("2023-01-01")
    end_date = pd.Timestamp("2023-12-31")

    df = mocked_parser.fetch_generation(country, start_date, end_date)

    mocked_parser.query_API.assert_called_once_with(
        "/public_power",
        {
            "country": "de",
            "start": "2023-01-01",
            "end": "2023-12-31",
        },
    )

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape == (2, 2)
    assert "solar" in df.columns
    assert "wind" in df.columns
    assert list(df["solar"]) == [100, 200]
    assert list(df["wind"]) == [300, 400]

def test_get_country(parser):
    country_code = "germany"
    country = parser.get_country(country_code)
    assert country == Country.GERMANY

    country_code = "invalid_country_code"
    with pytest.raises(CountryNotYetImplementedError):
        parser.get_country(country_code)

def test_get_country_wrong_country_type(parser):
    with pytest.raises(TypeError):
        parser.get_country(Country.GERMANY)  # type: ignore

def test_format_date(parser):
    date_str = "2023-01-01"
    date_timestamp = pd.Timestamp(date_str)
    formatted_date_str = parser.format_date(date_str)
    formatted_date_timestamp = parser.format_date(date_timestamp)

    assert formatted_date_str == date_timestamp.strftime("%Y-%m-%d")
    assert formatted_date_timestamp == date_timestamp.strftime("%Y-%m-%d")

def test_format_wrong_date_type(parser):
    with pytest.raises(TypeError):
        parser.format_date(12345)  # type: ignore
    with pytest.raises(ValueError):
        parser.format_date("invalid_date")


