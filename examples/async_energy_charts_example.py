import asyncio
from logging import getLogger
import aiohttp
import pandas as pd
from energy_data_parser.energy_charts import EnergyChartsParser, Country

parser = EnergyChartsParser()
logger = getLogger(__name__)


async def fetch(
    session: aiohttp.ClientSession,
    country: Country,
    endpoint: EnergyChartsParser.APIEndPoint,
    start_date: None | str | pd.Timestamp = None,
    end_date: None | str | pd.Timestamp = None,
) -> dict[str, str]:
    params = {"country": country.value}
    if start_date and end_date:
        params["start"] = parser.format_date(start_date)
        params["end"] = parser.format_date(end_date)
    data = await parser.async_query_API(session, endpoint.value, params=params)

    return data


async def async_fetch_generation(
    session: aiohttp.ClientSession,
    country: Country,
    start_date: str | pd.Timestamp,
    end_date: str | pd.Timestamp,
) -> pd.DataFrame:
    return await parser.async_fetch_data(
        session=session,
        country=country,
        endpoint=parser.get_endpoint("generation"),
        start_date=start_date,
        end_date=end_date,
    )


async def main():
    print("Energy Charts Async Example")
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    data = {}
    countries = ["germany", "belgium", "france", "netherlands"]
    async with aiohttp.ClientSession() as session:
        tasks = [
            async_fetch_generation(
                session, parser.get_country(country), start_date, end_date
            )
            for country in countries
        ]
        results = await asyncio.gather(*tasks)
        for country, result in zip(countries, results):
            data[country] = result
            print(f"-------{country}-----")
            print(result.head())
    return data


if __name__ == "__main__":
    asyncio.run(main())
