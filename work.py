# Working Dashboard
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                dcc.Dropdown(id='site-dropdown',
                                                options={'All Sites':'ALL', 'CCAFS LC-40':'CCAFS LC-40', 'VAFB SLC-4E':'VAFB SLC-4E', 'KSC LC-39A':'KSC LC-39A', 'CCAFS SLC-40':'CCAFS SLC-40'},
                                                value='ALL',
                                                placeholder='Select Launch Site',
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                updatemode='drag'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def make_pie(site):
    filtered_df=spacex_df[spacex_df['Launch Site']==site]
    success_total = sum(spacex_df['class']==1)
    fail_total = sum(spacex_df['class']==0)
    success_count = sum(filtered_df['class']==1)
    fail_count = sum(filtered_df['class']==0)
    if site == 'ALL':
        fig = go.Figure(data=[go.Pie(labels=['Success', 'Failure'], values=[success_total, fail_total])])
        fig.update_layout(title=f"Launch Site: {site}")
        return fig
    else:
        fig = go.Figure(data=[go.Pie(labels=['Success', 'Failure'], values=[success_count, fail_count])])
        fig.update_layout(title=f"Launch Site; {site}")
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def make_scatter(site, slide):
    filtered_df=spacex_df[spacex_df['Launch Site']==site]
    frange_df=filtered_df[filtered_df['Payload Mass (kg)'].between(min(slide), max(slide))==True]
    range_df=spacex_df[spacex_df['Payload Mass (kg)'].between(min(slide), max(slide))==True]
    if site == 'ALL':
        fig = px.scatter(data_frame=range_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        fig = px.scatter(data_frame=frange_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()