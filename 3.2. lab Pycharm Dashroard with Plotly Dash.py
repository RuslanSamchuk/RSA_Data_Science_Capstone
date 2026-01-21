'''
Hands-on Lab: Build an Interactive Dashboard with Plotly Dash
In this lab, you will be building a Plotly Dash application for users to perform interactive visual analytics on SpaceX launch data in
real-time.

This dashboard application contains input components such as a dropdown list and a range slider to
interact with a pie chart and a scatter point chart. You will be guided to build this dashboard application via the following tasks:

TASK 1: Add a Launch Site Drop-down Input Component
TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
TASK 3: Add a Range Slider to Select Payload
TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
Note:Please take screenshots of the Dashboard and save them. Further upload your notebook to github.

The github url and the screenshots are later required in the presentation slides.
After visual analysis using the dashboard, you should be able to obtain some insights to answer the following five questions:

Which site has the largest successful launches?
Which site has the highest launch success rate?
Which payload range(s) has the highest launch success rate?
Which payload range(s) has the lowest launch success rate?
Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
launch success rate?
'''
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/t4-Vy4iOU19i8y6E3Px_ww/spacex-dash-app.py"
import urllib.request

urls = {
    "spacex_launch_dash.csv":
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv",
    "spacex-dash-app.py":
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/t4-Vy4iOU19i8y6E3Px_ww/spacex-dash-app.py"
}

for filename, url in urls.items():
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, filename)

print("Done.")

'''
TASK 1: Add a Launch Site Drop-down Input Component
We have four different launch sites and we would like to first see which one has the largest success count. Then,
we would like to select one specific site and check its detailed success rate (class=0 vs. class=1).

As such, we will need a dropdown menu to let us select different launch sites.

Find and complete a commented dcc.Dropdown(id='site-dropdown',...) input with following attributes:
id attribute with value site-dropdown
options attribute is a list of dict-like option objects (with label and value attributes). You can set
the label and value all to be the launch site names in the spacex_df
and you need to include the default All option. e.g.,
'''
# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

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
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
#Next, we want to find if variable payload is correlated to mission outcome. From a dashboard point of view, we
#want to be able to easily select different payload range and see if we can identify some visual patterns.
#Find and complete a commented dcc.RangeSlider(id='payload-slider',...) input with the following attribute:
#id to be payload-slider
#min indicating the slider starting point, we set its value to be 0 (Kg)
#max indicating the slider ending point to, we set its value to be 10000 (Kg)
#step indicating the slider interval on the slider, we set its value to be 1000 (Kg)
#value indicating the current selected range, we could set it to be min_payload and max_payload
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
'''
The general idea of this callback function is to get the selected launch site from site-dropdown and render
a pie chart visualizing launch success counts.

Dash callback function is a type of Python function which will be automatically called by
Dash whenever receiving an input component updates, such as a click or dropdown selecting event.

If you need to refresh your memory about Plotly Dash callback functions,
you may refer to the lab you have learned before:

Plotly Dash Lab

Let’s add a callback function in spacex_dash_app.py including the following application logic:

Input is set to be the site-dropdown dropdown, i.e., Input(component_id='site-dropdown', component_property='value')
Output to be the graph with id success-pie-chart, i.e., Output(component_id='success-pie-chart', component_property='figure')
A If-Else statement to check if ALL sites were selected or just a specific launch site was selected
If ALL sites are selected, we will use all rows in the dataframe spacex_df to render and return a pie chart graph to show the total success launches (i.e., the total count of class column)
If a specific launch site is selected, you need to filter the dataframe spacex_df first in order
to include the only data for the selected site.
Then, render and return a pie chart graph to show the success (class=1) count and failed (class=0) count for the selected site.
'''
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='Launch Site',
        title='Success Count for all launch sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values='class count', names='class',
                     title=f"Total Success Launches for site {entered_site}")
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
'''
Next, we want to plot a scatter plot with the x axis to be the payload and the y axis to be the launch outcome (i.e., class column).
As such, we can visually observe how payload may be correlated with mission outcomes for selected site(s).

In addition, we want to color-label the Booster version on each scatter point so that we may
observe mission outcomes with different boosters.

Now, let’s add a call function including the following application logic:

Input to be [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
Note that we have two input components, one to receive selected launch site and another to receive selected payload range
Output to be Output(component_id='success-payload-scatter-chart', component_property='figure')
A If-Else statement to check if ALL sites were selected or just a specific launch site was selected
If ALL sites are selected, render a scatter plot to display all values for variable Payload Mass (kg) and variable class.
In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
If a specific launch site is selected, you need to filter the spacex_df first, and render a scatter chart to show
values Payload Mass (kg) and class for the selected site, and color-label the point using Boosster Version Category likewise.
'''
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def scatter(entered_site, payload):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]
    # thought reusing filtered_df may cause issues, but tried it out of curiosity and it seems to be working fine

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Success count on Payload mass for all sites')
        return fig
    else:
        fig = px.scatter(filtered_df[filtered_df['Launch Site'] == entered_site], x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f"Success count on Payload mass for site {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run()
