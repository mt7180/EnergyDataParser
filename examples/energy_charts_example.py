from energy_data_parser.energy_charts import EnergyChartsParser, Country

parser = EnergyChartsParser()


def fetch_all(country_str, start_date, end_date):
    """Fetch all data for a specific country and date range."""
    
    data = {}

    country = EnergyChartsParser.get_country(country_str)
    data["generation"] = parser.fetch_generation(
        country=country, start_date=start_date, end_date=end_date
    )
    data["installed_power"] = parser.fetch_installed_power(
        country=country,
    )
    data["public_power"] = parser.fetch_total_power(
        country=country, start_date=start_date, end_date=end_date
    )
    return data


if __name__ == "__main__":
    print("Energy Charts Example")
    start_date="2023-01-01"
    end_date="2023-12-31"
    data = fetch_all("germany", start_date, end_date)
    for name, df in data.items():
        print(f"-------{name}-----")
        print(df.head())
