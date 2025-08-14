import pandas as pd

# Read CSV and clean data
df = pd.read_csv("data.csv")
df.fillna(0, inplace=True)           # Replace missing values with 0
df.drop_duplicates(inplace=True)     # Remove duplicates

# Mean function
def calculate_mean(data):
    return {
        "age_mean": data["age"].mean(),
        "salary_mean": data["salary"].mean()
    }

# Median function
def calculate_median(data):
    return {
        "age_median": data["age"].median(),
        "salary_median": data["salary"].median()
    }

# Mode function
def calculate_mode(data):
    return {
        "age_mode": data["age"].mode()[0] if not data["age"].mode().empty else None,
        "salary_mode": data["salary"].mode()[0] if not data["salary"].mode().empty else None
    }

# Save summary to file
def save_summary(mean_vals, median_vals, mode_vals):
    with open("summary.txt", "w") as f:
        f.write("Summary Report\n")
        f.write("------------------\n")
        f.write(f"Mean: {mean_vals}\n")
        f.write(f"Median: {median_vals}\n")
        f.write(f"Mode: {mode_vals}\n")
    print("\nSummary saved to 'summary.txt'.")

# Run and store results
mean_values = calculate_mean(df)
median_values = calculate_median(df)
mode_values = calculate_mode(df)

# Print DataFrame
print("DataFrame:")
print(df)

# Print results
print("\nResults:")
print(mean_values)
print(median_values)
print(mode_values)

# Save results to file
save_summary(mean_values, median_values, mode_values)
