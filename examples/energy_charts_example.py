from energy_data_parser.energy_charts import EnergyChartsParser, Country

parser = EnergyChartsParser()


def fetch_generation_data():
    """Fetch generation data for a specific country and date range."""
    df_generation = parser.fetch_generation(
        country=Country.GERMANY, start_date="2023-01-01", end_date="2023-12-31"
    )
    return df_generation


if __name__ == "__main__":
    print("Energy Charts Example")
    df_generation = fetch_generation_data()
    print(df_generation.head())
