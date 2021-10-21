from dash.html.Div import Div
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ])

server = app.server

# -- Import and clean data (importing csv into pandas)
PATH = 'df_clean.csv'
df = pd.read_csv(PATH)



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Ph.D Awarded in The U.S.", style={'text-align': 'center'}),
    html.Div(id="app-container", children=[html.Div(id='heatmap-container', children=[
        html.H4("Number of PhD degrees in each state", style={'text-align': 'center'}),
        html.P("Hover over the state to see break down by schools.", style={'text-align': 'center'}),
        dcc.Graph(id="state-choropleth", figure={}, hoverData={'points':[{'location':'CA'}]}),
        html.H4("Number of PhD by Universities", style={'text-align': 'center'}),
        dcc.Graph(id="selected-data", figure={})])])])



# ------------------------------------------------------------------------------
# the choropleth map
@app.callback(
    Output(component_id='state-choropleth', component_property='figure'),
    [Input(component_id='state-choropleth', component_property='hoverData')]
)
def choropleth_graph(hoverData):
    fig = px.choropleth(df, locations="state_abb", locationmode="USA-states", color="state_num", scope="usa")
    return fig 

# the bar plot
@app.callback(
    Output(component_id='selected-data', component_property='figure'),
    [Input(component_id='state-choropleth', component_property='hoverData')]
)
def update_graph(hoverData):
    dff = df[df.state_abb == hoverData['points'][0]['location']].sort_values(by='num_institution')
    fig = px.bar(dff, x='insitution', y='num_institution')
    return fig 


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)



