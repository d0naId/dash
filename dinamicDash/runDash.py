# -*- coding: utf-8 -*-
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import sqlite3 as sq
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objs as go
import sys
path2root = '.'
sys.path.append(path2root)
from utils.dbAPI import DataPrepare
from dbinfo.access import db_acc_dict, USERNAME_PASSWORD_PAIRS

#new params
host = db_acc_dict['host']
port = db_acc_dict['port']
service_name = db_acc_dict['service_name']
user = db_acc_dict['user']
passwd = db_acc_dict['passwd']

# Load data hear
## hist graph base
### read request
turTransaction = open('./requests/turTransaction.txt', 'r', encoding="utf-8").read()

### HARD CODE
min_date = '29.12.2017'
max_date = '03.01.2018'

### declarate object
base_hist_obj = DataPrepare(min_date, max_date, turTransaction)
print('Loading data')

base_hist_obj.connection(user, passwd, host, port, service_name)
base_hist_obj.take_data()

today = '05.01.2018'
print('Load one more day')
base_hist_obj.get_new_date(new_max = today)



app = dash.Dash(__name__, sharing=True)
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server


app.layout = html.Div(
    [ # Самый большой контейнер
    html.Div([html.H1('ISD super dashboard')]), # Заголовок
    html.Div(
        [
        html.Div([
        html.P('Выберети интересующие Вас действия')],
               style={'float':'left',
                  'margin-top':'30px',
                  'display': 'inline-block'}),
        dcc.Checklist(
                id = 'EVENT',
                options=[
                    {'label': 'доступ разрешен', 'value': 'доступ разрешен'},
                    {'label': 'был проход (вход)', 'value': 'был проход (вход)'},
                    {'label': 'был проход (выход)', 'value': 'был проход (выход)'},
                    {'label': 'ошибочная транзакция', 'value': 'ошибочная транзакция'},
                    {'label': 'вход после таймаута', 'value': 'вход после таймаута'}
                    ],
                values=['доступ разрешен', 'был проход (вход)',
                'ошибочная транзакция', 'был проход (выход)',
                'открытие из кассы', 'вход после таймаута'],
                labelStyle={'display': 'inline-block', 'float':'left'}
            ),  # Закончился Checklist EVENT
        html.Div([
        html.P('Выберите турникеты')],
               style={'float':'left',
                  'margin-top':'30px',
                  'display': 'inline-block'}),
        dcc.Checklist(
                id = 'DEVICE',
                options=[
                    {'label': 'Тур.№2 KABA-КАССА (2-ой слева)', 'value': 'Тур.№2 KABA-КАССА (2-ой слева)'},
                    {'label': 'Тур.№3 KABA-ВХОД', 'value': 'Тур.№3 KABA-ВХОД'},
                    {'label': 'Тур.№1 KABA-ВЫХОД (Левый)', 'value': 'Тур.№1 KABA-ВЫХОД (Левый)'},
                    {'label': 'Тур.№7 Skidata (Соляная)', 'value': 'Тур.№7 Skidata (Соляная)'},
                    {'label': 'Тур.№4 KABA-КАССА (Правый)', 'value': 'Тур.№4 KABA-КАССА (Правый)'}
                    ],
                values=['Тур.№2 KABA-КАССА (2-ой слева)', 'Тур.№3 KABA-ВХОД',
                        'Тур.№1 KABA-ВЫХОД (Левый)', 'Тур.№7 Skidata (Соляная)',
                        'Тур.№4 KABA-КАССА (Правый)'],
                labelStyle={'display': 'inline-block', 'float':'left'}
            ),   # Закончился Checklist DEVICE
        html.Div([
        html.P('Введите кол-во дней')],
               style={'float':'left',
                  'margin-top':'30px',
                  'display': 'inline-block'}),
        dcc.Input(
            id = 'HIST',
            placeholder='Количество дней',
            type='text',
            value='3'
            ),  #Закончился Input
        ], style={'width': '19%',
                  'float':'left','display': 'inline-block',
                  'padding-top': '50px'}),  # Dash Core Components

    html.Div([
        html.Div([
        html.Div([
        html.P('Укажите частоту дискретизации')],
               style={'float':'left',
                  'margin-top':'30px',
                  'display': 'inline-block'}),
        dcc.Dropdown(
            id = 'GROUPER',
            options=[
                {'label': '30 мин', 'value': 'HALFH'},
                {'label': '1 день', 'value': 'DAY'},
                {'label': '1 неделя', 'value': 'WEEK'},
                {'label': '1 месяц', 'value': 'MONTH'}
            ],
            value='HALFH'
            ) # Закончился Dropdown
        ], style={'width': '50%'}),

        dcc.Graph(id='bar_time',config={'displayModeBar':False})
        ], style={'width': '80%', 'float':'left',
                  'margin-top':'30px',
                  'display': 'inline-block'})
    ]) # Закончился Самый большой контейнер

@app.callback(dash.dependencies.Output('bar_time', 'figure'),
              [dash.dependencies.Input('EVENT', 'values'),
               dash.dependencies.Input('GROUPER', 'value'),
               dash.dependencies.Input('DEVICE', 'values'),
               dash.dependencies.Input('HIST', 'value')])

def update_bar_time(EVENT, GROUPER, DEVICE, HIST):
    df_test = base_hist_obj.df
    base_hist_obj.get_new_date(new_max = today)

    df_for_plot = df_test[df_test.HALFH > (df_test.HALFH.max() - datetime.timedelta(days=int(HIST))) ]
    event_mask = np.array([event_row in EVENT for event_row in df_for_plot.EVENT])
    device_mask = np.array([device_row in DEVICE for device_row in df_for_plot.DEVICE])
    df_for_plot = df_for_plot[event_mask & device_mask]

    print('df_for_plot_mask', df_for_plot.shape)

    data = [go.Bar(
            y = df_for_plot.groupby(GROUPER).EVENT.count(),
            x = df_for_plot.groupby(GROUPER).count().index
    )]

    return {'data': data}

if __name__ == '__main__':
    app.run_server()
