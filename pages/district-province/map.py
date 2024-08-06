import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

with open('thailand_map.json', encoding="utf-8") as f:
  thai_json = json.load(f)

dash.register_page(__name__, name="map", path="/district-province/map")

layout = html.Div(children=[
    html.H2(children='อายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) ระดับประเทศปี พ.ศ. 2562 (หน่วย: ปี)', className="section-name", id="section-name-map"),
    html.Div([
        html.Div([
            html.H3(children = 'เลือกปี พ.ศ.', className="year-filter-title"),
            dcc.Dropdown(searchable=False, clearable=False, id="year-dd-map")     
        ], className="year-filter"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - Overview.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลภาพรวม', className="tab-name"),
        ], href="/district-province/district", style={'background-color': '#dadee7', 
                                                      'border' : 'solid 3px #aeb2b7'}, id="tab1-map"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - map.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลแผนที่', className="tab-name"),
        ], href="/district-province/map", style={'background-color': '#bbdee4',
                                                 'border' : 'solid 3px #1aa2b6'}, id="tab2-map"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - Table.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลมีตาราง', className="tab-name"),
        ], href="/district-province/table", style={'background-color': '#dadee7',
                                                   'border' : 'solid 3px #aeb2b7'}, id="tab3-map")
    ], className="year-filter-and-tabs"),
    html.Div([
        html.Div([
            html.Div("เลือก", className="filter-panel-name"),
            html.Div([
                html.H4("เขตสุขภาพ", className="filter-name"),
                dcc.Dropdown(id='dt-dd-map', clearable=False)
            ], id="dt-filter-map"),
            html.Div([
                html.H4("อายุคาดเฉลี่ย", className="filter-name"),
                dcc.Dropdown({'LE':'LE', 'HALE':'HALE'},'LE', id='metric-dd-map', 
                             clearable=False)
            ], id="metric-filter-map"),
            html.Div([
                html.H4("การคำนวณ", className="filter-name"),
                dcc.Dropdown({'0':"เมื่อแรกเกิด (at birth)", '60':"เมื่ออายุ 60 ปี"},'0', id='type-dd-map', 
                             clearable=False)
            ], id="type-filter-map"),
            html.Div([
                html.H4("เพศ", className="filter-name"),
                dcc.Dropdown({'male':'เพศชาย', 'female':'เพศหญิง'},'male', id='sex-dd-map', 
                             clearable=False)
            ], id="sex-filter-map"),
        ], id="filter-panel-map"),
        html.Div([
            dcc.Graph(id="map", style={'background-color': '#f0f1f3'}, config={'displayModeBar': False}),
            html.Div(id="map-table")
        ], id="map-block")
    ], className="filter-and-content-block"),
], className="page-2-map")

@callback(
    [Output("year-dd-map", "options"),
     Output("year-dd-map", "value"),
     Output("dt-dd-map", "options"),
     Output("dt-dd-map", "value")],
     Input("pv-store", "data")
)
def update_dropdown_map(data):
    temp_df = pd.DataFrame(data)
    min_year = min(temp_df['year']) + 543
    max_year = max(temp_df['year']) + 543
    all_dt_dict = {**{'all': 'ทุกเขตสุขภาพ'}, **{dt.split()[1] : dt for dt in temp_df["area_code"].unique().tolist()}}

    return [
        [{'label':year, 'value':year} for year in range(min_year, max_year+1)], 
        min_year, 
        all_dt_dict, 
        '1'
    ]

@callback(
    Output("section-name-map", "children"),
    Input("year-dd-map", "value")
)
def update_title_name_map(selected_year):
    return 'อายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) ระดับประเทศปี พ.ศ. ' + str(selected_year) + ' (หน่วย: ปี)'

