# -*- coding: utf-8 -*-
import dash
import dash_auth
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
                id = 'soc_x',
                options=[
                    {'label': 'Пол', 'value': 'SEX'},
                    {'label': 'Возраст', 'value': 'AGE'}
                    ],
                values=['SEX', 'AGE'],
                labelStyle={'display': 'inline-block'}
            )
        ])
    ]) # Закончился Самый большой контейнер


if __name__ == '__main__':
    app.run_server()
