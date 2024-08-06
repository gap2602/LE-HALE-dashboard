import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(__name__, name="trend_country", path="/trend/trend-country")

layout = html.Div(children=[
    html.H2(children='แนวโน้มอายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) (หน่วย: ปี)', className="section-name"),
    html.Div([
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page3 - Thailand Trend.png"), className="tab-pic-trend"),
            html.H2(children = 'ภาพรวมประเทศ', className="tab-name-trend"),
        ], href="/trend/trend-country", style={'background-color': '#bbdee4', 
                                         'border' : 'solid 3px #1aa2b6'}, id="tab1-trend-ct"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page3 - Health Region.png"), className="tab-pic-trend"),
            html.H2(children = 'ระดับเขตสุขภาพ', className="tab-name-trend"),
        ], href="/trend/trend-district", style={'background-color': '#dadee7',
                                                'border' : 'solid 3px #aeb2b7'}, id="tab2-trend-ct"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page3 - Province.png"), className="tab-pic-trend"),
            html.H2(children = 'ระดับจังหวัด', className="tab-name-trend"),
        ], href="/trend/trend-province", style={'background-color': '#dadee7',
                                                'border' : 'solid 3px #aeb2b7'}, id="tab3-trend-ct"),
    ], className="tabs-trend"),
    html.Div([
        html.Div([
            html.Div("เลือก", className="filter-panel-name"),
            html.Div([
                html.H3(children = 'การคำนวณ', className="filter-name"),
                dcc.Dropdown({'0':"เมื่อแรกเกิด (at birth)", '60':"เมื่ออายุ 60 ปี"},'0', clearable=False, id="type-dd-trend-ct")     
            ], className="filter", id="type-filter-trend-ct"),
            html.Button("ตั้งช่วงแกนใหม่", className="filter", id="reset-ct")
        ], id="filter-panel-trend-ct"),
        html.Div([
            dcc.Graph(id="le-trend-ct", config= {'displaylogo': False}),
            dcc.Graph(id="hale-trend-ct", config= {'displaylogo': False})
        ], className="line-chart-block")
    ], className="filter-and-content-block")
], className="page-3-trend-ct")

@callback(
    [Output("le-trend-ct", "figure"),
     Output("hale-trend-ct", "figure")],
    [Input("type-dd-trend-ct", "value"),
     Input("ov-store", "data"),
     Input("reset-ct","n_clicks")]
)
def update_line_chart_trend_ct(age_type, data, n_clicks):
    temp_df = pd.DataFrame(data)
    temp_df['used_year'] = temp_df['year'] + 543
    temp_df['เพศ'] = temp_df['sex'].apply(lambda x : 'เพศชาย' if x == 'male' else ('เพศหญิง' if x == 'female' else 'รวมเพศ'))
    filtered_df = temp_df.loc[temp_df['age_type'] == int(age_type)]

    fig = px.line(filtered_df, x="used_year", y="LE", color='เพศ', custom_data=['เพศ'],
                  title='แนวโน้มอายุคาดเฉลี่ย (LE)', line_shape='spline', markers=True)
    fig.update_traces(hovertemplate='%{customdata[0]}<extra></extra><br>ปี พ.ศ. %{x}<br>LE: %{y:.1f}')
    fig.update_yaxes(range=[0,100],ticksuffix = "  ")
    fig.update_xaxes(range=[filtered_df['used_year'].min()-0.1, filtered_df['used_year'].max()+0.1], dtick=1)
    fig.update_layout(xaxis=dict(fixedrange = True, title=None, showgrid=False),
                      yaxis=dict(title=None),
                      legend=dict(orientation='h', xanchor='center', yanchor='bottom', x=0.5, y=-0.2),
                      title=dict(x=0.5, font_weight='bold'),
                      hoverlabel_font=dict(color='black', family="IBM Plex Sans Thai"),
                      hoverlabel_bordercolor="black",
                      margin=dict(l=50, r=50, t=50, b=0), font_family="IBM Plex Sans Thai",
                      plot_bgcolor='#f0f1f3', paper_bgcolor='#f0f1f3',
                      modebar_remove = ["toImage", "select2d", "lasso2d", "zoomIn2d", 
                                        "zoomOut2d", "resetScale2d"])
    
    fig_2 = px.line(filtered_df, x="used_year", y="HALE", color='เพศ', custom_data=['เพศ'],
                    title='แนวโน้มอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE)', line_shape='spline', markers=True)
    fig_2.update_traces(hovertemplate='%{customdata[0]}<extra></extra><br>ปี พ.ศ. %{x}<br>LE: %{y:.1f}')
    fig_2.update_yaxes(range=[0,100],ticksuffix = "  ")
    fig_2.update_xaxes(range=[filtered_df['used_year'].min()-0.1, filtered_df['used_year'].max()+0.1], dtick=1)
    fig_2.update_layout(xaxis=dict(fixedrange = True, title=None, showgrid=False),
                      yaxis=dict(title=None),
                      legend=dict(orientation='h', xanchor='center', yanchor='bottom', x=0.5, y=-0.2),
                      title=dict(x=0.5, font_weight='bold'),
                      hoverlabel_font=dict(color='black', family="IBM Plex Sans Thai"),
                      hoverlabel_bordercolor="black",
                      margin=dict(l=50, r=50, t=50, b=0), font_family="IBM Plex Sans Thai",
                      plot_bgcolor='#f0f1f3', paper_bgcolor='#f0f1f3',
                      modebar_remove = ["toImage", "select2d", "lasso2d", "zoomIn2d", 
                                        "zoomOut2d", "resetScale2d"])
    
    if n_clicks:
        fig.update_layout(yaxis_range=[0,100])
        fig_2.update_layout(yaxis_range=[0,100])
    
    return [fig, fig_2]
