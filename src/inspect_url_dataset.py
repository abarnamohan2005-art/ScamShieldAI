
import pandas as pd

# Load URL dataset
data = pd.read_csv("data/phishing_urls.csv")

# Display first five rows
print("FIRST FIVE ROWS:")
print(data.head())

# Display column names
print("\nCOLUMN NAMES:")
print(data.columns.tolist())

# Display dataset size
print("\nDATASET SHAPE:")
print(data.shape)

# Display data types and missing values
print("\nDATASET INFORMATION:")
data.info()

print("\nMISSING VALUES:")
print(data.isnull().sum())

# Display duplicate rows
print("\nDUPLICATE ROWS:")
print(data.duplicated().sum())

# Display unique values in each column
print("\nUNIQUE VALUES:")
for column in data.columns:
    print(column, ":", data[column].nunique())
print("\nCLASS DISTRIBUTION:")
print(data["type"].value_counts())

print("\nCLASS DISTRIBUTION IN PERCENTAGE:")
print(data["type"].value_counts(normalize=True) * 100)