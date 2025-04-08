from enum import Enum
from logging import getLogger
import pandas as pd
from typing import Any

from energy_data_parser.base_parser import _EnergyAPIBaseParser

logger = getLogger(__name__)

DEFAULT_COUNTRY = "Germany"

class CountryNotYetImplementedError(Exception):
    pass

class EnergyChartsParser(_EnergyAPIBaseParser):
    """Class for fetching data from Energy Charts API"""

    REQUEST_URL = "https://api.energy-charts.info"

    class APIEndPoint(Enum):
        GENERATION = "/public_power"
        TOTAL_POWER = "/total_power"
        INSTALLED_POWER = "/installed_power"

    def __init__(self, api_key: str| None =None):
        self.time_zone="Europe/Brussels"
        self.country_code = EnergyChartsParser.get_country(DEFAULT_COUNTRY)
        super().__init__(api_key)

    @staticmethod
    def get_country(country: str) -> 'Country':
        for member in Country:
            if member.name == country.upper():
                return member
        raise CountryNotYetImplementedError(
            f"Country '{country}' not available at Energy Charts API"
        )
      
    def format_date(self, date:str|pd.Timestamp)->str:
        if not isinstance(date, (str, pd.Timestamp)):
            raise TypeError("date must be a string or pd.Timestamp")
        
        if isinstance(date, str):
            try:
                date = pd.Timestamp(date)
            except ValueError:
                raise ValueError(f"Invalid date format: {date}")
        return date.strftime('%Y-%m-%d')
    
    def fetch_generation(
            self, 
            country: 'Country', 
            start_date: str|pd.Timestamp, 
            end_date: str|pd.Timestamp,
        ) -> pd.DataFrame:
        params = {
            "country": country.value,
            "start": self.format_date(start_date),
            "end": self.format_date(end_date)
        }
        response = self.query_API(
            self.APIEndPoint.GENERATION.value, 
            params
        )

        if not response:
            return pd.DataFrame()
        #return self.make_dataframe(response)
        df = self.make_dataframe(response)
        logger.info(f"{df.head(3)},{ len(df.columns)}")
        return df
    
    
    def create_time_index(self, data: dict[str,Any]) -> pd.DatetimeIndex:
        if "unix_seconds" in data.keys():
            index = pd. DatetimeIndex(
            pd.to_datetime(
                data["unix_seconds"], unit="s", utc=True)
            ) #.tz_localize(TIME_ZONE)  
        elif "time" in data.keys():
            index = pd.DatetimeIndex(data["time"])
        else:
            raise ValueError("No time information found in data")
        return index
        
    def add_columns(self, df: pd.DataFrame, data: dict[str,Any]) -> pd.DataFrame:
        if "forecast_values" in data.keys():
            production_type = data["production_type"]
            df[production_type] = data["forecast_values"]
        elif "data" in data.keys():
            df["frequency"] = data["data"]
        
        for category in ["production_types", "countries"]:
            if category not in data:
                continue
            #print(f"data: {category}")
            for column in data[category]:
                #for name, data in obj.items():
                df[column["name"]] = column["data"]
        return df
    
    def make_dataframe(self, data: dict[str,Any]) -> pd.DataFrame:
        if not data:
            raise ValueError("data empty, no dataframe can be created")

        index = self.create_time_index(data)
        df = pd.DataFrame(index=index)
        return self.add_columns(df, data)

    
class Country(Enum):
    """country codes used in Energy Charts API"""
    # see also: https://api.energy-charts.info/#/power/total_power_total_power_get
    
    GERMANY = "de"
    SWITZERLAND = "ch"
    EUROPEAN_UNION = "eu"
    EUROPE = "all"
    ALBANIA = "al"
    ARMENIA = "am"
    AUSTRIA = "at"
    AZERBAIJAN = "az"
    BOSNIA_HERZEGOINA = "ba"
    BELGIUM = "be"
    BULGARIA = "bg"
    BELARUS = "by"
    CYPRUS = "cy"
    CZECH_REPUBLIC = "cz"
    DENMARK = "dk"
    SPAIN = "es"  
    ESTONIA = "ee"
    FINLAND = "fi"
    France = "fr"
    GEORGIA = "ge"
    CROATIA = "hr"
    GREECE = "gr"
    IRELAND = "ie"
    HUNGARY = "hu"
    ITALY = "it"
    LITHUANIa = "lt"
    LUXEMBOURG = "lu"
    LATVIA = "lv"
    MOLDOVA = "md"
    NORTH_MACEDONI = "mk"
    MONTENEGRO = "me"
    MALTA = "mt"
    NORTH_IRELAND = "nie"
    NETHERLANDS = "nl"
    NORWAY = "no"
    POLAND = "pl"
    PORTUGAL = "pt"
    ROMANIA = "ro"
    SERBIA = "rs"
    RUSSIA = "ru"
    SWEDEN = "se"
    SLOVENIA = "si"
    SLOVAK_REPUBLIC = "sk"
    TURKEY = "tr"
    UKRAINE = "ua"
    UNITED_KINGDOM = "uk"
    KOSOVO= "xk"

