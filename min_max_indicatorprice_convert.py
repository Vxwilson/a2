import pandas as pd

# used to produce the indicator_prices_avgdiff.csv file
# used for layered area-line chart


def transform_coffee_data(filepath):

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    price_cols = ['Colombian Milds', 'Other Milds', 'Brazilian Naturals', 'Robustas']

    df['min_price'] = df[price_cols].min(axis=1)
    df['max_price'] = df[price_cols].max(axis=1)

    df['months'] = pd.to_datetime(df['months'], format='%m/%Y')

    return df[['months', 'min_price', 'max_price']]


transformed_df = transform_coffee_data('data/indicator-prices.csv')

if transformed_df is not None:
    yearly_coffee_prices = transformed_df.groupby(transformed_df['months'].dt.year).agg(
        {'min_price': ['min'], 'max_price': ['max']}  # Get min/max for both price columns
    ).reset_index()

    # Flatten the MultiIndex columns
    yearly_coffee_prices.columns = ['_'.join(col).strip() for col in yearly_coffee_prices.columns.values]
    yearly_coffee_prices.rename(columns={'months_': 'year'}, inplace=True)
    yearly_coffee_prices['year'] = pd.to_datetime(yearly_coffee_prices['year'], format='%Y')
    print(transformed_df)

    print(yearly_coffee_prices)

    yearly_coffee_prices.to_csv("data/yearly-min-max-prices.csv", index=False)

def transform_exports_data(filepath):

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    df = df.set_index('exports').T.reset_index()
    df.rename(columns={'index': 'year'}, inplace=True) #rename index col to year

    df['year'] = pd.to_datetime(df['year'], format='%Y')

    # Calculate the total exports for each year
    df['total_exports'] = df.drop('year', axis=1).sum(axis=1) 

    return df[['year', 'total_exports']]


transformed_exports = transform_exports_data('data/total-production.csv')

if transformed_exports is not None:
    transformed_exports.to_csv("data/exports-sum.csv", index=False)


# merge the two dataframes
coffee_prices = pd.read_csv('data/yearly-min-max-prices.csv')
coffee_exports = pd.read_csv('data/exports-sum.csv')

merged_df = pd.merge(coffee_prices, coffee_exports, on='year', how='inner')
merged_df.to_csv('data/merged-coffee-data.csv', index=False)
print(merged_df)

