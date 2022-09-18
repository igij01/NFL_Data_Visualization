import read_from_csv
import plotly.io as pio
import read_games_data

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)



def conversion(val):
    new_val = val.replace(',', '')
    return float(new_val)


app = Dash(__name__)

app.layout = html.Div([
    html.H1("NFL Data Visualization", style={'text-align': 'center'}),
    dcc.Dropdown(id="dropdown",
                 options=[
                     {"label": 'Rushing Leader Yards', "value": "Rushing_leader_by_year.csv"},
                     {"label": 'QB Passing Leader Yards', "value": "passing_leader_yards_by_year.csv"},
                     {"label": 'Passing yds/rushing yds', "value": "P/R Ratio"}],
                 value='passing_leader_yards_by_year.csv'),
    dcc.Graph(id='nfl_map', figure={})
])

@app.callback(Output('nfl_map', 'figure'),
              Input('dropdown', 'value'))

def update_graph(value):
    if value == 'P/R Ratio':
        object1 = read_from_csv.ReadCsv(
        "C:\\Users\\ericq\\PycharmProjects\\NFL_Data_Visualization\\games_data\\passing_leader_yards_by_year.csv")
        object2 = read_from_csv.ReadCsv(
            "C:\\Users\\ericq\\PycharmProjects\\NFL_Data_Visualization\\games_data\\Rushing_leader_by_year.csv")
        object1.data.Yards = object1.data.Yards.apply(conversion)
        object1 = object1.filter_column(["Year", "Yards"])
        object2.data.Yards = object2.data.Yards.apply(conversion)
        object2 = object2.filter_column(["Year", "Yards"])
        object = object1
        object.Yards = object1.Yards / object2.Yards
    else:
        object = read_from_csv.ReadCsv(
        "C:\\Users\\ericq\\PycharmProjects\\NFL_Data_Visualization\\games_data\\" + value)
        object = object.filter_column(["Year", "Yards"])
        object.Yards = object.Yards.apply(conversion)
    object = object.drop_duplicates(subset="Year").sort_values(by="Yards", ascending=False)
    fig = px.scatter(object, x="Year", y="Yards")
    return fig
#
# fig = px.line(object.loc[object['QB Passing Leader Yards'] == ])

app.run_server(debug=True)









