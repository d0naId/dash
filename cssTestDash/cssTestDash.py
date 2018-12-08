# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(
    className="layout",
    children=[
    html.Div(
        className="app-header",
        children=[
            html.Div('ISD super dashboard', className="app-header--title")
        ]
    ), #закончился header

    html.Div(
        className="main-content-grid",
        children=[
            html.Div(
                className="left-frame",
                children=[
                    html.H5('Событие'),
                    html.Div('''Div для чекьокса'''),
                    html.H5('Турникет'),
                    html.Div('''Div для чекбокса''')
                ] #закончились дети leftFrame
            ), # закончился leftFrame

            html.Div(
                className="right-frame",
                children=[
                    html.H5('Название графика'),
                    html.Div('''Div для графика'''),
                    html.Div(
                        className= "options",
                        children=[
                            html.Div([
                                    html.H5('Название опции_1'),
                                    html.Div('''ОПЦИЯ_1''')
                            ]),
                            html.Div([
                                    html.H5('Название опции_2'),
                                    html.Div('''ОПЦИЯ_2''')
                                    ])
                        ] #закончились дети options
                    ) #закончился options
                ]#закончились дети rightFrame
            )#закончился rightFrame
        ]#закончился дети mainGrid
    )#закончился mainGrid
]) #закончился главный LayoutDIV

if __name__ == '__main__':
    app.run_server(debug=True)
