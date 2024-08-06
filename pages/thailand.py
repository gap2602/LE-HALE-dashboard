import dash
from dash import dcc, html, callback
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/")

layout = html.Div(children=[
            html.H2(children='อายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) ระดับประเทศปี พ.ศ. 2562 (หน่วย: ปี)', className="section-name", id="section-name-thailand"),
            html.Div(children=[
                html.Div(children=[
                    html.Div(children=[
                        html.H3(children='เลือกปี พ.ศ.', id="year-filter-title-th"),
                        dcc.Dropdown([], clearable=False, id="year-dd-th")   
                    ], id="year-filter-th"),
                    html.Div(children=["เมื่อแรกเกิด (at birth)"], id="at-birth-name"),
                    html.Div(children=["เมื่ออายุ 60 ปี"], id="at-60-name"),
                ], id="filter-and-type"),
                html.Div(children=[
                    html.Div([
                        html.Div([
                            html.Img(src=dash.get_asset_url("Page1 - Both-sex.png"), className="sex-pic")
                        ], className="sex-pic-frame"),
                        html.Div(children=["รวมเพศ"], className="sex-type"),
                    ], className="section-name-frame"),
                    html.Div([
                        html.Div(children=[dcc.Graph(id="both-at-birth", config={'displayModeBar': False})]),
                        html.Div(children=[
                            html.Div(children=["LE", html.Br(), html.Div(id='both-at-birth-le')], className="card-box-left"),
                            html.Div(children=["HALE", html.Br(), html.Div(id='both-at-birth-hale')], className="card-box-right"),
                        ], className="numbers")
                    ], className="type-block", id="both-birth-block"),
                    html.Div([
                        html.Div(children=[dcc.Graph(id="both-at-60", config={'displayModeBar': False})]),
                        html.Div(children=[
                            html.Div(children=["LE", html.Br(), html.Div(id='both-at-60-le')], className="card-box-left"),
                            html.Div(children=["HALE", html.Br(), html.Div(id='both-at-60-hale')], className="card-box-right")
                        ], className="numbers")
                    ], className="type-block", id="both-60-block"),   
                ], id="both-section"),
                html.Div(children=[
                    html.Div([
                        html.Div([
                            html.Img(src=dash.get_asset_url("Page1 - Male.png"), className="sex-pic")
                        ], className="sex-pic-frame"),
                        html.Div(children=["เพศชาย"], className="sex-type"),
                    ], className="section-name-frame"),
                    html.Div([
                        html.Div(children=[dcc.Graph(id="male-at-birth", config={'displayModeBar': False})]),
                        html.Div(children=[
                            html.Div(children=["LE", html.Br(), html.Div(id='male-at-birth-le')], className="card-box-left"),
                            html.Div(children=["HALE", html.Br(), html.Div(id='male-at-birth-hale')], className="card-box-right"),
                        ], className="numbers"),
                    ], className="type-block", id="male-birth-block"),          
                    html.Div([
                        html.Div(children=[dcc.Graph(id="male-at-60", config={'displayModeBar': False})]),
                        html.Div(children=[
                            html.Div(children=["LE", html.Br(), html.Div(id='male-at-60-le')], className="card-box-left"),
                            html.Div(children=["HALE", html.Br(), html.Div(id='male-at-60-hale')], className="card-box-right")
                        ], className="numbers"),
                    ], className="type-block", id="male-60-block"),   
                ], id="male-section"),
                html.Div(children=[
                    html.Div([
                        html.Div([
                            html.Img(src=dash.get_asset_url("Page1 - Female.png"), className="sex-pic")
                        ], className="sex-pic-frame"),
                        html.Div(children=["เพศหญิง"], className="sex-type"),
                    ], className="section-name-frame"),
                    html.Div([
                        html.Div(children=[dcc.Graph(id="female-at-birth", config={'displayModeBar': False})]),
                        html.Div(children=[
                            html.Div(children=["LE", html.Br(), html.Div(id='female-at-birth-le')], className="card-box-left"),
                            html.Div(children=["HALE", html.Br(), html.Div(id='female-at-birth-hale')], className="card-box-right"),
                        ], className="numbers")
                    ], className="type-block", id="female-birth-block"),
                    html.Div([
                        html.Div(children=[dcc.Graph(id="female-at-60", config={'displayModeBar': False})]),
                        html.Div(children=[
                            html.Div(children=["LE", html.Br(), html.Div(id='female-at-60-le')], className="card-box-left"),
                            html.Div(children=["HALE", html.Br(), html.Div(id='female-at-60-hale')], className="card-box-right")
                        ], className="numbers")
                    ], className="type-block", id="female-60-block"),          
                ], id="female-section")          
            ], className="content-block")
        ], className="page-1")

def gen_bar_chart(data, age_type, sex, color_left, color_right):
    filtered_data = data.loc[(data['age_type'] == age_type) &
                             (data['sex'] == sex)]
    fig = px.bar( x=['<b>LE</b>', '<b>HALE</b>'], y = filtered_data[['LE','HALE']].values[0], text_auto=True)
    fig.update_yaxes(range=[0,100])
    fig.update_traces(textfont_size=14, textangle=0, textposition="outside", texttemplate="%{value:.1f}",
                      textfont_weight='bold', marker_color=[color_left, color_right], 
                      textfont_color=[color_left, color_right], marker_line_width = 0,
                      hovertemplate=None)
    fig.update_layout(xaxis=dict(showgrid=False, title=None, fixedrange = True),
                      yaxis=dict(showgrid=False, visible=False, fixedrange = True),
                      margin=dict(l=80, r=80, t=0, b=0), bargap=0, font_family="IBM Plex Sans Thai",
                      hoverlabel_font=dict(color='black', family="IBM Plex Sans Thai"),
                      hoverlabel_bordercolor="black",
                      plot_bgcolor='#f7f8f8', paper_bgcolor='#f7f8f8')

    return fig

