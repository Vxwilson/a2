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

print(consumption_filtered)

print("---------------------------------")

print(population_pivot)
population_filtered = population_pivot.loc[common_countries, common_years].astype(int) # Ensure population is integer type


# Calculate per capita consumption

# original consumption data: 
# consumption is in thousands of 60kg bags
# population in thousands

# so we need to divide consumption by population to get per capita consumption
per_capita_df = consumption_filtered / population_filtered * 60  # Multiply by 60 to get per capita consumption in kg

per_capita_melted = per_capita_df.melt(ignore_index=False, var_name='Year', value_name='Consumption')
per_capita_melted = per_capita_melted.rename_axis('Country').reset_index()

# remove rows where consumption is 0 for both years


# Save to CSV
per_capita_melted.to_csv('data/per_capita_consumption_1990_2018.csv', index=False)

print(per_capita_melted)