import pandas as pd
from pathlib import Path
from dash import Dash, dcc, html
import plotly.express as px

# Load data from Task 2
DATA_PATH = Path("data") / "formatted_sales.csv"
PRICE_INCREASE_DATE = pd.to_datetime("2021-01-15")

# Read the formatted sales file
df = pd.read_csv(DATA_PATH)

# Ensure correct types
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Region"] = df["Region"].astype(str)

# Drop bad rows
df = df.dropna(subset=["Date", "Sales", "Region"])

# Aggregate sales by date and sort by date
daily_sales = (
    df.groupby("Date", as_index=False)["Sales"]
      .sum()
      .sort_values("Date")
)

# Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    labels={"Date": "Date", "Sales": "Sales ($)"}
)

# Add vertical line (shape) for the price increase date
fig.add_shape(
    type="line",
    x0=PRICE_INCREASE_DATE,
    x1=PRICE_INCREASE_DATE,
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(width=2, dash="dash"),
)

# Add annotation near the top of the chart
fig.add_annotation(
    x=PRICE_INCREASE_DATE,
    y=1,
    xref="x",
    yref="paper",
    text="Price Increase (2021-01-15)",
    showarrow=False,
    yanchor="bottom",
    xanchor="left",
)

# Build the Dash app
app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

app.layout = html.Div(
    style={"maxWidth": "1000px", "margin": "0 auto", "padding": "20px"},
    children=[
        html.H1("Pink Morsel Sales Visualiser"),
        html.P(
            "Question: Were sales higher before or after the Pink Morsel price increase on January 15, 2021?"
        ),
        dcc.Graph(figure=fig),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)
