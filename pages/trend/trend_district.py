import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(__name__, name="trend_district", path="/trend/trend-district")

layout = html.Div(children=[
    html.H2(children='แนวโน้มอายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) (หน่วย: ปี)', className="section-name"),
    html.Div([
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page3 - Thailand Trend.png"), className="tab-pic-trend"),
            html.H2(children = 'ภาพรวมประเทศ', className="tab-name-trend"),
        ], href="/trend/trend-country", style={'background-color': '#dadee7', 
                                         'border' : 'solid 3px #aeb2b7'}, id="tab1-trend-dt"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page3 - Health Region.png"), className="tab-pic-trend"),
            html.H2(children = 'ระดับเขตสุขภาพ', className="tab-name-trend"),
        ], href="/trend/trend-district", style={'background-color': '#bbdee4',
                                                'border' : 'solid 3px #1aa2b6'}, id="tab2-trend-dt"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page3 - Province.png"), className="tab-pic-trend"),
            html.H2(children = 'ระดับจังหวัด', className="tab-name-trend"),
        ], href="/trend/trend-province", style={'background-color': '#dadee7',
                                                'border' : 'solid 3px #aeb2b7'}, id="tab3-trend-dt"),
    ], className="tabs-trend"),
    html.Div([
        html.Div([
            html.Div("เลือก", className="filter-panel-name"),
            html.Div([
                html.H3(children = 'เขตสุขภาพ', className="filter-name"),
                dcc.Dropdown(clearable=False, id="dt-dd-trend-dt")     
            ], className="filter", id="dt-filter-trend-dt"),
            html.Div([
                html.H3(children = 'การคำนวณ', className="filter-name"),
                dcc.Dropdown({'0':"เมื่อแรกเกิด (at birth)", '60':"เมื่ออายุ 60 ปี"},'0', clearable=False, id="type-dd-trend-dt")     
            ], className="filter", id="type-filter-trend-dt"),
            html.Div([
                html.H3(children = 'เพศ', className="filter-name"),
                dcc.Dropdown({'male':"เพศชาย", 'female':"เพศหญิง"},'male',clearable=False, id="sex-dd-trend-dt")     
            ], className="filter", id="sex-filter-trend-dt"),
            html.Button("ตั้งช่วงแกนใหม่", className="filter", id="reset-dt")
        ], id="filter-panel-trend-dt"),
        html.Div([
            dcc.Graph(id="le-trend-dt", config= {'displaylogo': False}),
            dcc.Graph(id="hale-trend-dt", config= {'displaylogo': False})
        ], className="line-chart-block")
    ], className="filter-and-content-block"),
], className="page-3-trend-dt")

@callback(
    [Output("dt-dd-trend-dt", "options"),
     Output("dt-dd-trend-dt", "value")],
     Input("pv-store", "data")
)
def update_dt_dropdown(data):
    temp_df = pd.DataFrame(data)

    return [{dt.split()[1] : dt for dt in temp_df["area_code"].unique().tolist()}, '1']

@callback(
    [Output("le-trend-dt", "figure"),
     Output("hale-trend-dt", "figure")],
    [Input("dt-dd-trend-dt", "value"),
     Input("type-dd-trend-dt", "value"),
     Input("sex-dd-trend-dt", "value"),
     Input("pv-store", "data"),
     Input("reset-dt","n_clicks")],
)
def update_line_chart_trend_ct(dt, age_type, sex, data, n_clicks):
    temp_df = pd.DataFrame(data)
    temp_df['used_year'] = temp_df['year'] + 543
    temp_df['เพศ'] = temp_df['sex'].apply(lambda x : 'เพศชาย' if x == 'male' else ('เพศหญิง' if x == 'female' else 'รวมเพศ'))
    temp_df = temp_df.rename(columns={'th_province':'จังหวัด'})
    filtered_df = temp_df.loc[(temp_df['age_type'] == int(age_type)) &
                              (temp_df['district_number'] == int(dt)) &
                              (temp_df['sex'] == sex)]

    fig = px.line(filtered_df, x="used_year", y="LE", color='จังหวัด', custom_data=['จังหวัด', 'เพศ'],
                  title='แนวโน้มอายุคาดเฉลี่ย (LE)', line_shape='spline', markers=True)
    fig.update_traces(hovertemplate='%{customdata[0]}<extra></extra><br>ปี พ.ศ. %{x}<br>%{customdata[1]}<br>LE: %{y:.1f}')
    fig.update_yaxes(range=[0,100],ticksuffix = "  ")
    fig.update_xaxes(range=[filtered_df['used_year'].min()-0.1, filtered_df['used_year'].max()+0.1], dtick=1)
    fig.update_layout(xaxis=dict(fixedrange = True, title=None, showgrid=False),
                      yaxis=dict(title=None),
                      legend=dict(orientation='h', xanchor='center', yanchor='bottom', x=0.5, y=-0.2, title=None),
                      title=dict(x=0.5, font_weight='bold'),
                      hoverlabel_font=dict(color='black', family="IBM Plex Sans Thai"),
                      hoverlabel_bordercolor="black",
                      margin=dict(l=50, r=50, t=50, b=0), font_family="IBM Plex Sans Thai",
                      plot_bgcolor='#f0f1f3', paper_bgcolor='#f0f1f3',
                      modebar_remove = ["toImage", "select2d", "lasso2d", "zoomIn2d", 
                                        "zoomOut2d", "resetScale2d"])

    fig_2 = px.line(filtered_df, x="used_year", y="HALE", color='จังหวัด', custom_data=['จังหวัด', 'เพศ'],
                    title='แนวโน้มอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE)', line_shape='spline', markers=True)
    fig_2.update_traces(hovertemplate='%{customdata[0]}<extra></extra><br>ปี พ.ศ. %{x}<br>%{customdata[1]}<br>LE: %{y:.1f}')
    fig_2.update_yaxes(range=[0,100],ticksuffix = "  ")
    fig_2.update_xaxes(range=[filtered_df['used_year'].min()-0.1, filtered_df['used_year'].max()+0.1], dtick=1)
    fig_2.update_layout(xaxis=dict(fixedrange = True, title=None, showgrid=False),
                      yaxis=dict(title=None),
                      legend=dict(orientation='h', xanchor='center', yanchor='bottom', x=0.5, y=-0.2, title=None),
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