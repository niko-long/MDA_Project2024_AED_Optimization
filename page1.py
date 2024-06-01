import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from layout import create_top_bar, placeholder

# 创建 Dash 应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 读取 Excel 数据
df = pd.read_excel("data/3_city_case_death.xlsx")

# 将 'Month' 列转换为日期格式
df['Month'] = pd.to_datetime(df['Month'], format='%Y-%m')

# 获取所有唯一的月份并排序
months = pd.date_range(start='2022-06-01', end='2023-05-31', freq='MS').strftime('%Y-%m').tolist()

# Define CSS styles for the slider marks
mark_style = {
    'color': '#488A99',  # Change the mark color
    'fontSize': '12px',  # Change the mark font size
    'fontFamily': 'Arial',  # Change the mark font family
    'whiteSpace': 'nowrap'  # Prevent line break
}

# 定义 Dash 应用布局
app.layout = html.Div(
    style={'fontFamily': 'Arial', 'padding': '0', 'margin': '0', 'minHeight': '100vh', 'backgroundColor': 'rgba(245, 245, 245, 1)'},
    children=[
        # Top blue bar
        create_top_bar('AED Mortality Rate Analysis by Different Cities and Month'),
        placeholder,

        html.Div(
            dcc.Slider(
                id='month-slider',
                min=0,
                max=len(months) - 1,
                value=0,
                marks={i: month for i, month in enumerate(months)},
                step=None
            ),
            style={'width': '90%', 'margin': 'auto', 'padding': '40px 30px', 
                   'overflow': 'visible', 'backgroundColor': 'rgba(245, 245, 245, 1)'}  # 调整滑动条的宽度和背景颜色
        ),

        html.Div(
            children=[
                dcc.Graph(
                    id='example-graph'
                ),
                html.Div(id='pie-charts-container', style={'display': 'flex', 'justify-content': 'space-around'})
            ],
            style={'backgroundColor': 'rgba(245, 245, 245, 1)', 'padding': '10px'}  # 设置背景颜色和内边距
        )
    ]
)

# 设置回调函数，根据滑动条的值更新图表数据
@app.callback(
    [Output('example-graph', 'figure'),
     Output('pie-charts-container', 'children')],
    [Input('month-slider', 'value')]
)
def update_figure(selected_month_index):
    selected_month = months[selected_month_index]
    df_filtered = df[df['Month'].dt.strftime('%Y-%m') == selected_month]

    # 定义城市、总病例数和死亡人数数据
    cities = df_filtered['City'].tolist()
    total_cases = df_filtered['Total Cases'].tolist()
    deaths = df_filtered['Deaths'].tolist()

    # 创建柱状图
    fig = go.Figure()

    # 添加总病例的柱状图
    fig.add_trace(go.Bar(
        x=cities, 
        y=total_cases,
        name='Total Cases',
        marker_color='#1C4E80',
        text=total_cases,
        textposition='auto'
    ))

    # 添加死亡人数的柱状图
    fig.add_trace(go.Bar(
        x=cities, 
        y=deaths,
        name='Deaths',
        marker_color='rgb(255, 123, 0)',
        text=deaths,
        textposition='auto'
    ))

    # 更新图表的布局，包括标题和轴标签
    fig.update_layout(
        title=dict(
        text=f'Total Cases and Death Count by City for {selected_month}',
        font=dict(size=20)  # Adjust the size as needed
    ),
        xaxis=dict(
            title='City',
            titlefont=dict(size=18),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            title='Count',
            titlefont=dict(size=18),
            tickfont=dict(size=14),
            gridcolor='rgba(200, 200, 200, 0.5)'
        ),
        barmode='group',  # 将柱状图设置为分组显示
        bargap=0.2,  # 调整柱状图之间的间距
        plot_bgcolor='rgba(0, 0, 0, 0)',  # 设置图表背景颜色为透明
        paper_bgcolor='rgba(0, 0, 0, 0)',  # 设置图表纸张背景颜色为透明
        legend=dict(
            x=0.02, 
            y=0.98,
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1
        )
    )

    # 创建饼图
    pie_charts = []
    for i, city in enumerate(cities):
        pie_chart = dcc.Graph(
            figure=go.Figure(data=[go.Pie(
                labels=['Deaths', 'Survivals'],
                values=[deaths[i], total_cases[i] - deaths[i]],
                hole=0.3,
                marker=dict(colors=['rgb(255, 123, 0)', '#1C4E80'])  # 使用与柱状图相同的颜色
            )]).update_layout(
                title=dict(
                    text=f'Death Rate for {city}',
                    font=dict(size=20)  # Adjust the size as needed
                ),
                plot_bgcolor='rgba(0, 0, 0, 0)',  # 设置饼图背景颜色为透明
                paper_bgcolor='rgba(0, 0, 0, 0)',  # 设置饼图纸张背景颜色为透明
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255, 255, 255, 0.5)',
                    bordercolor='rgba(0, 0, 0, 0.5)',
                    borderwidth=1
                )
            ),
            style={'width': '30%', 'display': 'inline-block'}
        )
        pie_charts.append(pie_chart)

    return fig, pie_charts

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)