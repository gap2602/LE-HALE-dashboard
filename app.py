import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
import pandas as pd

# path
OVERVIEW_PATH = r"data\country.csv"
DISTRICT_PATH = r"data\district.csv"
AREA_CODE_PATH = r"data\area code.csv"
PROVINCE_PATH = r"data\province.csv"
MAP_PATH = r"data\province_lat_lon.csv"

# read data
ov_df = pd.read_csv(OVERVIEW_PATH)
dt_df = pd.read_csv(DISTRICT_PATH)
pv_df = pd.read_csv(PROVINCE_PATH)
ac_df = pd.read_csv(AREA_CODE_PATH)
map_df = pd.read_csv(MAP_PATH)

# join
pv_df["pv_name"] = pv_df["pv_name"].str.upper()
pv_w_code_df = pd.merge(pv_df, ac_df, how="left", left_on="pv_name", right_on="eng_province")
pv_w_code_df = pv_w_code_df[['year', 'post_code', 'sex', 'LE', 'HALE', 'LE-HALE', 'age_type', 
                             'th_province', 'eng_province', 'area_code' ]]
pv_w_code_df = pd.merge(pv_w_code_df, map_df, how="left", on="post_code")
pv_w_code_df = pv_w_code_df[['year', 'post_code', 'sex', 'LE', 'HALE', 'LE-HALE', 'age_type', 
                             'th_province', 'eng_province', 'area_code', 'lat', 'lon']]

#transform
pv_w_code_df["district_number"] = pv_w_code_df["area_code"].apply(lambda x: x.split()[1])
pv_w_code_df["district_number"] = pv_w_code_df["district_number"].astype(int)
pv_w_code_df["sex"] = pv_w_code_df["sex"].apply(lambda x: "male" if x == 1 else "female")
pv_w_code_df.loc[pv_w_code_df["age_type"] == "60-64", "age_type"] = 60
pv_w_code_df["age_type"] = pv_w_code_df["age_type"].astype(int)

app = Dash(__name__, external_stylesheets=['assets/app_style.css'], use_pages=True)

