import dash
import statistics
import json
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, State, callback, Patch
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
#app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    html.H1('Eleições municipais de Belo Horizonte (primeiro turno)'),
    html.Div([
        html.Div(
            dcc.Link(f"Navergar para {page['name']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()    
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=False)
