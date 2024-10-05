import pandas as pd

def preprocess_coffee_data(csv_filepath):
    """
    Preprocesses coffee price data by calculating the difference from the average 
    for each coffee group.

    Args:
        csv_filepath: Path to the CSV file containing the data.

    Returns:
        A pandas DataFrame with the preprocessed data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(csv_filepath)

        # Calculate the average price for each coffee group
        coffee_groups = ["Colombian Milds", "Other Milds", "Brazilian Naturals", "Robustas"]
        # averages = df[coffee_groups].mean()

        # Calculate the difference from the average for each group
        for group in coffee_groups:
            df[group] = df[group] - df["ICO composite indicator"]

        return df

    except FileNotFoundError:
        print(f"Error: File not found at {csv_filepath}")
        return None
    except pd.errors.ParserError:  # Handle potential parsing errors
        print(f"Error: Could not parse the CSV file. Check the file format.")
        return None
    except KeyError as e: # Handles if a column name is not found
        print(f"Error: Column {e} not found in the CSV file")
        return None
    except Exception as e:  # Catch any other potential errors
        print(f"An unexpected error occurred: {e}")
        return None


# Example usage (replace with your file path):
filepath = "data/indicator-prices.csv"  
processed_df = preprocess_coffee_data(filepath)

if processed_df is not None:
    print(processed_df)
    # You can now save the processed DataFrame to a new CSV file if needed:
    processed_df.to_csv("data/indicator_prices_avgdiff.csv", index=False) 