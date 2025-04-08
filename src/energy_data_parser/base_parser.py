from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar
from logging import getLogger
import pandas as pd
import requests
from typing import Any

CountryType = TypeVar('CountryType', bound=Enum)

class _EnergyAPIBaseParser(ABC):
    """Abstract Base Class for fetching data from a specific energy data API."""
    REQUEST_URL = ""

    def __init__(self, api_key=None):
        self.api_key = api_key

    @abstractmethod
    def fetch_generation(self, country: CountryType, start_date: str, end_date: str) -> pd.DataFrame:
        pass

    # @abstractmethod
    # def fetch_total_power(self, country: CountryType, start_date: str, end_date: str) -> pd.DataFrame:
    #     pass

    # @abstractmethod
    # def fetch_installed_power(self, country: CountryType) -> pd.DataFrame:
    #     pass


    @abstractmethod
    def format_date(self, input_date)->str:
        pass

    @abstractmethod
    def make_dataframe(self, response: dict[str,Any])->pd.DataFrame:
        pass

    
    @staticmethod
    @abstractmethod
    def get_country(country: str) -> CountryType:
        pass

    @classmethod
    def query_API(cls, api_end_point, params) ->dict:
        print(f"Querying API: {cls.REQUEST_URL+api_end_point} with params: {params}")
        response = requests.get(url=cls.REQUEST_URL+api_end_point, params=params)

        if response.status_code != 200:
            logger = getLogger(__name__)
            logger.error(f"Request failed with status code {response.status_code}:{response.text}")
            return dict()
        
        return response.json()


    def fetch_all_data(self, country: str, start_date: str, end_date: str):
        """Fetch all types of energy data from a specific API for a given country and date range."""
        energy_data = {}
       
        for method_name in self.__class__.__abstractmethods__:
            if not "fetch" in method_name:
                continue
            elif not hasattr(self, method_name):
                raise NotImplementedError(f"{method_name} not implemented in {self.__class__.__name__}")
            energy_data[method_name] = getattr(self.__class__)
        return energy_data
