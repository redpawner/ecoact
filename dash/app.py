import dash
from dash import html
import requests
import dash_table

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Greenhouse Gas Emissions Dashboard"),
    dash_table.DataTable(
        id="emissions-table",
        columns=[],
        data=[],
    ),
])

response = requests.get("http://localhost:8000/summary-data")
data = response.json()

if data:
    columns = [{"name": col, "id": col} for col in data[0].keys()]
    table_data = [{col: entry[col] for col in entry.keys()} for entry in data]
    app.layout["emissions-table"].data = table_data
    app.layout["emissions-table"].columns = columns

if __name__ == "__main__":
    app.run_server(debug=True)
