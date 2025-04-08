import pytest
import pandas as pd

from energy_data_parser.energy_charts import EnergyChartsParser, Country


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

def test_fetch_generation_with_mocked_api(mocked_parser, mocker):

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
