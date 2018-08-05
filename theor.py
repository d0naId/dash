# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlite3 as sq
import pandas as pd
import numpy as np
import plotly.graph_objs as go

finance = pd.read_pickle('finance.pcl') # DF for finance

xs = np.array([['D', 'Агрегация по дням недели'], ['M','Агрегация по ме сяцам'], ['H','Агрегация по времени суток']])
ys = np.array([['ORDER_ID','Количество ордеров (шт)'], ['SUM','Сумма чеков (руб)']])

x_axis_dict = {'D':['пн','вт','ср','чт','пт','сб','вс'],
               'M':['January', 'February', 'March', 'April', 'May', 'June', 'July',
                    'August', 'September', 'October', 'November', 'December'],
               'H':range(0,24)}
D_dict = {0:'пн',1:'вт',2:'ср',3:'чт',4:'пт',5:'сб',6:'вс'}
M_dict = {0:'January', 1:'February', 2:'March', 3:'April', 4:'May', 5:'June', 6:'July',
          7:'August', 8:'September', 9:'October', 10:'November', 11:'December'}

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
        dcc.Graph(id='indicator-graphic',config={'displayModeBar':False})],
                  style={'width': '50%','hight':'10%',  'display': 'inline-block'
                  }
            )

                     ])
@app.callback(dash.dependencies.Output('indicator-graphic', 'figure'),
                [dash.dependencies.Input('xaxis-column', 'value'),
                 dash.dependencies.Input('yaxis-column', 'value'),
                 dash.dependencies.Input('week_day_lim', 'value'),
                 dash.dependencies.Input('month_lim', 'value'),])
def update_graph(xaxis_column_name, yaxis_column_name, week_day_lim, month_lim):
    agg_dict = {'ORDER_ID':'count', 'SUM':'sum'} #словарь с правилом для агрегации
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

if __name__ == '__main__':
    app.run_server()
