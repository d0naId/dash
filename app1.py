# -*- coding: utf-8 -*-
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import sqlite3 as sq
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py

py.sign_in('astepankoff', 'On8qdeiL0m9WEuSmJWak')

USERNAME_PASSWORD_PAIRS = [
    ['ISD', 'ShowMeTheDash'],['D0naid', 'yoyoyo'],['Stepler', 'yoyoyo']
]


path = r'../my_dash_app/{}'

finance = pd.read_pickle(path.format('finance.pcl')) # DF for finance
tech = pd.read_pickle(path.format('tech.pcl'))

xs = np.array([['D', 'Агрегация по дням недели'], ['M','Агрегация по месяцам'], ['H','Агрегация по времени суток']])
ys = np.array([['ORDER_ID','Количество ордеров (шт)'], ['SUM','Сумма чеков (руб)']])
soc_sex_list = np.array(['Не указан', 'М','Ж'])

x_axis_dict = {'D':['пн','вт','ср','чт','пт','сб','вс'],
               'M':['January', 'February', 'March', 'April', 'May', 'June', 'July',
                    'August', 'September', 'October', 'November', 'December'],
               'H':range(0,24)}
D_dict = {0:'пн',1:'вт',2:'ср',3:'чт',4:'пт',5:'сб',6:'вс'}
M_dict = {0:'Jan', 1:'Feb', 2:'Mar', 3:'Apr', 4:'May', 5:'Jun', 6:'Jul',
          7:'Aug', 8:'Sep', 9:'Oct', 10:'Nov', 11:'Dec'}
agg_dict = {'ORDER_ID':'count', 'SUM':'sum'} #словарь с правилом для агрегации

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server

app.layout = html.Div([ # Самый большой контейнер
    html.Div([ # Строка с заголовком и слайдерами
        html.Div([html.H1('ISD super dashboard')]#,style={#'float':'left','display': 'inline-block'}
        ),
        html.Div([dcc.RangeSlider( # слайдер дней недели
            id = 'week_day_lim',
            marks={i: D_dict[i] for i in range(7)},
            min=0,max=7,
            value=[0, 6]
                       )], style={'width': '50%','display': 'inline-block'}),
                                  #style={'width': '48%','display': 'inline-block','float':'left'}),
        html.Div([dcc.RangeSlider( # слайдер месяца недели
            id = 'month_lim',
            marks={i: M_dict[i] for i in range(12)},
            min=0,max=11,
            value=[0, 12]
                       )], style={'width': '50%','display': 'inline-block'})
            ], style={'padding': '38px'}),

    html.Div([
        html.Div([ # График с деньгами
            html.Div([dcc.Dropdown(
                        id='xaxis-column',
                        options=[{'label': i[1], 'value': i[0]} for i in xs],
                        value='M'
                    )],
                    style={'width': '44%','float':'left',
                     'display': 'inline-block',#'background-color': 'cian',
                     #'padding': '10px',
                      'margin-left':'6%'}),
            html.Div([dcc.Dropdown(
                        id='yaxis-column',
                        options=[{'label': i[1], 'value': i[0]} for i in ys],
                        value='ORDER_ID'
                    )],
                    style={'width': '44%','float':'right',
                    'display': 'inline-block',#'background-color': 'yellow',
                    #'padding': '10px',
                    'margin-right':'3%'}),
            html.Div([dcc.Graph(id='fin_ind',config={'displayModeBar':False})],
                        style={'width': '100%','float':'left','margin-top':'30px'}

            )],
                  style={'width': '50%','float':'left'}
        ),

        html.Div([ # График с social
            html.Div([dcc.Dropdown(
                        id='soc_y',
                        options=[{'label': i[1], 'value': i[0]} for i in ys],
                        value='ORDER_ID'
                    )],
                    style={'width': '46%','float':'left',
                     'display': 'inline-block',#'background-color': 'cian',
                     'margin-left': '7%'
                     }),
            html.Div([dcc.Checklist(
                    id = 'soc_x',
                    options=[
                        {'label': 'Пол', 'value': 'SEX'},
                        {'label': 'Возраст', 'value': 'AGE'}
                    ],
                    values=['SEX', 'AGE'],
                    labelStyle={'display': 'inline-block'},
                )
            ],style={'width': '25%','float':'left','display': 'inline-block', 'margin-left': '12%','margin-top': '1%'
            }),
            html.Div([dcc.Graph(id='soc_ind',config={'displayModeBar':False})],
                      style={'width': '100%', 'float':'left','margin-top':'30px','display': 'inline-block'#,'padding-top':'20px'
                      }),

            html.Div([ ##Checklist

                html.Div(#[html.P('Пол:'),
                    [dcc.Checklist(
                        id = 'soc_sexs',
                        options=[
                            {'label':i, 'value':i} for i in np.array(['Не указан', 'М','Ж'])
                        ],
                        values=['Не указан', 'М','Ж'],
                        labelStyle={'display': 'inline-block'}
                    )
                ],style={'width': '25%','margin-left': '10%','float':'left','display': 'inline-block'}),

                html.Div([dcc.Checklist(
                        id = 'soc_ages',
                        options=[
                            {'label':i, 'value':i} for i in np.array(['Не указан','0-4','4-14', '14-21','21-35', '35-50',  '50-'])
                        ],
                        values=['Не указан','0-4','4-14', '14-21','21-35', '35-50',  '50-'],
                        labelStyle={'display': 'inline-block'}
                    )
                ],style={'width': '60%', 'margin-left': '5%','float':'left','display': 'inline-block'}),
                ], style = {'width': '100%', 'float':'right','display': 'inline-block', 'padding': '-10px'

                })],#,'padding': '10px'}
            ##social
#            dcc.Graph(id='soc_ind',config={'displayModeBar':False})],
            style={'width': '50%', 'display': 'inline-block'#,'padding-top':'20px'
                }
        )
    ],style={'width': '100%','margin-top':'1%'}
    ),
    html.Div([
    #html.Div([],style={'width': '200px', 'float':'left', 'display': 'inline-block',
    #                    'background-color': 'cian'}),
    html.Div([ #heat_map
##        html.Div(
##            [dcc.Checklist(
##                    id = 'tech_event',
##                    options=[{'label':i, 'value':i}
##                    for i in tech.EVENT.unique()],
##                    values=tech.EVENT.unique(),
##                    labelStyle={'display': 'inline-block'}
##                )],
##            style={'width': '100%',
##            'float':'left','display': 'inline-block',
##                   'padding': '5px'}
##        ),
        html.Div(
            [dcc.Graph(id='tech_ind',config={'displayModeBar':False}
            )],
            style={'width': '100%',
            'float':'left','display': 'inline-block',
                   #'padding-left': '150px', #'border': '10px','border-color': 'black'
                    }
        )

    ],style={'width': '49%',
            'float':'left','display': 'inline-block',
            #'display': 'flex',
            #'justify-content': 'center',
           'padding-top': '-100px',
           'margin-left': '20%'
           }
    ), ##heat_map
    #
    html.Div([
    html.Div(
        [dcc.Checklist(
                id = 'tech_event',
                options=[{'label':i, 'value':i}
                for i in tech.EVENT.unique()],
                values=tech.EVENT.unique(),
                labelStyle={'display': 'inline-block'}
            )],
        style={'width': '200px',
        'float':'left','display': 'inline-block',
               'padding-top': '100px'}
    )
    ],style={'width': '20%','float':'left','display': 'inline-block'})
])

],style={'width': '100%'}) #сабый большой контейнр

