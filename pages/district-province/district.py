import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

dash.register_page(__name__, name="district", path="/district-province/district")

layout = html.Div(children=[
    html.H2(children='อายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) ระดับประเทศปี พ.ศ. 2562 (หน่วย: ปี)', className="section-name", id="section-name-dt"),
    html.Div([
        html.Div([
            html.H3(children = 'เลือกปี พ.ศ.', className="year-filter-title"),
            dcc.Dropdown(clearable=False, id="year-dd-dt")     
        ], className="year-filter"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - Overview.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลภาพรวม', className="tab-name"),
        ], href="/district-province/district", style={'background-color': '#bbdee4', 
                                                      'border' : 'solid 3px #1aa2b6'}, id="tab1-dt"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - map.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลแผนที่', className="tab-name"),
        ], href="/district-province/map", style={'background-color': '#dadee7',
                                                 'border' : 'solid 3px #aeb2b7'}, id="tab2-dt"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - Table.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลมีตาราง', className="tab-name"),
        ], href="/district-province/table", style={'background-color': '#dadee7',
                                                   'border' : 'solid 3px #aeb2b7'}, id="tab3-dt")
    ], className="year-filter-and-tabs"),
    html.Div([
        html.Div([
            html.Div("เลือก", className="filter-panel-name"),
            dcc.Link("ระดับเขตสุขภาพ", className="level-tab", 
                     href="/district-province/district", style={'background-color': '#1aa3b7'}),
            dcc.Link("ระดับจังหวัด", className="level-tab",
                     href="/district-province/province", style={'background-color': '#b3b3b3'}),
            html.Div([
                html.H4("เขตสุขภาพ", className="filter-name"),
                dcc.Dropdown(id='dt-dd', clearable=False)
            ], id="dt-filter"),
            html.Div([
                html.H4("การคำนวณ", className="filter-name"),
                dcc.Dropdown({'0':"เมื่อแรกเกิด (at birth)", '60':"เมื่ออายุ 60 ปี"},'0', id='type-dd', 
                             clearable=False)
            ], id="type-filter"),
        ], id="filter-panel"),
        html.Div([
            html.Div("ภาพรวมเขตสุขภาพ 1", id="content-name-1-dt"),
            html.Div([
                html.Div([
                    html.Div([
                        #html.Img(src=dash.get_asset_url("Page1 - Male.png"), className="sex-pic"),
                        html.Div("เพศชาย", className="sex-male"),
                    ], className="dt-header"),
                    html.Div([
                        dcc.Graph(id="dt-male-at-birth", config={'displayModeBar': False}, className="bar-chart"),
                        dcc.Graph(id="dt-male-at-60",config={'displayModeBar': False}, className="bar-chart")
                    ], className="dt-bar-chart"),
                    html.Div([
                        html.Div("เมื่อแรกเกิด (at birth)", className="dt-type-name-value"),
                        html.Div("เมื่ออายุ 60 ปี", className="dt-type-name-value")
                    ], className="dt-type-name"),
                    html.Div([
                        html.Div(children=["LE", html.Br(), html.Div(id='dt-male-at-birth-le', style={'color':'#1a84b8'})], className="card-box-left"),
                        html.Div(children=["HALE", html.Br(), html.Div(id='dt-male-at-birth-hale', style={'color':'#25a3e0'})], className="card-box-right"),
                        html.Div(children=["LE", html.Br(), html.Div(id='dt-male-at-60-le', style={'color':'#1a84b8'})], className="card-box-left"),
                        html.Div(children=["HALE", html.Br(), html.Div(id='dt-male-at-60-hale', style={'color':'#25a3e0'})], className="card-box-right")
                    ], className="dt-value")
                ], id="dt-male"),
                html.Div([
                    html.Div([
                        #html.Img(src=dash.get_asset_url("Page1 - Female.png"), className="sex-pic"),
                        html.Div("เพศหญิง", className="sex-female"),
                    ], className="dt-header"),
                    html.Div([
                        dcc.Graph(id="dt-female-at-birth",config={'displayModeBar': False}, className="bar-chart"),
                        dcc.Graph(id="dt-female-at-60",config={'displayModeBar': False}, className="bar-chart")
                    ], className="dt-bar-chart"),
                    html.Div([
                        html.Div("เมื่อแรกเกิด (at birth)", className="dt-type-name-value"),
                        html.Div("เมื่ออายุ 60 ปี", className="dt-type-name-value")
                    ], className="dt-type-name"),
                    html.Div([
                        html.Div(children=["LE", html.Br(), html.Div(id='dt-female-at-birth-le', style={'color':'#b81a84'})], className="card-box-left"),
                        html.Div(children=["HALE", html.Br(), html.Div(id='dt-female-at-birth-hale', style={'color':'#e025a3'})], className="card-box-right"),
                        html.Div(children=["LE", html.Br(), html.Div(id='dt-female-at-60-le', style={'color':'#b81a84'})], className="card-box-left"),
                        html.Div(children=["HALE", html.Br(), html.Div(id='dt-female-at-60-hale', style={'color':'#e025a3'})], className="card-box-right")
                    ], className="dt-value")
                ], id="dt-female")
            ], id="dt-content")
        ], id="dt-block"),
        html.Div([
            html.Div("เปรียบเทียบจังหวัดภายในเขตสุขภาพ", id="content-name-2-dt"),
            html.Div([
                html.Div([
                    html.Div([
                        #html.Img(src=dash.get_asset_url("male_icon.png"),className="sex-pic"),
                        html.Div("เพศชาย", className="sex-male"),
                    ], className="pv-header"),
                    dcc.Graph(id="pv-male-dt",config={'displayModeBar': False}, className="hbar-chart"),
                    dcc.Graph(id="pv-male-pv",config={'displayModeBar': False}, className="hbar-chart"),
                ],id="pv-male"),
                html.Div([
                    html.Div([
                        #html.Img(src=dash.get_asset_url("female_icon.png"),className="sex-pic"),
                        html.Div("เพศหญิง", className="sex-female"),
                    ], className="pv-header"),
                    dcc.Graph(id="pv-female-dt",config={'displayModeBar': False}, className="hbar-chart"),
                    dcc.Graph(id="pv-female-pv",config={'displayModeBar': False}, className="hbar-chart"),
                ],id="pv-female"),
            ],id="pv-content"),
            html.Div([
                html.Div("", id="legend-le-m", style={'background-color':'#1a84b8'}),
                html.Div("LE เพศชาย", className="legend-name"),
                html.Div("", id="legend-hale-m", style={'background-color':'#25a3e0'}),
                html.Div("HALE เพศชาย", className="legend-name"),
                html.Div("", id="legend-le-fm", style={'background-color':'#b81a84'}),
                html.Div("LE เพศหญิง", className="legend-name"),
                html.Div("", id="legend-hale-fm", style={'background-color':'#e025a3'}),
                html.Div("HALE เพศหญิง", className="legend-name"),
            ], id="legend")
        ], id="pv-block"),
    ], className="filter-and-content-block"),
], className="page-2-dt")

