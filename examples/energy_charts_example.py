from energy_data_parser.energy_charts import EnergyChartsParser, Country

parser = EnergyChartsParser()
df_generation = parser.fetch_generation(
    country=Country.AUSTRIA,
    start_date="2023-01-01",
    end_date="2023-01-31"
)
print(df_generation.head())