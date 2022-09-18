import plotly.io as pio

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)


# converting strings in yards to float
def conversion_float(val):
    new_val = val.replace(',', '')
    return float(new_val)


app = Dash(__name__)

app.layout = html.Div([
    html.H1("NFL Data Visualization", style={'text-align': 'center'}),  # title
    dcc.Dropdown(id="dropdown",
                 options=[
                     {"label": 'Rushing Leader Yards', "value": "Rushing_leader_by_year.csv"},
                     {"label": 'QB Passing Leader Yards', "value": "passing_leader_yards_by_year.csv"},
                     {"label": 'Passing yds/rushing yds', "value": "P/R Ratio"}],
                 value='Rushing_leader_by_year.csv'),  # drop down menu
    dcc.Graph(id='nfl_map', figure={})  # placeholder for the main graph
])


@app.callback(Output('nfl_map', 'figure'),
              Input('dropdown', 'value'))
def update_graph(value):
    if value == 'P/R Ratio':  # if the dropdown menu call for P/R ratio
        df1 = pd.read_csv(
        # "C:\\Users\\ericq\\PycharmProjects\\NFL_Data_Visualization\\games_data\\passing_leader_yards_by_year.csv")
            "games_data/passing_leader_yards_by_year.csv").drop_duplicates(subset="Year")  # read the data from passing
        df2 = pd.read_csv(
            # "C:\\Users\\ericq\\PycharmProjects\\NFL_Data_Visualization\\games_data\\Rushing_leader_by_year.csv")
            "games_data/Rushing_leader_by_year.csv").drop_duplicates(subset="Year")  # read the data from rushing
        df1.Yards = df1.Yards.apply(conversion_float)  # apply the conversion to Yard column
        df2.Yards = df2.Yards.apply(conversion_float)
        df1.index = df2.index  # reindex the passing data
        df = df1.copy()
        df.Yards = df1["Yards"].div(df2["Yards"])  # divide the passing yard by rushing yard
        df.rename(columns={"Yards": "P yds/R yds"}, inplace=True)  # rename column Yard
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









