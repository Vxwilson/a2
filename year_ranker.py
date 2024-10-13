import pandas as pd

# used to produce the exports_top5_yearly.csv file

df = pd.read_csv("data/exports-calendar-year.csv")
df_melted = df.melt(id_vars=['exports'], var_name='year', value_name='export')
df_melted['year'] = pd.to_datetime(df_melted['year'], format='%Y')

def rank_within_year(group):
    group['rank'] = group['export'].rank(ascending=False)
    return group

df_ranked = df_melted.groupby('year').apply(rank_within_year)

# Filter for top 5
df_top5 = df_ranked[df_ranked['rank'] <= 5]

df_top5.to_csv("data/exports_top5_yearly.csv", index=False)