import pandas as pd

def transform_coffee_data(filepath):
    """
    Transforms coffee price data to find min and max prices for each month.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A pandas DataFrame with 'months', 'min_price', and 'max_price' columns.
    """

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    # Select relevant columns for min/max calculation
    price_cols = ['Colombian Milds', 'Other Milds', 'Brazilian Naturals', 'Robustas']
    
    # Calculate min and max prices for each row (month)
    df['min_price'] = df[price_cols].min(axis=1)
    df['max_price'] = df[price_cols].max(axis=1)

    df['months'] = pd.to_datetime(df['months'], format='%m/%Y')
    
    # Select and return the desired columns
    return df[['months', 'min_price', 'max_price']]



# Example usage (assuming your CSV is named 'indicator-prices.csv'):
transformed_df = transform_coffee_data('data/indicator-prices.csv')

if transformed_df is not None:
    yearly_coffee_prices = transformed_df.groupby(transformed_df['months'].dt.year).agg(
        {'min_price': ['min'], 'max_price': ['max']}  # Get min/max for both price columns
    ).reset_index()

    # Flatten the MultiIndex columns
    yearly_coffee_prices.columns = ['_'.join(col).strip() for col in yearly_coffee_prices.columns.values]
    yearly_coffee_prices.rename(columns={'months_': 'year'}, inplace=True)  # Rename the year column
    yearly_coffee_prices['year'] = pd.to_datetime(yearly_coffee_prices['year'], format='%Y')
    print(transformed_df)

    print(yearly_coffee_prices)


    #To save to a new CSV:
    # transformed_df.to_csv("data/bounded-indicator-prices.csv", index=False)  # index=False prevents writing row numbers
    yearly_coffee_prices.to_csv("data/yearly-min-max-prices.csv", index=False)


import pandas as pd

def transform_exports_data(filepath):
    """
    Transforms yearly coffee export data into a DataFrame with 'year' and 'total_exports' columns.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A pandas DataFrame with 'year' and 'total_exports' columns.
    """

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    # Transpose the DataFrame to get years as rows
    df = df.set_index('exports').T.reset_index() #T for transpose
    df.rename(columns={'index': 'year'}, inplace=True) #rename index col to year

    # Convert year to datetime objects for proper plotting (important for Vega-Lite)
    df['year'] = pd.to_datetime(df['year'], format='%Y')

    # Calculate the total exports for each year
    df['total_exports'] = df.drop('year', axis=1).sum(axis=1) 

    return df[['year', 'total_exports']]


# Example usage:
transformed_exports = transform_exports_data('data/total-production.csv')
# transformed_exports = transform_exports_data('data/exports-calendar-year.csv')

if transformed_exports is not None:
    # print(transformed_exports)

    # Save to a new CSV:
    transformed_exports.to_csv("data/exports-sum.csv", index=False)


# merge the two dataframes
coffee_prices = pd.read_csv('data/yearly-min-max-prices.csv')
coffee_exports = pd.read_csv('data/exports-sum.csv')

merged_df = pd.merge(coffee_prices, coffee_exports, on='year', how='inner')
merged_df.to_csv('data/merged-coffee-data.csv', index=False)
print(merged_df)

