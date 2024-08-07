import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output
import pandas as pd

AREA_CODE_PATH = "data/area code.csv"
ac_df = pd.read_csv(AREA_CODE_PATH)
province_dict = ac_df.set_index("eng_province")["th_province"].to_dict()
province_label = [{'label': th_pv,'value': eng_pv,'search': th_pv} for eng_pv, th_pv in province_dict.items()]

dash.register_page(__name__, name="table", path="/district-province/table")

layout = html.Div(children=[
    html.H2(children='อายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) ระดับประเทศปี พ.ศ. 2562 (หน่วย: ปี)', className="section-name", id="section-name-table"),
    html.Div([
        html.Div(id = "year-filter-margin"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - Overview.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลภาพรวม', className="tab-name"),
        ], href="/district-province/district", style={'background-color': '#dadee7', 
                                                      'border' : 'solid 3px #aeb2b7'}, id="tab1-table"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - map.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลแผนที่', className="tab-name"),
        ], href="/district-province/map", style={'background-color': '#dadee7',
                                                 'border' : 'solid 3px #aeb2b7'}, id="tab2-table"),
        dcc.Link(children=[
            html.Img(src=dash.get_asset_url("Page2 - Table.png"), className="tab-pic"),
            html.H2(children = 'ข้อมูลตาราง', className="tab-name"),
        ], href="/district-province/table", style={'background-color': '#bbdee4',
                                                   'border' : 'solid 3px #1aa2b6'}, id="tab3-table")
    ], className="year-filter-and-tabs"),
    html.Div([
        html.Div([
            html.Div("เลือก", className="filter-panel-name"),
            html.Div([
                html.H4(children = 'เลือกปี พ.ศ.', className="filter-name"),
                dcc.Dropdown(id="year-dd-table", multi=True)     
            ], id="year-filter-table"),
            html.Div([
                html.H4("เขตสุขภาพ", className="filter-name"),
                dcc.Dropdown(id='dt-dd-table', multi=True)
            ], id="dt-filter-table"),
            html.Div([
                html.H4("จังหวัด", className="filter-name"),
                dcc.Dropdown(id='pv-dd-table', multi=True, optionHeight=20)
            ], id="pv-filter-table")
        ], id="filter-panel-table"),
        dash_table.DataTable(id="table-block", merge_duplicate_headers=True, fixed_rows={'headers': True}, 
                             fixed_columns={'headers': True, 'data': 4},
                             style_table={'minWidth':'100%', 'height':'100%', 'overflowX':'auto', 'overflowY':'auto'},
                             style_header={'backgroundColor': '#1aa4b8','fontWeight': 'bold', 
                                           'fontSize':16, 'color':'white', 'textAlign':'center'},
                             style_cell={'fontSize':16, 'font-family':'IBM Plex Sans Thai','textAlign':'center'},
                            ) 
    ], className="filter-and-content-block"),
], className="page-2-table")

@callback(
    [Output("year-dd-table", "options"),
     Output("year-dd-table", "value"),
     Output("pv-dd-table", "options"),
     Output("pv-dd-table", "value"),
     Output("dt-dd-table", "options"),
     Output("dt-dd-table", "value")],
     Input("pv-store", "data")
)
def update_dropdown_map(data):
    temp_df = pd.DataFrame(data)
    min_year = min(temp_df['year']) + 543
    max_year = max(temp_df['year']) + 543

    return [ 
        [{'label':year, 'value':year} for year in range(min_year, max_year+1)],
        [min_year],
        province_label,
        ['BANGKOK'],
        {dt.split()[1] : dt for dt in temp_df["area_code"].unique().tolist()},
        ['1']
    ]
    