@app.callback(dash.dependencies.Output('tech_ind', 'figure'),
                [dash.dependencies.Input('tech_event', 'values'),
                 dash.dependencies.Input('week_day_lim', 'value'),
                 dash.dependencies.Input('month_lim', 'value')])
def update_graph_tech(tech_event, week_day_lim, month_lim):
    df = tech[(tech.D_N>=week_day_lim[0])&(tech.D_N<=week_day_lim[1])&
              (tech.M_N>=month_lim[0])&(tech.M_N<=month_lim[1])]
    index_n = [ind in tech_event for ind in df.EVENT]
    df = df[index_n]

    for_plot = df.pivot_table(values='DATE', columns='H', index = 'DEVICE', aggfunc='count').fillna(0)

    hovertext = list()
    for yi, yy in enumerate(for_plot.index):
        hovertext.append(list())
        for xi, xx in enumerate(for_plot.columns):
            hovertext[-1].append('устройство: {}<br /> время : {}-{}'.format(yy, xx, xx+1))
    return {
        'data': [go.Heatmap(x=for_plot.columns,
                   y=for_plot.index,
                   z=for_plot.values,
                   hoverinfo='z+text',
                   text = hovertext)]
    }

@app.callback(dash.dependencies.Output('fin_ind', 'figure'),
                [dash.dependencies.Input('xaxis-column', 'value'),
                 dash.dependencies.Input('yaxis-column', 'value'),
                 dash.dependencies.Input('week_day_lim', 'value'),
                 dash.dependencies.Input('month_lim', 'value'),])
