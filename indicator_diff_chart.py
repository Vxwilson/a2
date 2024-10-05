import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV
df = pd.read_csv('data/indicator-prices.csv')

# Convert 'months' to datetime
df['months'] = pd.to_datetime(df['months'], format='%m/%Y')

# Calculate the average price of the four types of coffee
df['Average'] = df[['Colombian Milds', 'Other Milds', 'Brazilian Naturals', 'Robustas']].mean(axis=1)

# Calculate the difference from the average
df['Diff_Colombian'] = df['Colombian Milds'] - df['Average']
df['Diff_Other'] = df['Other Milds'] - df['Average']
df['Diff_Brazilian'] = df['Brazilian Naturals'] - df['Average']
df['Diff_Robustas'] = df['Robustas'] - df['Average']

# Plotting the differences
plt.figure(figsize=(12, 8))

plt.plot(df['months'], df['Diff_Colombian'], label='Colombian Milds', linestyle='-', marker='')
plt.plot(df['months'], df['Diff_Other'], label='Other Milds', linestyle='-', marker='')
plt.plot(df['months'], df['Diff_Brazilian'], label='Brazilian Naturals', linestyle='-', marker='')
plt.plot(df['months'], df['Diff_Robustas'], label='Robustas', linestyle='-', marker='')

plt.xlabel('Months')
plt.ylabel('Price Difference from Average')
plt.title('Price Difference from Average for Different Types of Coffee')
plt.legend()
plt.grid(True)
plt.show()
