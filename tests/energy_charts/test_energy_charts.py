import pytest
import pandas as pd

from energy_data_parser.energy_charts import EnergyChartsParser, Country


@pytest.fixture
def parser():
    return EnergyChartsParser()

def test_parser_initialization(parser):
    assert isinstance(parser, EnergyChartsParser)

def test_parser_fetch_generation(parser):
    country = Country.GERMANY
    start_date = pd.Timestamp("2023-01-01")
    end_date = pd.Timestamp("2023-12-31")
    
    df = parser.fetch_generation(country, start_date, end_date)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    #assert 