@callback(
    [Output("table-block", "columns"),
     Output("table-block", "data"),
     Output("table-block", "style_cell_conditional"),
     Output("table-block", "fixed_columns")
    ],
    [Input("pv-store", "data"),
     Input("year-dd-table", "value"),
     Input("dt-dd-table", "value"),
     Input("pv-dd-table", "value")]
)
def update_table(data, year_list, dt_list, pv_list):
    temp_df = pd.DataFrame(data)
    year_list = [int(i) for i in year_list]
    dt_list = [int(i) for i in dt_list]

    temp_df = temp_df.rename(columns={'th_province':'จังหวัด','area_code':'เขตสุขภาพ'})
    temp_df['ปี'] = temp_df['year'] + 543
    temp_df['การคำนวณ'] = temp_df['age_type'].apply(lambda x:'เมื่อแรกเกิด (at birth)' if x == 0 else 'เมื่ออายุ 60 ปี')
    temp_df['เพศ'] = temp_df['sex'].apply(lambda x: 'เพศชาย' if x == 'male' else 'เพศหญิง')

    filtered_df = temp_df.loc[(temp_df["ปี"].isin(year_list)) &
                                ((temp_df["district_number"].isin(dt_list)) |
                                (temp_df["eng_province"].isin(pv_list)))] 
    
    pivot_df = pd.pivot_table(filtered_df,values=['LE', 'HALE', 'LE-HALE'], 
                        index=['เขตสุขภาพ','จังหวัด','การคำนวณ','เพศ'], 
                        columns='ปี', aggfunc='first').swaplevel(1, 0, axis=1) \
                        .sort_index(level=0, axis=1, sort_remaining=False) \
                        .reindex(['LE', 'HALE', 'LE-HALE'], level=1, axis=1) \
                        .reindex(['เขตสุขภาพ '+str(i) for i in range(1,14)], level=0, axis=0) \
                        .reset_index() 
    
    columns = [
            {"name": ["", "เขตสุขภาพ"], "id": "เขตสุขภาพ"},
            {"name": ["", "จังหวัด"], "id": "จังหวัด"},
            {"name": ["", "การคำนวณ"], "id": "การคำนวณ"},
            {"name": ["ปี", "เพศ"], "id": "เพศ"}
        ] + [{"name": [str(i[0]), str(i[1])], "id":str(i[0])+str(i[1])} for i in pivot_df.columns[4:]]
    
    data =[]
    prev_value = {"เขตสุขภาพ":"", "จังหวัด":"", "การคำนวณ":"", "เพศ":""}
    for idx, row in pivot_df.iterrows():  
        record = {}
        for col in columns:
            if col["id"].startswith('2'):
                temp_rec = {col["id"]: "{:.1f}".format(row[int(col["id"][:4]),col["id"][4:]])}
                record = {**record, **temp_rec}
            else:
                if prev_value[col["id"]] == row[col["id"],""]:
                    temp_rec = {col["id"]: ""}
                    record = {**record, **temp_rec}
                else:
                    temp_rec = {col["id"]: row[col["id"],""]}
                    record = {**record, **temp_rec}
                    prev_value[col["id"]] = row[col["id"],""]
                
        data.append(record)
    
    if filtered_df.shape[0] != 0:
        fixed_columns = {'headers': True, 'data': 4}
    else:
        fixed_columns = {'headers': False}
   
    return [columns, data, 
            [
            {'if': {'column_id': 'เขตสุขภาพ'},
            'textAlign': 'left', 'fontWeight': 'bold', 'width': '10%'},
            {'if': {'column_id': 'จังหวัด'},
            'textAlign': 'left', 'fontWeight': 'bold', 'width': '10%'},
            {'if': {'column_id': 'การคำนวณ'},
            'textAlign': 'left', 'fontWeight': 'bold', 'width': '10%'},
            {'if': {'column_id': 'เพศ'},
            'textAlign': 'left', 'fontWeight': 'bold', 'width': '10%'}
            ] + [{'if' : {'column_id' : col['id']}, 'width' : '75px'} for col in columns if col['id'].endswith("LE")],
            fixed_columns
    ]