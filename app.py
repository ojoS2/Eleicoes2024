import dash
import json
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, Patch
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.graph_objects as go
import plotly.express as px

#app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{ "name": "viewport",
                        "content": "width=device-width, initial-scale=1.0",
                      }])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
             html.H2('Eleições municipais de Belo Horizonte (primeiro turno)'),
             html.Div([
                       html.Div(
                                dcc.Link(f"Navergar para {page['name']}", href=page["relative_path"])
                               ) for page in dash.page_registry.values()  
           ])
    ],justify='center'),dash.page_container
])
    


if __name__ == '__main__':
    app.run(debug=False)
