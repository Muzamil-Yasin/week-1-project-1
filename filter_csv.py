import pandas as pd

# Read CSV
df = pd.read_csv("data.csv")

# Clean column names
df.columns = df.columns.str.strip()  # remove spaces
print(df.columns)  # check exact column names

# Filter rows
filtered_df = df[df['salary'] > 50000]

# Add Bonus column
filtered_df['Bonus'] = filtered_df['salary'] * 0.05

# Save new CSV
filtered_df.to_csv("output/filtered_data.csv", index=False)
print("Filtered data saved to output/filtered_data.csv")
