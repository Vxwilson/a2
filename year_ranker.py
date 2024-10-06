import pandas as pd

# Load the data
df = pd.read_csv("data/exports-calendar-year.csv")

# Melt the dataframe to long format
df_melted = df.melt(id_vars=['exports'], var_name='year', value_name='export')

# Convert year to datetime
df_melted['year'] = pd.to_datetime(df_melted['year'], format='%Y')

# Group by year and calculate rank
def rank_within_year(group):
    group['rank'] = group['export'].rank(ascending=False)
    return group

df_ranked = df_melted.groupby('year').apply(rank_within_year)

# Filter for top 5
df_top10 = df_ranked[df_ranked['rank'] <= 5]

# Export the processed data
df_top10.to_csv("data/exports_top5_yearly.csv", index=False)