app.layout = html.Div(children=[
    html.H1(children='อายุคาดเฉลี่ย และอายุคาดเฉลี่ยของการมีสุขภาวะของประชากรไทย พ.ศ. - ระดับประเทศและจังหวัด', className="header", id="main-header"),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(["รายละเอียด"],className="menu-name", id="menu-topic"),
                dcc.Location(refresh=False, id="url"),
                dcc.Link(children=[
                    html.Img(src=dash.get_asset_url("Menu - Thailand.png"), className="menu-pic", id="thai-map")
                ], className="pic-frame", id="thai-map-frame", href="/", style={'background-color': '#0874b0'}),
                html.H4(["LE และ HALE",html.Br()," ระดับประเทศ"], className="menu-name"),
                dcc.Link(children=[
                    html.Img(src=dash.get_asset_url("Menu - Province.png"), className="menu-pic")
                ], className="pic-frame", id="province-frame", href="/district-province/district", style={'background-color': 'gray'}),
                html.H4("LE และ HALE เขตสุขภาพและจังหวัด", className="menu-name"),
                dcc.Link(children=[
                    html.Img(src=dash.get_asset_url("Menu - trend.png"), className="menu-pic")
                ], className="pic-frame", id="trend-frame", href="/trend/trend-country", style={'background-color': 'gray'}),
                html.H4("แนวโน้ม LE และ HALE", className="menu-name")
            ], id="menu-panel"),
            html.Div([
                html.Div([
                    html.Img(src=dash.get_asset_url("Menu - Export File.png"), id="export-pic")
                ], id="export-pic-frame"),
                dcc.Store(id="download-store", storage_type="session"),
                dcc.Store(id="ov-store", storage_type="session", data=ov_df.to_dict('records')),
                dcc.Store(id="dt-store", storage_type="session", data=dt_df.to_dict('records')),
                dcc.Store(id="pv-store", storage_type="session", data=pv_w_code_df.to_dict('records')),
                html.Button("Export Data", id="export-btn"),
                dcc.Download(id="download-dataframe-csv")
            ], id="export-frame"),    
        ], id="nav-panel"),
        html.Div([dash.page_container], id="page-container")
    ], id="section-block"),

    html.Div(children=[html.P("หมายเหตุ:", className="remark-topic"),
                      html.Div([
                          html.P("อายุคาดเฉลี่ย (Life Expectancy: LE)", className="cal-type"),
                          html.P([
                              html.P("i", className="i-icon"),
                              html.Span(["•	อายุคาดเฉลี่ยเมื่อแรกเกิด (Life Expectancy at birth) หมายถึง ค่าเฉลี่ยของจำนวนปีที่คาดว่าประชากรจะมีชีวิตอยู่ตั้งแต่แรกเกิดจนกระทั่งเสียชีวิต",
                                         html.P(),
                                         "•	อายุคาดเฉลี่ยเมื่ออายุ 60 ปี (Life expectancy at age 60 years) หมายถึง ค่าเฉลี่ยของจำนวนปีที่คาดว่าประชากรจะมีชีวิตอยู่เมื่ออายุ 60 ปี จนกระทั่งเสียชีวิต"], className="tooltip", id="tooltip-1")
                          ], className="info-icon", id="info-1")
                      ], className="text-info"),
                      html.P("หมายถึง ค่าเฉลี่ยของจำนวนปีที่คาดว่าประชากรจะมีชีวิตอยู่จนกระทั่งเสียชีวิต", className="meaning"),
                      html.Div([
                          html.P("อายุคาดเฉลี่ยของการมีสุขภาวะ (Health-Adjusted Life Expectancy: HALE)", className="cal-type"),
                          html.P([
                              html.P("i", className="i-icon"),
                              html.Span(["• อายุคาดเฉลี่ยของการมีสุขภาวะที่เมื่อแรกเกิด (Health-Adjusted Life Expectancy at birth) หมายถึง ค่าเฉลี่ยของจำนวนปีที่คาดว่าประชากรจะมีชีวิตอยู่อย่างมีสุขภาพที่สมบูรณ์ตั้งแต่แรกเกิดจนกระทั่งเสียชีวิต",
                                         html.P(),
                                         "•	อายุคาดเฉลี่ยของการมีสุขภาวะที่ปรับด้วยสุขภาพเมื่ออายุ 60 ปี (Health-Adjusted Life Expectancy at age 60 years) หมายถึง ค่าเฉลี่ยของจำนวนปีที่คาดว่าประชากรจะมีชีวิตอยู่อย่างมีสุขภาพที่สมบูรณ์อยู่เมื่ออายุ 60 ปี จนกระทั่งเสียชีวิต"], className="tooltip", id="tooltip-2")
                          ], className="info-icon", id="info-2"),
                      ], className="text-info"),
                      html.P("หมายถึง ค่าเฉลี่ยของจำนวนปีที่คาดว่าประชากรจะมีชีวิตอยู่อย่างมีสุขภาพที่สมบูรณ์จนกระทั่งเสียชีวิต", className="meaning"),
                      html.P("อ้างอิง:", className="remark-topic"),
                      html.P("รายงานอายุคาดเฉลี่ย (Life Expectancy: LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (Health Adjusted Life Expectancy: HALE) ของประชากรไทย พ.ศ. 2562-2565 สํานักงานพัฒนานโยบายสุขภาพระหว่างประเทศ กลุ่มงานพัฒนาดัชนีภาระโรคแห่งประเทศไทย", id="ref-text")
    ], className="remark"),

    html.Div(children=[
        html.Div(children=[
                    html.P(children=[html.B("จัดทำเนื้อหา โดย "),
                                     html.Br(),
                                     "สํานักงานพัฒนานโยบายสุขภาพระหว่างประเทศ กลุ่มงานพัฒนาดัชนีภาระโรคแห่งประเทศไทย",
                                     html.Br(),
                                     html.B("สนับสนุน โดย "),
                                     html.Br(),
                                     "สำนักงานคณะกรรมการส่งเสริมวิทยาศาสตร์ วิจัยและนวัตกรรม (สกสว.)"])
        ], id="footer-text"),
        html.Div(children=[
                    html.Img(src=dash.get_asset_url("IHPP.png"), className="footer-logo"),
                    html.Img(src=dash.get_asset_url("BOD.png"), className="footer-logo"),
                    html.Img(src=dash.get_asset_url("MOPH.png"), className="footer-logo"),
                    html.Img(src=dash.get_asset_url("TSRI.png"), className="footer-logo"),
                    html.Img(src=dash.get_asset_url("ThaiHealth.png"), className="footer-logo")
        ], id="footer-logo-frame")
    ], id="footer")
])

@app.callback(
    Output("main-header", "children"),
    Input("dt-store", "data")
)
def update_main_title(data_df):
    temp_df = pd.DataFrame(data_df)
    min_year = min(temp_df['year']) + 543
    max_year = max(temp_df['year']) + 543
    return 'อายุคาดเฉลี่ย และอายุคาดเฉลี่ยของการมีสุขภาวะของประชากรไทย พ.ศ. '+str(min_year)+'-'+str(max_year)+' ระดับประเทศและจังหวัด'

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("export-btn", "n_clicks"),
    State("download-store", "data"),
    prevent_initial_call=True,
)
def export_data(n_clicks, data):
    temp_df = pd.DataFrame(data)
    return dcc.send_data_frame(temp_df.to_csv, "test.csv", index=False)

@app.callback([
     Output("thai-map-frame", "style"),
     Output("province-frame", "style"),
     Output("trend-frame", "style")
     ],
    Input("url", "pathname"), prevent_initial_call=True
)
def change_color_nav(path):
    colors = ['#0874b0', 'gray', 'gray']
    if path.startswith("/district-province"):
        colors = ['gray', '#0874b0', 'gray']
    elif path.startswith("/trend"):
        colors = ['gray', 'gray', '#0874b0']
    else:
        colors = ['#0874b0', 'gray', 'gray']

    return [{'background-color': c} for c in colors]
    

if __name__ == '__main__':
    app.run_server(debug=True)
