# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlite3 as sq
import pandas as pd
import numpy as np
import plotly.graph_objs as go

finance = pd.read_pickle('finance.pcl') # DF for finance

xs = np.array([['D', 'Агрегация по дням недели'], ['M','Агрегация по месяцам'], ['H','Агрегация по времени суток']])
ys = np.array([['ORDER_ID','Количество ордеров (шт)'], ['SUM','Сумма чеков (руб)']])

soc_xs = np.array([['AGE','Возраст'],['SEX','Пол']])

x_axis_dict = {'D':['пн','вт','ср','чт','пт','сб','вс'],
               'M':['January', 'February', 'March', 'April', 'May', 'June', 'July',
                    'August', 'September', 'October', 'November', 'December'],
               'H':range(0,24)}
D_dict = {0:'пн',1:'вт',2:'ср',3:'чт',4:'пт',5:'сб',6:'вс'}
M_dict = {0:'January', 1:'February', 2:'March', 3:'April', 4:'May', 5:'June', 6:'July',
          7:'August', 8:'September', 9:'October', 10:'November', 11:'December'}
agg_dict = {'ORDER_ID':'count', 'SUM':'sum'} #словарь с правилом для агрегации
app = dash.Dash()
app.layout = html.Div([ # Самый большой контейнер
    html.Div([ # Строка с заголовком и слайдерами
        html.Div([html.H1('super dash')]#,style={#'float':'left','display': 'inline-block'}
        ),
        html.Div([dcc.RangeSlider( # слайдер дней недели
            id = 'week_day_lim',
            marks={i: D_dict[i] for i in range(7)},
            min=0,max=7,
            value=[0, 6]
                       )], style={'width': '48%','display': 'inline-block','float':'left'}),
        html.Div([dcc.RangeSlider( # слайдер месяца недели
            id = 'month_lim',
            marks={i: M_dict[i] for i in range(12)},
            min=0,max=12,
            value=[0, 6]
                       )], style={'width': '48%','display': 'inline-block','float':'left'})
            ]),
    html.Div([ # График с деньгами
        html.Div([dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i[1], 'value': i[0]} for i in xs],
                    value='M'
                )],style={'width': '48%',#'display': 'inline-block'
                         }),
        html.Div([dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i[1], 'value': i[0]} for i in ys],
                    value='ORDER_ID'
                )],style={'width': '48%','display': 'inline-block'}),
        dcc.Graph(id='fin_ind',config={'displayModeBar':False})],
                  style={'width': '50%','hight':'10%',  'display': 'inline-block'}
            ),
    html.Div([ # График с social
        html.Div([dcc.Dropdown(
                    id='soc_y',
                    options=[{'label': i[1], 'value': i[0]} for i in ys],
                    value='ORDER_ID'
                )],style={'width': '48%','display': 'inline-block'}),
        html.Div([dcc.Checklist(
                    id = 'soc_x',
                    options=[
                        {'label': 'Пол', 'value': 'SEX'},
                        {'label': 'Возраст', 'value': 'AGE'}
                    ],
                    values=['SEX', 'AGE'],
                    labelStyle={'display': 'inline-block'}
                )
            ], style = {'width': '50%','height':'10%',  'display': 'inline-block'}
            ),
        dcc.Graph(id='soc_ind',config={'displayModeBar':False})],
                  style={'width': '50%','height':'10%',  'display': 'inline-block'})
        ])
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
    return {
            'data': [go.Scatter(
                y=df.loc[x_axis_dict[xaxis_column_name]][yaxis_column_name],
                x=df.loc[x_axis_dict[xaxis_column_name]].index,
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
                 dash.dependencies.Input('month_lim', 'value')
                 ])
def update_graph_soc(soc_x, soc_y, week_day_lim, month_lim):
    agg_dict = {'ORDER_ID':'count', 'SUM':'sum'} #словарь с правилом для агрегации
    axis_name_dict = {'ORDER_ID':'Количество орддеров','SUM':'Сумма чеков',
                      'D':'День недели','H':'Время (часы)','M':'Месяц'} # СЛоварь для подписей к осям
    social = pd.read_pickle('social.pcl')
    df = social[(social.D_N>=week_day_lim[0])&(social.D_N<=week_day_lim[1])&
                 (social.M_N>=month_lim[0])&(social.M_N<=month_lim[1])]
    sex_list = ['Не указан', 'М','Ж']
    age_list = ['Не указан','0-4','4-14', '14-21','21-35', '35-50',  '50-']
    print(soc_x)
    if ('SEX' in soc_x) and ('AGE' in soc_x):
        data = [go.Bar(
            x=sex_list,
            y = [df[(df.SEX==i)&
                  (df.AGE_GROUP == j)][
                  ['SUM']
                  ].agg(agg_dict[soc_y]).values[0] for i in sex_list],
            name = j) for j in age_list
            ]
    elif 'SEX' in soc_x:
        print(1)
        data = [go.Bar(
            x=sex_list,
            y = [df[(df.SEX==i)][
                  ['SUM']
                  ].agg(agg_dict[soc_y]).values[0] for i in sex_list],
            name = 'value')]
    elif  'AGE' in soc_x:
        print (2)
        data = [
        go.Bar(
            x=sex_list,
            y = [df[(df.AGE_GROUP == j)][
                  ['SUM']
                  ].agg(agg_dict[soc_y]).values[0]],
            name = j) for j in age_list
            ]
    else:
        print(3)
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
    app.run_server()
