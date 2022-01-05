# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 12:07:10 2021

@author: Daniel Moscoe dmoscoe@gmail.com
"""

import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

def species_list():
    """Returns a list of unique tree species.
    """
    url_for_query = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$select=spc_common,count(tree_id)&$group=spc_common'
    res = pd.read_json(url_for_query).dropna().spc_common
    return res

species_list = species_list()

###
app.layout = dbc.Tabs([
    dbc.Tab([
        html.Div([
            html.H1('How healthy are NYC\'s trees?'),
            html.H6('The bar plot shows the health of one species of tree across NYC. The value at the top of each bar gives the total population of that species in a borough.'),
            html.Br(),
            ('Select a species from the dropdown menu below.'),
            dcc.Dropdown(id='species_dropdown_1',
                 options=[{'label':species,'value':species}
                            for species in species_list],
                 value='American beech',),
            html.Br(),
            dcc.Graph(id = 'stacked_bar',),
    ])
        ], style={'padding':20}, label = 'Tree health by borough'),
    
    dbc.Tab([
        html.Div([
            html.H1('Is stewardship related to the health of NYC\'s trees?'),
            html.H6('In the line graph below, each line represents trees of one species in one borough with a single health status. The line shows the fraction of these trees exhibiting none, a few, or many signs of stewardship.'),
            ('Select a species from the dropdown menu below.'),
            dcc.Dropdown(id='species_dropdown_2',
                         options=[{'label':species,'value':species}
                                   for species in species_list],
                         value='American beech',),
            html.Br(),
            html.H6('Select a borough.'),
            dcc.RadioItems(id='borough_radios',
                options=[
            {'label':'Bronx', 'value':'Bronx'},
            {'label':'Brooklyn', 'value':'Brooklyn'},
            {'label':'Manhattan', 'value':'Manhattan'},
            {'label':'Staten Island', 'value':'Staten Island'},
            {'label':'Queens', 'value':'Queens'}],
            value='Bronx',
            inputStyle={"margin-left": "20px"},),
            dcc.Graph(id = 'line',),
            
            ]) #html.Div
        
        
        ], style={'padding':20}, label = 'Stewardship'), #dbc.Tab
    
###

    dbc.Tab([
        html.Div([
            html.H1('The arboretum'),
            html.H6('In the scatterplot below, each dot represents a tree. The health of the tree is indicated by the dot\'s color. The borough and the extent to which the tree has received stewardship are given by the dot\'s location.'),
            ('Select a species from the dropdown menu below.'),
            dcc.Dropdown(id='species_dropdown_3',
                         options=[{'label':species,'value':species}
                                   for species in species_list],
                         value='mulberry',),
            html.Br(),
            dcc.Graph(id = 'arboretum',),
            ('This plot is called \'The arboretum\' because it\'s arranged like a park with groups of trees in different regions of the park. You can imagine walking from the bottom to the top of the plot along the rightmost column to explore all the trees of the selected species in Queens. Along the way, you\'ll see trees in varying states of health. And as you continue your walk, you\'ll see trees with more and more signs of stewardship.'),
            html.Br(),
            ('This plot still has some issues, though.'),
            html.Ul([
                html.Li('How can I show boundaries between different regions in the park? My first strategy using vlines and hlines did not work as expected in the browser.'),
                html.Li('How can I improve the colors in this plot?'),
                html.Li('For very populous species, such as London planetrees, overplotting obscures the true ratios between trees of differing health in the most crowded regions or the plot. For very dense regions, refer to the tab \'Tree health by borough\' for an accurate representation of tree health within a borough.'),
                ])

            ]) #html.Div
        
        ], style={'padding':20}, label = 'Arboretum') #dbc.Tab
    
    ]) #app.layout = dbc.Tabs

@app.callback(Output('stacked_bar', 'figure'),
              Input('species_dropdown_1', 'value'))
def plot_stacked_bar(species):
    """Takes a species.
    Returns a figure that shows the proportion of that species by health status for all boroughs.
    """
    
    #API query
    url_stem = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?'
    url_select = '$select=boroname,health,count(tree_id)'
    url_where = '&$where=spc_common=\'' + species + '\''
    url_group = '&$group=boroname,health'
    url_for_api = (url_stem + url_select + url_where + url_group).replace(' ', '%20')
    df = pd.read_json(url_for_api).fillna(0)
    
    #Dataframe
    tmp = df.groupby(['boroname'])['count_tree_id'].sum().reset_index().rename(columns = {'count_tree_id':'total'})
    df = pd.merge(df,tmp)
    df['fraction'] = df.count_tree_id/df.total
    df.loc[df['health'] != 'Good', ['total']] = ''
    df['health'] = pd.Categorical(df['health'], ['Poor', 'Fair', 'Good'])
    df = df.sort_values(['health'])
    
    #Figure
    stacked_bar = px.bar(data_frame = df,
                         x = 'boroname',
                         y = 'fraction',
                         color = 'health',
                         text = 'total',
                         title = 'The health of NYC\'s ' + str(species) + ' trees',
                         labels = {'boroname':'Borough',
                                   'fraction':'Cumulative fraction of trees'})
    stacked_bar.update_layout(barmode = 'stack',
                              xaxis = {'categoryorder':'array', 'categoryarray':['Bronx', 'Brooklyn', 'Manhattan', 'Staten Island', 'Queens']},
                              legend = {'traceorder':'reversed'})
    return stacked_bar

@app.callback(Output('line','figure'),
              Input('species_dropdown_2','value'),
              Input('borough_radios','value'))
def plot_line(species, borough):
    """Takes a species and a borough.
    Returns a figure showing the relationship between stewardship and tree health.
    """

    url_stem = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?'
    url_select = '$select=health,steward,count(tree_id)'
    url_where = '&$where=spc_common=\'' + species + '\' AND boroname=\'' + borough + '\''
    url_group = '&$group=steward,health'
    url_for_api = (url_stem + url_select + url_where + url_group).replace(' ', '%20')
    df = pd.read_json(url_for_api).dropna()
    
    tmp = df.groupby(['health'])['count_tree_id'].sum().reset_index().rename(columns = {'count_tree_id':'total'})
    df = pd.merge(df,tmp)
    df['fraction'] = df.count_tree_id/df.total
    df.loc[df['steward'] == '1or2', ['steward']] = '1 or 2'
    df.loc[df['steward'] == '3or4', ['steward']] = '3 or 4'
    df.loc[df['steward'] == '4orMore', ['steward']] = '4 or more'
    df['steward'] = pd.Categorical(df['steward'], ['None', '1 or 2', '3 or 4', '4 or more'])
    try:
        Poor_str = 'Poor (n = ' + str(tmp.iloc[2]['total']) + ')'
    except IndexError:
        Poor_str = ''
    
    try:
        Fair_str = 'Fair (n = ' + str(tmp.iloc[0]['total']) + ')'
    except IndexError:
        Fair_str = ''
    
    try:
        Good_str = 'Good (n = ' + str(tmp.iloc[1]['total']) + ')'
    except IndexError:
        Good_str = ''
    
    df.loc[df['health'] == 'Poor', ['health']] = Poor_str
    df.loc[df['health'] == 'Fair', ['health']] = Fair_str
    df.loc[df['health'] == 'Good', ['health']] = Good_str
    
    df['health'] = pd.Categorical(df['health'], [Poor_str, Fair_str, Good_str])    
    
    df = df.sort_values(['steward','health'])

    line_graph = px.line(
        data_frame = df,
        x= 'steward',
        y='fraction',
        color = 'health')

    line_graph.update_layout(
        title = 'Stewardship of ' + str(species) + ' trees in ' + str(borough),
        xaxis_title = 'Signs of stewardship',
        yaxis_title = 'Fraction of trees',
        legend = {'traceorder':'reversed'})

    return line_graph

###
@app.callback(Output('arboretum', 'figure'),
              Input('species_dropdown_3', 'value'))
def arboretum(species):
    #API
    url_stem = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?'
    url_select = '$select=boroname,health,steward,count(tree_id)'
    url_where = '&$where=spc_common=\'' + species + '\''
    url_group = '&$group=boroname,health,steward'
    url_for_api = (url_stem + url_select + url_where + url_group).replace(' ', '%20')
    df = pd.read_json(url_for_api).dropna()
    
    borough = []
    health = []
    steward = []

    borough_location = {'Bronx':0,
          'Brooklyn':5,
          'Manhattan':10,
          'Staten Island':15,
          'Queens':20}

    steward_location = {'None':0,
          '1or2':5,
          '3or4':10,
          '4orMore':15}

    for i in range(len(df)):
        for j in range(df.iloc[i,3]):
            borough.append(borough_location[df.iloc[i,0]])
            health.append(df.iloc[i,1])
            steward.append(steward_location[df.iloc[i,2]])

    to_plot = pd.DataFrame({'borough': borough,
                     'health': health,
                     'steward':steward,
                     'jitterx':np.random.uniform(low = 0, high = 4, size = len(borough)),
                     'jittery':np.random.uniform(low = 0, high = 4, size = len(borough))})

    to_plot['x'] = to_plot.borough + to_plot.jitterx
    to_plot['y'] = to_plot.steward + to_plot.jittery

    to_plot['health'] = pd.Categorical(to_plot['health'], ['Good', 'Fair', 'Poor'])
    to_plot = to_plot.sort_values(['health'])

    fig = px.scatter(to_plot, x = 'x', y = 'y', color = 'health',
                 color_discrete_map={'Poor':'red',
                                     'Fair':'yellow',
                                     'Good':'green'})

    fig.update_xaxes(showgrid = False, zeroline = False,
                 ticktext=['Bronx','Brooklyn','Manhattan','Staten Island','Queens'],
                 tickvals=[2,7,12,17,22])
    fig.update_yaxes(showgrid = False, zeroline = False,
                 ticktext=['None','1 or 2','3 or 4','4 or more'],
                 tickvals=[2,7,12,17])
#    fig.layout.plot_bgcolor = 'white'

    fig.update_traces(mode='markers', marker_line_width=1, marker_size=5, opacity = 0.7)

    fig.update_layout(
    title = 'The health of ' + str(species) + ' trees by borough and stewardship',
    xaxis_title = 'Borough',
    yaxis_title = 'Signs of stewardship')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)