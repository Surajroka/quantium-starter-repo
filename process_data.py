import pandas as pd
from pathlib import Path

# Path to the data folder
data_folder = Path("data")

# Find all CSV files
csv_files = list(data_folder.glob("*.csv"))

processed_frames = []

for file in csv_files:
    df = pd.read_csv(file)

    # Keep only Pink Morsels
    df = df[df["product"] == "Pink Morsels"]

    # Create sales column
    df["sales"] = df["quantity"] * df["price"]

    # Select required columns
    df = df[["sales", "date", "region"]]

    processed_frames.append(df)

# Combine all CSV data into one DataFrame
final_df = pd.concat(processed_frames, ignore_index=True)

# Save the final output file
output_file = data_folder / "formatted_sales.csv"
final_df.to_csv(output_file, index=False)

print("✅ Task 2 complete: data/formatted_sales.csv created")
