import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
#from graphPrograms import apuTracker_final as apu
#from graphPrograms import df_by_press_or_parts as dpp
#from graphPrograms import defects_placement_final2 as dfp
#from graphPrograms import pivot_by_part as pbp
import numpy as np
import pandas as pd
from dash.dependencies import State, Input, Output
#from dash.exceptions import PreventUpdate
import datetime
from datetime import datetime as dt
from datetime import date as dtoday
import os
import time


defect_apu = pd.read_csv("./data/defect_apu.csv")
df_5= defect_apu.groupby("Part #").sum()
choices = list(df_5.index)
parts_options = []
for x in choices:
    parts_options.append({"label":x, 'value':x})

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
# app.config.suppress_callback_exceptions = True
server = app.server    


parts_layout = html.Div(

    children=[
        html.Div(
    
            children= [
                html.Div(
                    id="dropdown-select-outer",
                   className="clearfix",
                    children=[
                        html.Div(
                            [
                                html.H3("Select a Part"),
                                dcc.Dropdown(
                                    id="dropdown-select",
                                    #options= parts_options,
                                    options = [{'label': i, 'value':i} for i in df_5.index],
                                    value = '118439'),
                                 
                            ],
                            className = 'box',
                            style = { "float":"left","width":"25em", "padding-right":'3em'},
                        ),
                       
                        html.Div(
                           
                            [
                                
                                html.H3("Select Date Range"),
                                dcc.DatePickerRange(
                                    id="date-picker-range",
                                    min_date_allowed=dt(2008, 1, 1),
                                    max_date_allowed=dtoday.today(), 
                                    initial_visible_month=dt(2019, 9, 1),
                                    display_format="MMM Do, YY",
                                ),
                            ],
                            id="date-picker-outer",
                            className="box",
                            style = { "float":"left", "padding-left":"3em","width":"25em"},
                        ),
                    ], 
                ),
                 html.Div(id='dataOutPut', style={'display': 'none'}),
              
                html.Div(
                    id="middle_row_graphs",
                    className = 'clearfix',
                    children = [
                        html.Div(
                            id= "parts_defect_counts",
                            className = "box1",
                            children = dcc.Graph(id ="defect_counts"),
                        ),
                        html.Div(
                            id = 'where_in_festoon',
                            className = "box2",
                            children = dcc.Graph(id = 'festoon_placement')
                        ),
                    ],
                ),
                html.Div(
                    id = 'last_row',
                    className = 'clearfix',
                    children = [
                        html.Div(
                            id = 'material_box_plot',
                            className = 'box3',
                            children = dcc.Graph(id = 'material_box'),
                        ),
                        html.Div(
                            id = 'process_params_box_plot',
                            className = 'box4',
                            children = dcc.Graph(id = 'process_box'),
                        ),
                    ],

                ),
            ],

        ),
    ],
    )


banner_layout = html.Div(
    [
         html.Div(
            className="row header",
            children=[
                html.Button(id="menu", children=dcc.Markdown("&#8801")),
                html.Span(
                    className="app-title",
                    children=[
                        dcc.Markdown("**CSP-Huntington**"),
                        html.Span(
                            id="subtitle",
                            children=dcc.Markdown("&nbsp using Huntington Data Only"),
                            style={"font-size": "1.8rem", "margin-top": "15px"},
                        ),
                    ],
                ),
                html.Img(src=app.get_asset_url("logo.png")),
                html.A(
                    id="learn_more",
                    children=html.Button("Learn More"),
                    #className = 'button',
                    href="https://www.cspplastics.com/",
                ),
            ],
        ),
        html.Div(
            id="tabs",
            className="row tabs",
            children=[
                dcc.Tab("By Parts"),
                dcc.Tab("By Defect Types"),
                dcc.Tab("Machine Learning Analysis"),
            ],
        ),
       
       
        # html.Div([
        # # represents the URL bar, doesn't render anything
        #     dcc.Location(id='url', refresh=False),

        #     dcc.Link( href='/'),
         
        #     dcc.Link( href='/defects'),
        #     dcc.Link( href='/machine'),

    # content will be rendered in this element
    # html.Div(id='page-content')
    ],
    className = "row",
    style = {"margin":'0%'}
)

app.layout = html.Div(
    [banner_layout, parts_layout]
)

@app.callback(
    Output("defect_counts", "figure"),
    [Input('dropdown-select', 'value')],#Input("dataOutPut", "childen")
)
def plot_all_defects(data):
    x = list(df_5.columns)[2:]
    y = df_5.loc[data][2:]
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(title_text = "Defect Counts",template = 'plotly_dark')
    return fig




@app.callback(
    Output("festoon_placement", "figure"),
    [Input('dropdown-select', 'value')],#Input("dataOutPut", "childen")
)
def where_in_festoon(data):
    x = list(df_5.columns)[2:]
    y = df_5.loc[data][2:]
    fig = go.Figure(data = [go.Pie(labels=x, values=y)])
    fig.update_layout(template = 'plotly_dark',title_text = "Festoon_placement")
   
    return fig


@app.callback(
    Output("material_box", "figure"),
    [Input('dropdown-select', 'value')],#Input("dataOutPut", "childen")
)
def material_box_plot(data):
    x = list(df_5.columns)[2:]
    y = df_5.loc[data][2:]
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(title_text = "Material Box Plot",template = 'plotly_dark')
    return fig
 



@app.callback(
    Output("process_box", "figure"),
    [Input('dropdown-select', 'value')],#Input("dataOutPut", "childen")
)
def process_box_plots(data):
    x = list(df_5.columns)[2:]

    y = df_5.loc[data][2:]
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(title_text = "Process Parameter Box",template = 'plotly_dark')
    return fig
 










if __name__ == "__main__":
    app.run_server(debug=True)