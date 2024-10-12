import pandas as pd

# Load consumption data
consumption_df = pd.read_csv('data/domestic-consumption.csv', index_col='domestic_consumption')

# Load population data
population_df = pd.read_csv('data/country-population-ranged.csv')

# Pivot population data to match consumption format
population_pivot = population_df.pivot(index='Country', columns='Year', values='Population')
population_pivot.columns = population_pivot.columns.astype(str)  # Ensure year columns are strings

# Get common countries and years
common_countries = consumption_df.index.intersection(population_pivot.index)
common_years = ['1990', '2018']  # Specify the desired years

# Filter dataframes
consumption_filtered = consumption_df.loc[common_countries, common_years]
population_filtered = population_pivot.loc[common_countries, common_years].astype(int)

# Calculate per capita consumption (in kg)
per_capita_df = (consumption_filtered * 60) / population_filtered  # Corrected calculation

# --- Filtering Logic (insert here) ---
# Pivot to check for zero consumption in both years
per_capita_pivot = per_capita_df.copy().melt(ignore_index=False, var_name='Year', value_name='Consumption')
per_capita_pivot = per_capita_pivot.reset_index().pivot(index='Country', columns='Year', values='Consumption')

countries_to_remove = per_capita_pivot[(per_capita_pivot['1990'] == 0) & (per_capita_pivot['2018'] == 0)].index
per_capita_df = per_capita_df[~per_capita_df.index.isin(countries_to_remove)] # Applying filter to the per_capita_df



# Melt the per capita dataframe for desired output format
per_capita_melted = per_capita_df.melt(ignore_index=False, var_name='Year', value_name='Consumption')
per_capita_melted = per_capita_melted.rename_axis('Country').reset_index()



# Save to CSV
per_capita_melted.to_csv('data/per_capita_consumption_1990_2018_2.csv', index=False)

print(per_capita_melted)