def update_graph_fin(xaxis_column_name, yaxis_column_name, week_day_lim, month_lim):

    axis_name_dict = {'ORDER_ID':'Количество орддеров','SUM':'Сумма чеков',
                      'D':'День недели','H':'Время (часы)','M':'Месяц'} # СЛоварь для подписей к осям

    df = finance[(finance.D_N>=week_day_lim[0])&(finance.D_N<=week_day_lim[1])&
                 (finance.M_N>=month_lim[0])&(finance.M_N<=month_lim[1])][
                    [xaxis_column_name,yaxis_column_name]].fillna(0).groupby(
                        xaxis_column_name).agg(agg_dict[yaxis_column_name])
    print (xaxis_column_name)
    if xaxis_column_name == 'D':
        min_x = week_day_lim[0]
        max_x = week_day_lim[1]
    elif xaxis_column_name == 'M':
        min_x = month_lim[0]
        max_x = month_lim[1]
    elif xaxis_column_name == 'H':
        min_x = 0
        max_x = 25

    return {
            'data': [go.Scatter(
                y=df.loc[x_axis_dict[xaxis_column_name][min_x:max_x+1]][yaxis_column_name],
                x=df.loc[x_axis_dict[xaxis_column_name][min_x:max_x+1]].index,
                text='blablabla',
                mode='lines+markers',
                marker={'size': 15, 'opacity': 0.5, 'line': {'width': 0.5, 'color': 'white'}}
                )],
            'layout': go.Layout(
                xaxis={
                    'title': axis_name_dict[xaxis_column_name],
                    #'type': 'linear' if xaxis_type == 'Linear' else 'log'
                },
                yaxis={
                    'title': axis_name_dict[yaxis_column_name],
                    #'type': 'linear' if yaxis_type == 'Linear' else 'log'
                },
                margin={'l': 100, 'b': 70, 't': 0, 'r': 15},
                #hovermode='closest'
            )
        }

@app.callback(dash.dependencies.Output('soc_ind', 'figure'),
                [dash.dependencies.Input('soc_x', 'values'),
                 dash.dependencies.Input('soc_y', 'value'),
                 dash.dependencies.Input('week_day_lim', 'value'),
                 dash.dependencies.Input('month_lim', 'value'),
                 dash.dependencies.Input('soc_sexs', 'values'),
                 dash.dependencies.Input('soc_ages', 'values'),
                 ])
def update_graph_soc(soc_x, soc_y, week_day_lim, month_lim, soc_sexs, soc_ages):
    agg_dict = {'ORDER_ID':'count', 'SUM':'sum'} #словарь с правилом для агрегации
    axis_name_dict = {'ORDER_ID':'Количество орддеров','SUM':'Сумма чеков',
                      'D':'День недели','H':'Время (часы)','M':'Месяц'} # СЛоварь для подписей к осям

    social = pd.read_pickle(path.format('social.pcl'))
    df = social[(social.D_N>=week_day_lim[0])&(social.D_N<=week_day_lim[1])&
                 (social.M_N>=month_lim[0])&(social.M_N<=month_lim[1])]
    df = df[[i in soc_sexs for i in df.SEX]]
    df = df[[i in soc_ages for i in df.AGE_GROUP]]
    sex_list = ['Не указан', 'М','Ж']
    age_list = ['Не указан','0-4','4-14', '14-21','21-35', '35-50',  '50-']
    if ('SEX' in soc_x) and ('AGE' in soc_x):
        data = [go.Bar(
            x = [s for s in sex_list if s in soc_sexs],
            y = [df[(df.SEX==i)&
                  (df.AGE_GROUP == j)][
                  ['SUM']
                  ].agg(agg_dict[soc_y]).values[0] for i in sex_list if i in soc_sexs],
            name = j) for j in age_list if j in soc_ages
            ]
    elif 'SEX' in soc_x:
        data = [go.Bar(
            x= [s for s in sex_list if s in soc_sexs],
            y = [df[(df.SEX==i)][
                  ['SUM']
                  ].agg(agg_dict[soc_y]).values[0] for i in sex_list if i in soc_sexs],
            name = 'value')]
    elif  'AGE' in soc_x:
        data = [
        go.Bar(
            x= [s for s in age_list if s in soc_ages],
            y = [df[(df.AGE_GROUP == j)][
                  ['SUM']
                  ].agg(agg_dict[soc_y]).values[0] for j in age_list if j in soc_ages],
            name = 'value')
            ]
    else:
        data = [
        go.Bar(
            x=sex_list,
            y = df[['SUM']].agg(agg_dict[soc_y]).values[0],
            name = 'name')
            ]
    return {
            'data': data,
            'layout': go.Layout(
                xaxis={
                    #'title': axis_name_dict[xaxis_column_name],
                    #'type': 'linear' if xaxis_type == 'Linear' else 'log'
                },
                yaxis={
                    #'title': axis_name_dict[yaxis_column_name],
                    #'type': 'linear' if yaxis_type == 'Linear' else 'log'
                },
                margin={'l': 100, 'b': 70, 't': 0, 'r': 15},
                hovermode='closest'
            )
        }

if __name__ == '__main__':
    app.run_server(debug=True)
