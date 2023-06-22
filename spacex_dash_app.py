# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())

# Create a Dash application
app = dash.Dash(__name__)

# Create the app layout
app.layout = html.Div(
    children=[
        html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC SC-39A', 'value': 'KSC SC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
            value='ALL',
            placeholder='All Sites',
            searchable=True
        ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        dcc.Graph(id='success-pie-chart'),

        html.Br(),
        html.P("Payload range (Kg):"),

        # TASK 3: Add a slider to select the payload range
        dcc.RangeSlider(
            id='payload-slider',
            min=min_payload,
            max=max_payload,
            step=1000,
            value=[min_payload, max_payload],
            marks={i: str(i) for i in range(min_payload, max_payload + 1, 1000)}
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        dcc.Graph(id='success-payload-scatter-chart'),
    ]
)


# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Launch Success Counts')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, values='class', names='class',
                     title=f"Total Success Launches for site {entered_site}")
    return fig


# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def scatter(entered_site, payload):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title='Success count on Payload mass for all sites')
    else:
        filtered_site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_site_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title=f"Success count on Payload mass for site {entered_site}")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