def gen_bar_chart_dt(df, year, dt, type_code, sex, color_left, color_right):

    used_data = df.loc[(df['year'] == year-543) &
                       (df["district_number"] == dt) & 
                       (df["age_type"] == type_code) &
                       (df["sex"] == sex)]
    
    fig = px.bar( x=['<b>LE</b>', '<b>HALE</b>'], y=used_data[["LE","HALE"]].values[0], text_auto=True)
    fig.update_yaxes(range=[0,100])
    fig.update_traces(textfont_size=14, textangle=0, textposition="outside", texttemplate="%{value:.1f}",
                      textfont_weight='bold', marker_color=[color_left, color_right], 
                      textfont_color=[color_left, color_right], marker_line_width = 0,
                      hovertemplate='%{x}: %{y:.1f}')
    fig.update_layout(xaxis=dict(showgrid=False, title=None, fixedrange = True),
                      yaxis=dict(showgrid=False, visible=False, fixedrange = True),
                      margin=dict(l=15, r=15, t=0, b=0), bargap=0, font_family="IBM Plex Sans Thai",
                      plot_bgcolor='#f0f1f3', paper_bgcolor='#f0f1f3')
    return fig

def gen_hbar_chart_dt(df, year, dt, type_code, sex, color_le, color_hale):

    used_data = df.loc[(df['year'] == year-543) &
                       (df["district_number"] == dt) & 
                       (df["age_type"] == type_code) &
                       (df["sex"] == sex)]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name = 'HALE',y = ['เขตสุขภาพ {}'.format(dt)], x = used_data["HALE"].values, 
                         marker_color=color_hale, orientation='h', textfont_color=color_hale))
    fig.add_trace(go.Bar(name = 'LE',y = ['เขตสุขภาพ {}'.format(dt)], x = used_data["LE"].values, 
                         marker_color=color_le, orientation='h', textfont_color=color_le))
    fig.update_xaxes(range=[0,100])
    fig.update_traces(textfont_size=14, textangle=0, textposition="outside", texttemplate="%{value:.1f}",
                      textfont_weight='bold', marker_line_width = 0, hovertemplate='%{y}: %{x:.1f}')
    fig.update_layout(xaxis=dict(showgrid=False, title=None, showticklabels=False, fixedrange = True),
                      yaxis=dict(showgrid=False, visible=True, fixedrange = True),
                      margin=dict(l=0, r=0, t=0, b=0), bargap=0, font_family="IBM Plex Sans Thai",
                      plot_bgcolor='#f0f1f3', paper_bgcolor='#f0f1f3', showlegend=False)

    return fig

