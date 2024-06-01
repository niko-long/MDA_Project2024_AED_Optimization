import dash
from dash import dcc, html
from layout import create_top_bar, placeholder
import dash_bootstrap_components as dbc

# 初始化Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义应用的布局
app.layout = html.Div(
    style={'fontFamily': 'Arial', 'padding': '0', 'margin': '0', 'color': '#1C4E80'},
    children=[
        # Top blue bar
        create_top_bar('AED Location Analytics'),
        placeholder,
        # Main content divided into four parts
        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gridTemplateRows': '1fr 1fr', 'gap': '20px', 'padding': '20px'},
            children=[
                html.Div(
                    style={'backgroundColor': 'rgba(245, 245, 245, 1)', 'padding': '30px', 'height': '520px', 'overflow': 'auto'},
                    children=[
                        html.H2('Project Introduction'),
                        html.P('The visualisation of this project consists of three parts:', style={'fontSize': '22px','padding-top':'80px'}),
                        html.P('1. Map visualisation, including AED locations, hospitals, patient visualisations, and changes in patient survival rates with the addition of new AEDs', style={'fontSize': '22px'}),
                        html.P('2. Monthly mortality rates, death rates for heart patients from June 2022 to May 2023', style={'fontSize': '22px'}),
                        html.P('3. Annual mortality rates, summarising cardiac patient mortality rates for different cities in 2022 and 2023', style={'fontSize': '22px'}),
                        html.P('The data includes ambulance call data for cardiac patients located in the cities of Brussels, Antwerp and Liege.', style={'fontSize': '22px'})
                    ]
                ),
                html.Div(
                    style={'textAlign': 'center', 'height': '520px'},
                    children=[
                        html.A(
                            href='http://localhost:8050',
                            children=[
                                html.Img(src='/assets/map.png', style={'width': '100%', 'height': '100%', 'objectFit': 'cover'}),
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={'textAlign': 'center', 'height': '520px'},
                    children=[
                        html.A(
                            href='http://localhost:8053',
                            children=[
                                html.Img(src='/assets/page1.png', style={'width': '100%', 'height': '100%', 'objectFit': 'cover'}),
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={'textAlign': 'center', 'height': '520px'},
                    children=[
                        html.A(
                            href='http://localhost:8052',
                            children=[
                                html.Img(src='/assets/page2.png', style={'width': '100%', 'height': '100%', 'objectFit': 'cover'}),
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# 运行服务器并指定端口号，例如：8051
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)