# -*- coding: utf-8 -*-
import dash
# import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import sqlite3 as sq
import pandas as pd
import numpy as np
import plotly.graph_objs as go

app = dash.Dash(__name__, sharing=True)
server = app.server

USERNAME_PASSWORD_PAIRS = [
    ['ISD', 'ShowMeTheDash'],['D0naid', 'yoyoyo'],['Stepler', 'yoyoyo']]

app.layout = html.Div(
    [ # Самый большой контейнер
    html.Div([html.H1('ISD super dashboard')]), # Заголовок
    html.Div(
        [
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
        dcc.Dropdown(
            id = 'GROUPER',
            options=[
                {'label': '30 мин', 'value': 'HALFH'},
                {'label': '1 день', 'value': 'DAY'},
                {'label': '1 неделя', 'value': 'WEEK'},
                {'label': '1 месяц', 'value': 'MONTH'}
            ],
            value='HALFH'
            ), # Закончился Dropdown
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
        dcc.Input(
            id = 'HIST',
            placeholder='Количество дней',
            type='text',
            value='3'
            )  #Закончился Input
        ], style={'width': '200px',
                  'float':'left','display': 'inline-block',
                  'padding-top': '50px'}),  # Dash Core Components
    # html.Div([
    #     dcc.Graph(id='bar_time',config={'displayModeBar':False}
    #     ])
    ]) # Закончился Самый большой контейнер


if __name__ == '__main__':
    app.run_server()
