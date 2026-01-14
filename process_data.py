import pandas as pd
from pathlib import Path

data_folder = Path("data")
csv_files = list(data_folder.glob("*.csv"))

required_cols = {"product", "quantity", "price", "date", "region"}
frames = []

for file in csv_files:
    df = pd.read_csv(file)

    # Normalize column names
    df.columns = [c.lower().strip() for c in df.columns]

    # Skip files without the expected schema
    if not required_cols.issubset(df.columns):
        print(f"⚠️ Skipping {file.name} (missing required columns)")
        continue

    # Filter product (your data uses lowercase + singular)
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df = df[df["product"] == "pink morsel"]

    # Convert quantity to number
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Convert price like "$3.00" to numeric
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Drop rows that failed conversion
    df = df.dropna(subset=["quantity", "price", "date", "region"])

    # Compute sales
    df["sales"] = df["quantity"] * df["price"]

    # Keep required columns only
    df = df[["sales", "date", "region"]]
    frames.append(df)

final_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["sales", "date", "region"])

# Capitalize column names exactly as Quantium asks
final_df = final_df.rename(columns={"sales": "Sales", "date": "Date", "region": "Region"})

output_file = data_folder / "formatted_sales.csv"
final_df.to_csv(output_file, index=False)

print(f"✅ Created {output_file} with {len(final_df)} rows")