@callback(
    Output("map", "figure"),
   [Input("year-dd-map", "value"),
    Input("dt-dd-map", "value"),
    Input("metric-dd-map", "value"),
    Input("type-dd-map", "value"),
    Input("sex-dd-map", "value"),
    Input("pv-store", "data")]
)
def update_map(year, dt, metric, age_type, sex, data):
    temp_df = pd.DataFrame(data)
    if dt == 'all':
        used_data = temp_df.loc[(temp_df['year'] == year-543) &
                                (temp_df['age_type'] == int(age_type)) &
                                (temp_df['sex'] == sex)]
    else:
        used_data = temp_df.loc[(temp_df['year'] == year-543) &
                                (temp_df['district_number'] == int(dt)) &
                                (temp_df['age_type'] == int(age_type)) &
                                (temp_df['sex'] == sex)]
        
    fig = px.choropleth(used_data, geojson=thai_json, locations='post_code', 
                        featureidkey="properties.id", color=metric,
                        range_color=(used_data[metric].min(), used_data[metric].max()),
                        color_continuous_scale=["#EFE9F4", "#5078F2"],
                        custom_data=['th_province']
          )
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_traces(hovertemplate='จังหวัด: %{customdata[0]}<br>'+metric+': %{z:.1f}')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, font=dict(size=16, family="IBM Plex Sans Thai"),
                      paper_bgcolor="#f0f1f3")
    fig.update_layout(coloraxis_colorbar=dict(
                                                len=0.7,
                                                xanchor="right", x=1,
                                                yanchor='bottom', y=0.15,
                                                thickness=20,
                                                title_font_weight = 'bold'
                                            ))
    

    if dt != 'all':
        fig.add_scattergeo(lat=used_data['lat'].values,
                        lon=used_data['lon'].values, 
                        text=['<b>'+pv+'</b>'for pv in used_data['th_province'].values], 
                        mode="text", textfont=dict(family="IBM Plex Sans Thai",size=14,color="black"),
                        hoverinfo = 'skip')
    return fig

@callback(
    Output("map-table", "children"),
   [Input("year-dd-map", "value"),
    Input("dt-dd-map", "value"),
    Input("metric-dd-map", "value"),
    Input("type-dd-map", "value"),
    Input("sex-dd-map", "value"),
    Input("pv-store", "data")]
)
def update_map_table(year, dt, metric, age_type, sex, data):
    temp_df = pd.DataFrame(data)
    used_data = temp_df.loc[(temp_df['year'] == year-543) &
                            (temp_df['age_type'] == int(age_type)) &
                            (temp_df['sex'] == sex)]
    columns = [
            {"name": "จังหวัดในเขตสุขภาพ", "id": "province"},
            {"name": metric + " (หน่วย: ปี)", "id": "metric_value"}
    ]
    data = []
    if dt == 'all':     
        for dt_num in range(1,14):
            used_data_2 = used_data.loc[(used_data['district_number'] == dt_num)]
            data.append({'province' : 'เขตสุขภาพ ' + str(dt_num), 'metric_value' : ''})
            temp = [{'province':used_data_2.iloc[i]['th_province'], 'metric_value':"{:.1f}".format(used_data_2.iloc[i][metric])} for i in range(used_data_2.shape[0])]
            data.extend(temp)
    else:
        used_data_2 = used_data.loc[used_data['district_number'] == int(dt)]
        temp = [{'province':used_data_2.iloc[i]['th_province'], 'metric_value':"{:.1f}".format(used_data_2.iloc[i][metric])} for i in range(used_data_2.shape[0])]
        data.append({'province' : "เขตสุขภาพ " + str(dt), 'metric_value' : ''})
        data.extend(temp)

    return dash_table.DataTable(columns=columns, data= data, fixed_rows={'headers': True}, cell_selectable=False,
                                style_table={'width':'100%', 'height':'365px', 'overflowX':'hidden','overflowY': 'auto'},
                                style_header={'backgroundColor': '#808080','fontWeight': 'bold', 'fontSize':16, 'color':'white', 'textAlign': 'center'},
                                style_cell={'fontSize':16, 'font-family':'IBM Plex Sans Thai'},
                                style_data_conditional=[{'if': {'column_id': 'province', 'filter_query': '{province} contains "เขต"'},
                                                         'fontWeight': 'bold'
                                                        }],
                                style_cell_conditional=[
                                                    {'if': {'column_id': 'province'},
                                                     'textAlign': 'left', 'width': '60%'},
                                                    {'if': {'column_id': 'metric_value'},
                                                     'textAlign': 'center', 'width': '40%'},   
                                ]
            )
    