def gen_hbar_chart_pv(df, year, dt, type_code, sex, color_le, color_hale):

    used_data = df.loc[(df['year'] == year-543) &
                       (df["district_number"] == dt) & 
                       (df["age_type"] == type_code) &
                       (df["sex"] == sex)]
    space = 0
    if used_data.shape[0] == 1:
        space = 60

    fig = go.Figure()
    fig.add_trace(go.Bar(name = 'HALE', y = used_data["th_province"].values, x = used_data["HALE"].values, 
                         marker_color=color_hale, orientation='h', textfont_color=color_hale))
    fig.add_trace(go.Bar(name = 'LE', y = used_data["th_province"].values, x = used_data["LE"].values, 
                         marker_color=color_le, orientation='h', textfont_color=color_le))
    fig.update_xaxes(range=[0,100])
    fig.update_traces(textfont_size=14, textangle=0, textposition="outside", texttemplate="%{value:.1f}",
                      textfont_weight='bold', width=0.5, marker_line_width = 0, hovertemplate='%{y}: %{x:.1f}')
    fig.update_layout(xaxis=dict(showgrid=False, title=None, showticklabels=False, fixedrange = True),
                      yaxis=dict(showgrid=False, visible=True, fixedrange = True),
                      margin=dict(l=0, r=0, t=space, b=space), font_family="IBM Plex Sans Thai",
                      plot_bgcolor='#f0f1f3', paper_bgcolor='#f0f1f3', showlegend=False, 
                      barmode='group', bargap=0.20, bargroupgap=0.0, autosize=True)

    return fig

@callback(
    [Output("year-dd-dt", "options"),
     Output("year-dd-dt", "value")],
    Input("dt-store", "data")
)
def update_year_dropdown(data):
    temp_df = pd.DataFrame(data)
    min_year = min(temp_df['year']) + 543
    max_year = max(temp_df['year']) + 543

    return [{'label':year, 'value':year} for year in range(min_year, max_year+1)], min_year

@callback(
    [Output("dt-dd", "options"),
     Output("dt-dd", "value")],
     Input("pv-store", "data")
)
def update_district_dropdown(data):
    temp_df = pd.DataFrame(data)

    return [{dt.split()[1] : dt for dt in temp_df["area_code"].unique().tolist()}, '1']


@callback(
    [Output("section-name-dt", "children"),
     Output("content-name-1-dt", "children"),
     Output("content-name-2-dt", "children")],
    [Input("dt-dd", "value"),
     Input("type-dd", "value"),
     Input('year-dd-dt', 'value')]
)
def update_title_name(dt, type_code, selected_year):
    return [
        'อายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) ระดับประเทศปี พ.ศ. ' + str(selected_year) + ' (หน่วย: ปี)',
        'ภาพรวมเขตสุขภาพ ' + dt,
        'เปรียบเทียบจังหวัดภายในเขตสุขภาพ - เมื่อแรกเกิด (at birth)' if type_code == '0' else 'เปรียบเทียบจังหวัดภายในเขตสุขภาพ - เมื่ออายุ 60 ปี',
    ]

