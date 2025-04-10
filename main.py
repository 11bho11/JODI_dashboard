from utilities import support_functions as sf
from dash import dcc, html, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
import datetime as dt


############################# LAYOUT ################################################
title = html.Div(
            html.H1('JODI', style={'textAlign': 'center'})
            )

controls = html.Div([
    html.Div([
        html.H5('Pick a Country'),
        dcc.Dropdown(
                    options = [
                        {'label': i, 'value': j} for i,j in sf.country_dict.items()
                        ],
                    value = 'USA',
                    id='country_id',
                    className='dropdowns',
                    clearable=False
                    ),
    ]),
    html.Div([
        html.H5('Filter by Energy'),
        dcc.Dropdown(
                    options = sf.energy_list, 
                    value = sf.energy_list[0],
                    id='energy_id',
                    className='dropdowns',
                    clearable=False
                    ),
    ]),
    html.Div([
        html.H5('Filter by Unit'),
        dcc.Dropdown(
                   value= 'Thousand Barrels per day (kb/d)',
                   id='unit_id',
                   className='dropdowns'
                   ),
    ]),
    html.Div([
        html.H5('Filter by Time Period'),
    ]),
    html.Div([
        html.H6('From'),
        dcc.Input(
                value = '2023-01-01',
                placeholder ='YYYY-MM-DD', 
                type='text',
                id = 'date_from_id',
                className='inputs'
                ),
        ],
        style = {
                'display':'flex'
                },
        ),
    html.Div([
        html.H6('To'),
        dcc.Input(
                value = dt.datetime.now().strftime("%Y-%m-%d"), 
                placeholder='YYYY-MM-DD',
                type='text',
                id = 'date_to_id',
                className='inputs'
                ), 
    ],
    style = {
            'display':'flex'
            },
    )
],
className= 'controls_box'
)


summary = html.Div([
    html.H5('Country-level Summary'),
    html.H5(id='asofdate_id',
            style={'margin-top':'0px',
                   'margin-bottom':'20px'}
            ),
    dcc.Loading(
                type='circle',
                children=html.Div(id='summary_id')
                )
    ],
    className= 'summary_box'
    )



line_chart = html.Div([
    html.Div([
        html.H5(
            'Product Breakdown', 
            style={'margin-top':'10px'}
            ),
        dcc.Dropdown(
                value = 'Crude Oil',
                id='product_id',
                className='dropdowns'
                )
    ], 
    style = {
            'display':'flex'
            }
    ),
    dcc.Loading(
            type='circle',
            children=dcc.Graph(
                    figure={}, 
                    id='line_chart_id',
                    className='line_chart'
                    ))
]
)

bar_chart = html.Div([
    html.Div([
        html.H5(
            'Flow Breakdown',    
            style={'margin-top':'10px'}
            ),
        dcc.Dropdown(
                value = 'Production',
                id='flow_id',
                className='dropdowns',
                )
    ],
    style = {
            'display':'flex'
            }
    ),
    dcc.Loading(
            type='circle',
            children=dcc.Graph(
                    figure={}, 
                    id='bar_chart_id',
                    className='bar_pie_chart'
                    ))
]
)

percentage_chart = html.Div([
    dcc.Loading(
            type='circle',
            children=html.H6(id='percentage_id')
            )
])




app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])

app.layout = dbc.Container([
    title,
    html.Div([
        html.Div([
                controls,
                summary
                ],
                className='column_left'
                ),

        html.Div([
                line_chart,
                html.Div([
                        bar_chart,
                        percentage_chart
                        ],
                        style = {
                        'display':'flex'
                        }),
                ],
                className='column_right'
        )
    ], 
    style = {
            'display':'flex',
            })
],
fluid=True,
className='dashboard_container'
)



############################# CALLBACKS ################################################

@app.callback(
    Output(component_id='summary_id', component_property='children'),
    Output(component_id='asofdate_id', component_property='children'),
    Input(component_id='energy_id', component_property='value'),
    Input(component_id='country_id', component_property='value')
)
def update_summary(energy, country):
    summary, max_date = sf.get_summary_data(energy, country)
    return [html.H6(line) for line in summary], f'({max_date})'


@app.callback(
    Output(component_id='product_id', component_property='style'),
    Input(component_id='energy_id', component_property='value')
)
def hide_product_id(energy):
    if energy == sf.energy_list[2]:
        return {'display': 'none'} 
    return {'display': 'block'}  



@callback(
    Output(component_id='unit_id', component_property='options'),
    Input(component_id='energy_id', component_property='value'),
)
def update_unit_id(energy):
    if energy in [sf.energy_list[0],sf.energy_list[1]]:
        return [{'label': i, 'value': i} for i in sf.oil_units_dict.keys()]
    elif energy == sf.energy_list[2]:
        return [{'label': i, 'value': i} for i in sf.gas_units_dict.keys()]



@callback(
    Output(component_id='product_id', component_property='options'),
    Input(component_id='energy_id', component_property='value'),
)
def update_product_id(energy):
    if energy == sf.energy_list[0]:
        return [{'label': i, 'value': i} for i in list(sf.primary_oil_products_dict.keys())]
    elif energy == sf.energy_list[1]:
        return [{'label': i, 'value': i} for i in list(sf.secondary_oil_products_dict.keys())]
    elif energy == sf.energy_list[2]:
        return []


@callback(
    Output(component_id='flow_id', component_property='options'),
    Input(component_id='energy_id', component_property='value'),
)
def update_flow_id(energy):
    if energy == sf.energy_list[0]: 
        return [{'label': i, 'value': i} for i in sf.primary_oil_flow_dict.keys()]
    elif energy == sf.energy_list[1]:
        return [{'label': i, 'value': i} for i in sf.secondary_oil_flow_dict.keys()]
    elif energy  == sf.energy_list[2]:
        return [{'label': i, 'value': i} for i in sf.gas_flow_dict.keys()]
    


@callback(
    Output(component_id='line_chart_id', component_property='figure'),
    Input(component_id='energy_id', component_property='value'),
    Input(component_id='country_id', component_property='value'),
    Input(component_id='unit_id', component_property='value'),
    Input(component_id='date_from_id', component_property='value'),
    Input(component_id='date_to_id', component_property='value'),
    Input(component_id='product_id', component_property='value'),
)
def update_line_chart_id(energy, country, unit, date_from, date_to, product):
    return sf.make_line_chart(energy, country, unit, date_from, date_to, product)


@callback(
    Output(component_id='bar_chart_id', component_property='figure'),
    Input(component_id='energy_id', component_property='value'),
    Input(component_id='country_id', component_property='value'),
    Input(component_id='unit_id', component_property='value'),
    Input(component_id='date_from_id', component_property='value'),
    Input(component_id='date_to_id', component_property='value'),
    Input(component_id='flow_id', component_property='value'),
    Input(component_id='product_id', component_property='value'),
)
def update_bar_chart_id(energy, country, unit, date_from, date_to, flow, product):
    return sf.make_bar_chart(energy, country, unit, date_from, date_to, flow, product)




@callback(
    Output(component_id='percentage_id', component_property='children'),
    Input(component_id='energy_id', component_property='value'),
    Input(component_id='country_id', component_property='value'),
    Input(component_id='unit_id', component_property='value'),
    Input(component_id='date_from_id', component_property='value'),
    Input(component_id='date_to_id', component_property='value'),
    Input(component_id='flow_id', component_property='value'),
)
def update_percentage_id(energy, country, unit, date_from, date_to, flow):
    return sf.make_percentage(energy, country, unit, date_from, date_to, flow)




if __name__ == '__main__':
    app.run(debug=True)