def get_values(data, age_type, sex, metric):
        filtered_data = data.loc[(data['age_type'] == age_type) &
                                 (data['sex'] == sex)]
        return filtered_data[metric].values[0]

@callback(
    [Output("year-dd-th", "options"),
     Output("year-dd-th", "value")],
    Input("ov-store", "data")
)
def update_year_dropdown(data):
    temp_df = pd.DataFrame(data)
    min_year = min(temp_df['year']) + 543
    max_year = max(temp_df['year']) + 543

    return [{'label':year, 'value':year} for year in range(min_year, max_year+1)], min_year

@callback(
     [Output('section-name-thailand', 'children'),
      Output('both-at-birth-le', 'children'),
      Output('both-at-birth-hale', 'children'),
      Output('both-at-60-le', 'children'),
      Output('both-at-60-hale', 'children'),
      Output('male-at-birth-le', 'children'),
      Output('male-at-birth-hale', 'children'),
      Output('male-at-60-le', 'children'),
      Output('male-at-60-hale', 'children'),
      Output('female-at-birth-le', 'children'),
      Output('female-at-birth-hale', 'children'),
      Output('female-at-60-le', 'children'),
      Output('female-at-60-hale', 'children'),
      Output('both-at-birth', 'figure'),
      Output('both-at-60', 'figure'),
      Output('male-at-birth', 'figure'),
      Output('male-at-60', 'figure'),
      Output('female-at-birth', 'figure'),
      Output('female-at-60', 'figure')],
     [Input('year-dd-th', 'value'),
      Input("ov-store", "data")],
)
def update_chart(selected_year, data):
    ov_df = pd.DataFrame(data)
    min_year = min(ov_df['year']) + 543

    if selected_year:
        use_value = selected_year
    else:
        use_value = min_year
    value_data = ov_df.loc[ov_df['year'] == (use_value-543)]

    b_cl_dark = "#84b81a"
    b_cl_light = "#a3e025"
    m_cl_dark = "#1a84b8"
    m_cl_light = "#25a3e0"
    fm_cl_dark = "#b81a84"
    fm_cl_light = "#e025a3"
    
    fig_1 = gen_bar_chart(value_data, 0, 'bothsex', b_cl_dark, b_cl_light)
    fig_2 = gen_bar_chart(value_data, 60, 'bothsex', b_cl_dark, b_cl_light)
    fig_3 = gen_bar_chart(value_data, 0, 'male', m_cl_dark, m_cl_light)
    fig_4 = gen_bar_chart(value_data, 60, 'male', m_cl_dark, m_cl_light)
    fig_5 = gen_bar_chart(value_data, 0, 'female', fm_cl_dark, fm_cl_light)
    fig_6 = gen_bar_chart(value_data, 60, 'female', fm_cl_dark, fm_cl_light)
    
    return ['อายุคาดเฉลี่ย (LE) และอายุคาดเฉลี่ยของการมีสุขภาวะ (HALE) ระดับประเทศปี พ.ศ. ' + str(selected_year) + ' (หน่วย: ปี)',
            html.Div("{:.1f}".format(get_values(value_data, 0, 'bothsex', 'LE')), id='both-at-birth-le', style={'color' : b_cl_dark}),
            html.Div("{:.1f}".format(get_values(value_data, 0, 'bothsex', 'HALE')), id='both-at-birth-hale', style={'color' : b_cl_light}),
            html.Div("{:.1f}".format(get_values(value_data, 60, 'bothsex', 'LE')), id='both-at-60-le', style={'color' : b_cl_dark}),
            html.Div("{:.1f}".format(get_values(value_data, 60, 'bothsex', 'HALE')), id='both-at-60-hale', style={'color' : b_cl_light}),
            html.Div("{:.1f}".format(get_values(value_data, 0, 'male', 'LE')), id='male-at-birth-le', style={'color' : m_cl_dark}),
            html.Div("{:.1f}".format(get_values(value_data, 0, 'male', 'HALE')), id='male-at-birth-hale', style={'color' : m_cl_light}),
            html.Div("{:.1f}".format(get_values(value_data, 60, 'male', 'LE')), id='male-at-60-le', style={'color' : m_cl_dark}),
            html.Div("{:.1f}".format(get_values(value_data, 60, 'male', 'HALE')), id='male-at-60-hale', style={'color' : m_cl_light}),
            html.Div("{:.1f}".format(get_values(value_data, 0, 'female', 'LE')), id='female-at-birth-le', style={'color' : fm_cl_dark}),
            html.Div("{:.1f}".format(get_values(value_data, 0, 'female', 'HALE')), id='female-at-birth-hale', style={'color' : fm_cl_light}),
            html.Div("{:.1f}".format(get_values(value_data, 60, 'female', 'LE')), id='female-at-60-le', style={'color' : fm_cl_dark}),
            html.Div("{:.1f}".format(get_values(value_data, 60, 'female', 'HALE')), id='female-at-60-hale', style={'color' : fm_cl_light}),
            fig_1,
            fig_2,
            fig_3,
            fig_4,
            fig_5,
            fig_6
           ]

@callback(
    Output('download-store', 'data', allow_duplicate=True),
    [Input('year-dd-th', 'value'),
     Input('ov-store', 'data')],
    prevent_initial_call=True
)
def update_data(value, data):
    used_data = pd.DataFrame(data)
    return used_data.to_dict('records')
