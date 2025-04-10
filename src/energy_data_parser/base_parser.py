from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic
from logging import getLogger
import pandas as pd
import requests
from typing import Any
import aiohttp
import asyncio

CountryType = TypeVar("CountryType", bound=Enum)


class _EnergyAPIBaseParser(ABC, Generic[CountryType]):
    """Abstract Base Class for fetching data from a specific energy data API."""

    REQUEST_URL = ""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    @abstractmethod
    def fetch_generation(
        self, country: CountryType, start_date: str, end_date: str
    ) -> pd.DataFrame:
        pass

    # @abstractmethod
    # def fetch_total_power(self, country: CountryType, start_date: str, end_date: str) -> pd.DataFrame:
    #     pass

    # @abstractmethod
    # def fetch_installed_power(self, country: CountryType) -> pd.DataFrame:
    #     pass

    @abstractmethod
    def format_date(self, input_date: str | pd.Timestamp) -> str:
        pass

    @abstractmethod
    def make_dataframe(self, response: dict[str, Any]) -> pd.DataFrame:
        pass

    @classmethod
    @abstractmethod
    def get_country(cls, country: str) -> CountryType:
        pass

    @classmethod
    def query_API(cls, api_end_point: str, params: dict[str, str]) -> dict:
        url = cls.REQUEST_URL + api_end_point
        print(f"Querying API: {url} with params: {params}")
        
        response = requests.get(url, params=params)

        if response.status_code != 200:
            logger = getLogger(__name__)
            logger.error(
                f"Request failed with status code {response.status_code}:{response.text}"
            )
            return dict()

        return response.json()
    
    @classmethod
    async def async_query_API(cls, session, api_end_point: str, params: dict[str, str]) -> dict:

        url = cls.REQUEST_URL + api_end_point
        async with session.get(url, params=params) as response:
            json_body = await response.json()
            if response.status != 200:
                logger = getLogger(__name__)
                logger.error(
                    f"Request failed with status code {response.status}:{json_body}"
                )
                return dict()
            return json_body
            