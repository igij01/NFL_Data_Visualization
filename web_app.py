import plotly.io as pio

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)


def conversion_float(val):
    new_val = val.replace(',', '')
    return float(new_val)


def conversion_percentile(val):
    return int(val * 100)


app = Dash(__name__)

app.layout = html.Div([
    html.H1("NFL Data Visualization", style={'text-align': 'center'}),
    dcc.Dropdown(id="dropdown",
                 options=[
                     {"label": 'Rushing Leader Yards', "value": "Rushing_leader_by_year.csv"},
                     {"label": 'QB Passing Leader Yards', "value": "passing_leader_yards_by_year.csv"},
                     {"label": 'Passing yds/rushing yds', "value": "P/R Ratio"}],
                 value='Rushing_leader_by_year.csv'),
    dcc.Graph(id='nfl_map', figure={})
])

@app.callback(Output('nfl_map', 'figure'),
              Input('dropdown', 'value'))

def update_graph(value):
    if value == 'P/R Ratio':
        df1 = pd.read_csv(
        # "C:\\Users\\ericq\\PycharmProjects\\NFL_Data_Visualization\\games_data\\passing_leader_yards_by_year.csv")
            "games_data/passing_leader_yards_by_year.csv").drop_duplicates(subset="Year")
        df2 = pd.read_csv(
            # "C:\\Users\\ericq\\PycharmProjects\\NFL_Data_Visualization\\games_data\\Rushing_leader_by_year.csv")
            "games_data/Rushing_leader_by_year.csv").drop_duplicates(subset="Year")
        df1.Yards = df1.Yards.apply(conversion_float)
        df2.Yards = df2.Yards.apply(conversion_float)
        df1.index = df2.index
        df = df1.copy()
        df.Yards = df1["Yards"].div(df2["Yards"])
        df.rename(columns={"Yards": "P yds/R yds"}, inplace=True)
        # df.Yards = df.Yards.apply(conversion_percentile)
        fig = px.scatter(df, x="Year", y="P yds/R yds")
    else:
        df = pd.read_csv(
        # "C:\\Users\\ericq\\PycharmProjects\\NFL_Data_Visualization\\games_data\\"
            "games_data/"
        + value)
        df.Yards = df.Yards.apply(conversion_float)
        df = df.drop_duplicates(subset="Year")
        fig = px.scatter(df, x="Year", y="Yards")
    return fig
#
# fig = px.line(object.loc[object['QB Passing Leader Yards'] == ])

app.run_server(debug=True)









