# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()
print(min_payload, max_payload)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',

                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                            {'label': launch_sites[0], 'value': launch_sites[0]}, {'label': launch_sites[1], 'value': launch_sites[1]}, {'label': launch_sites[2], 'value': launch_sites[2]},
                                            {'label': launch_sites[3], 'value': launch_sites[3]}
                                            ],

                                    value='ALL',
                                    placeholder="Select site",
                                    searchable=True,
                                            ),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={
                                            0: '0 kg',
                                            2500: '2500 kg',
                                            5000: '5000 kg',
                                            7500: '7500 kg',
                                            10000: '10000 kg'
                                        },
                                        value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
    # Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                  Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site','class']]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site',
                color_discrete_sequence = px.colors.qualitative.Set3,
                width=800, height=400,
                title="Total Landing Success Proportion by Site: {}".format(entered_site))
        return fig
    else:

        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df['success']= filtered_df['class'].astype('bool')
        #names = filtered_df.groupby('class').count().reset_index()['class']
        values = filtered_df.groupby('class').count().reset_index()['success']

        fig = px.pie(filtered_df, values=values, names= values.index, color = values.index,
                color_discrete_sequence = px.colors.qualitative.Set1,
                width=800, height=400,
                title="Landing Success Proportion for site: {}".format(entered_site))
        return fig
            # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                  [Input(component_id='site-dropdown', component_property='value'),
                  Input(component_id="payload-slider", component_property="value")])
def scatter_chart(entered_site, slider_range):

    filtered_df = spacex_df[['Flight Number','Launch Site','class',   'Payload Mass (kg)', 'Booster Version Category']]
    low, high = slider_range
    mask = (filtered_df['Payload Mass (kg)'] >= low) & (filtered_df['Payload Mass (kg)'] <= high)
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class', color = 'Booster Version Category',
            size =(filtered_df[mask]['Flight Number']+20)/2, size_max = 10,
            title="Correlation between Payload and Success for site: {}".format(entered_site))
        return fig
    else:

        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class', color = 'Booster Version Category', size = 'Flight Number',
        labels = {'Booster Version Category': 'Booster Version'},
        title="Correlation between Payload and Success for site: {}".format(entered_site))
        return fig
            # return the outcomes piechart for a selected site

# Run the app
if __name__ == '__main__':
    app.run_server()
