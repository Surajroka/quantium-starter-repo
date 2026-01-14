import pandas as pd
from pathlib import Path

data_folder = Path("data")
csv_files = list(data_folder.glob("*.csv"))

required_cols = {"product", "quantity", "price", "date", "region"}
frames = []

for file in csv_files:
    df = pd.read_csv(file)

    # Normalize column names to lowercase
    df.columns = [c.lower().strip() for c in df.columns]

    # Skip files missing required columns
    if not required_cols.issubset(df.columns):
        print(f"⚠️ Skipping {file.name} (missing required columns)")
        continue

    # Filter: only "pink morsel" (your data uses lowercase + singular)
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df = df[df["product"] == "pink morsel"]

    # Clean numeric fields
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # price may look like "$3.00" → remove $ and commas, then convert
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Drop any bad rows where conversion failed
    df = df.dropna(subset=["quantity", "price", "date", "region"])

    # Compute sales (numeric)
    df["sales"] = df["quantity"] * df["price"]

    # Keep only required output columns
    df = df[["sales", "date", "region"]]
    frames.append(df)

final_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["sales", "date", "region"])

# Capitalize columns exactly as Quantium asks
final_df = final_df.rename(columns={"sales": "Sales", "date": "Date", "region": "Region"})

output_file = data_folder / "formatted_sales.csv"
final_df.to_csv(output_file, index=False)

print(f" Created {output_file} with {len(final_df)} rows")
