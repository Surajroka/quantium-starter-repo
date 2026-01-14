import pandas as pd
from pathlib import Path
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DATA_PATH = Path("data") / "formatted_sales.csv"
PRICE_INCREASE_DATE = pd.to_datetime("2021-01-15")

df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Region"] = df["Region"].astype(str).str.strip().str.lower()
df = df.dropna(subset=["Date", "Sales", "Region"])

REGION_OPTIONS = [
    {"label": "All", "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
]

app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("Pink Morsel Sales Visualiser", className="title"),
                html.P(
                    "Were sales higher before or after the Pink Morsel price increase on Jan 15, 2021?",
                    className="subtitle",
                ),
            ],
        ),

        html.Div(
            className="card controls",
            children=[
                html.Div(
                    className="control-label",
                    children="Filter by region:",
                ),
                dcc.RadioItems(
                    id="region-radio",
                    options=REGION_OPTIONS,
                    value="all",
                    inline=True,
                    className="radio",
                ),
            ],
        ),

        html.Div(
            className="card",
            children=[
                dcc.Graph(id="sales-line", config={"displayModeBar": False}),
            ],
        ),

        html.Div(
            className="footer",
            children="Soul Foods • Pink Morsel Sales Dashboard",
        ),
    ],
)

@app.callback(
    Output("sales-line", "figure"),
    Input("region-radio", "value"),
)
def update_chart(region_value: str):
    dff = df if region_value == "all" else df[df["Region"] == region_value]

    daily_sales = (
        dff.groupby("Date", as_index=False)["Sales"]
          .sum()
          .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title="Daily Sales (Pink Morsel)",
        labels={"Date": "Date", "Sales": "Sales ($)"},
    )

    # Add vertical line marker for price increase date (robust method)
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
    fig.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase (2021-01-15)",
        showarrow=False,
        yanchor="bottom",
        xanchor="left",
    )

    # Slightly nicer chart look
    fig.update_layout(
        margin=dict(l=40, r=20, t=60, b=40),
        hovermode="x unified",
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)