@callback(
    [Output("dt-male-at-birth", "figure"),
     Output("dt-male-at-60", "figure"),
     Output("dt-female-at-birth", "figure"),
     Output("dt-female-at-60", "figure"),
     Output("pv-male-dt", "figure"),
     Output("pv-male-pv", "figure"),
     Output("pv-female-dt", "figure"),
     Output("pv-female-pv", "figure")],
    [Input("dt-dd", "value"),
     Input("type-dd", "value"),
     Input('year-dd-dt', 'value'),
     Input('dt-store', 'data'),
     Input('pv-store', 'data')]
)
def update_all_charts(dt, type_code, selected_year, dt_data, pv_data):
    dt_df = pd.DataFrame(dt_data)
    pv_w_code_df = pd.DataFrame(pv_data)
    return [
       gen_bar_chart_dt(dt_df, selected_year, int(dt), 0, "male", "#1a84b8", "#25a3e0"),
       gen_bar_chart_dt(dt_df, selected_year, int(dt), 60, "male", "#1a84b8", "#25a3e0"),
       gen_bar_chart_dt(dt_df, selected_year, int(dt), 0, "female", "#b81a84", "#e025a3"),
       gen_bar_chart_dt(dt_df, selected_year, int(dt), 60, "female", "#b81a84", "#e025a3"),
       gen_hbar_chart_dt(dt_df, selected_year, int(dt), int(type_code), "male", "#1a84b8", "#25a3e0"),
       gen_hbar_chart_pv(pv_w_code_df, selected_year, int(dt), int(type_code), "male", "#1a84b8", "#25a3e0"),
       gen_hbar_chart_dt(dt_df, selected_year, int(dt), int(type_code), "female", "#b81a84", "#e025a3"),
       gen_hbar_chart_pv(pv_w_code_df, selected_year, int(dt), int(type_code), "female", "#b81a84", "#e025a3")
    ]

@callback(
    [Output("dt-male-at-birth-le", "children"),
     Output("dt-male-at-birth-hale", "children"),
     Output("dt-male-at-60-le", "children"),
     Output("dt-male-at-60-hale", "children"),
     Output("dt-female-at-birth-le", "children"),
     Output("dt-female-at-birth-hale", "children"),
     Output("dt-female-at-60-le", "children"),
     Output("dt-female-at-60-hale", "children")],
    [Input("dt-dd", "value"),
     Input('year-dd-dt', 'value'),
     Input('dt-store', 'data')]
)
def update_cards(dt, selected_year, dt_data):
    dt_df = pd.DataFrame(dt_data)
    used_data = dt_df.loc[(dt_df['year'] == selected_year-543) &
                          (dt_df["district_number"] == int(dt))]
    return [
       "{:.1f}".format(used_data.loc[(used_data["sex"] == "male")&(used_data["age_type"] == 0),"LE"].values[0]),
       "{:.1f}".format(used_data.loc[(used_data["sex"] == "male")&(used_data["age_type"] == 0),"HALE"].values[0]),
       "{:.1f}".format(used_data.loc[(used_data["sex"] == "male")&(used_data["age_type"] == 60),"LE"].values[0]),
       "{:.1f}".format(used_data.loc[(used_data["sex"] == "male")&(used_data["age_type"] == 60),"HALE"].values[0]),
       "{:.1f}".format(used_data.loc[(used_data["sex"] == "female")&(used_data["age_type"] == 0),"LE"].values[0]),
       "{:.1f}".format(used_data.loc[(used_data["sex"] == "female")&(used_data["age_type"] == 0),"HALE"].values[0]),
       "{:.1f}".format(used_data.loc[(used_data["sex"] == "female")&(used_data["age_type"] == 60),"LE"].values[0]),
       "{:.1f}".format(used_data.loc[(used_data["sex"] == "female")&(used_data["age_type"] == 60),"HALE"].values[0]),
    ]

@callback(
    Output('download-store', 'data', allow_duplicate=True),
    [Input("dt-dd", "value"),
     Input("type-dd", "value"),
     Input('year-dd-dt', 'value'),
     Input('dt-store', 'data')],
    prevent_initial_call=True
)
def update_data(dt, type_code, selected_year, dt_data):
    dt_df = pd.DataFrame(dt_data)
    used_data = dt_df.loc[(dt_df['year'] == selected_year-543) &
                          (dt_df["district_number"] == int(dt))]
    return used_data.to_dict('records')

