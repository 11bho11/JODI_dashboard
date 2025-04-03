import support_functions as sf
from dash import dcc, html, callback, Output, Input
import dash
import dash_bootstrap_components as dbc


############################# LAYOUT ################################################

title_tile = dbc.Row(
        [
            dbc.Col(
                html.Label('1. Select Energy'), 
                width=3
                ),
            dbc.Col(
                html.Label('2. Select Country'), 
                width=3
                ),
            dbc.Col(
                html.Label('3. Select Time Period (YYYY-MM-DD)'), 
                width=3
                )
        ]
    )

selection_tile = dbc.Row(
        [
            dbc.Col(
                    dcc.RadioItems(
                        sf.energy_list, 
                        sf.energy_list[0],
                        id='energy_id'),
                        #width=3
                    ),
            dbc.Col(
                    dcc.Dropdown(
                        [{'label': i, 'value': j} for i,j in sf.country_dict.items()],
                        'GBR',
                        id='country_id'),
                        #width=3
                        ),
            dbc.Col(
                    [
                    #html.Div('From'),
                    dcc.Input(
                        value = '2023-01-01',
                        placeholder ='From', 
                        type='text',
                        id = 'date_from_id'),
                    ],
                    #width=1.5
                    ),
            dbc.Col(
                    [
                    #html.Div('To'),
                    dcc.Input(
                        value = '2025-01-01', 
                        type='text',
                        placeholder='To',
                        id = 'date_to_id')    
                    ],
                    #width=1.5
                    )
        ]
)

upper_option_tile = dbc.Row(
        [
            dbc.Col(
                    dcc.Dropdown(
                   id='up_unit_id',
                   value=None,
                   #placeholder='Select Primary Oil Flow'
                   ),
                   width=3
                   ),
            dbc.Col(
                    dcc.Dropdown(
                   id='up_flow_id',
                   #placeholder='Select Primary Oil Flow'
                   ),
                   width=3
                   ),
            dbc.Col(
                    dcc.Dropdown(
                    id='up_product_id',
                    #placeholder='Select Primary Oil Product'
                    ), 
                    width=3
                    )
        ]
    )

upper_graph_tile = dbc.Row(
        [
            dbc.Col(dcc.Graph(figure={}, id='up_left_graph_id'), width=3),
            dbc.Col(dcc.Graph(figure={}, id='up_right_graph_id'), width=9),
        ]
    )


############################# APP ################################################


app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])

app.layout = dbc.Container(
    [
    html.H1('JODI', style={'textAlign': 'center'}),
    html.Hr(),
    title_tile,
    html.Hr(),
    selection_tile,
    html.Hr(),
    upper_option_tile,
    html.Hr(),
    upper_graph_tile,
    ],
    fluid=True,
    #className='dashboard-container'
)  



@callback(
    Output(component_id='up_unit_id', component_property='options'),
    Input(component_id='energy_id', component_property='value'),
)
def update_up_unit(energy):
    if energy == sf.energy_list[0] or sf.energy_list[1]:
        return [{'label': i, 'value': i} for i in sf.oil_units_dict.keys()]
    elif energy == sf.energy_list[2]:
        return [{'label': i, 'value': i} for i in sf.gas_units_dict.keys()]

@callback(
    Output(component_id='up_flow_id', component_property='options'),
    Input(component_id='energy_id', component_property='value'),
)
def update_up_flow(energy):
    if energy == sf.energy_list[0]: 
        return [{'label': i, 'value': i} for i in sf.primary_oil_flow_dict.keys()]
    elif energy == sf.energy_list[1]:
        return [{'label': i, 'value': i} for i in sf.secondary_oil_flow_dict.keys()]
    elif energy  == sf.energy_list[2]:
        return [{'label': i, 'value': i} for i in ['Imports','Exports']]



@callback(
    Output(component_id='up_product_id', component_property='options'),
    Input(component_id='energy_id', component_property='value'),
)
def update_up_product(energy):
    if energy == sf.energy_list[0]:
        return [{'label': i, 'value': i} for i in list(sf.primary_oil_products_dict.keys())]
    elif energy == sf.energy_list[1]:
        return [{'label': i, 'value': i} for i in list(sf.secondary_oil_products_dict.keys())]
    elif energy == sf.energy_list[2]:
        return []



@callback(
    Output(component_id='up_left_graph_id', component_property='figure'),
    Input(component_id='energy_id', component_property='value'),
    Input(component_id='country_id', component_property='value'),
    Input(component_id='up_unit_id', component_property='value'),
    Input(component_id='date_from_id', component_property='value'),
    Input(component_id='date_to_id', component_property='value'),
    Input(component_id='up_flow_id', component_property='value'),
)
def update_up_left_graph(energy, country, unit, date_from, date_to, flow):
    return sf.make_up_left_graph(energy, country, unit, date_from, date_to, flow)


@callback(
    Output(component_id='up_right_graph_id', component_property='figure'),
    Input(component_id='energy_id', component_property='value'),
    Input(component_id='country_id', component_property='value'),
    Input(component_id='up_unit_id', component_property='value'),
    Input(component_id='date_from_id', component_property='value'),
    Input(component_id='date_to_id', component_property='value'),
    Input(component_id='up_product_id', component_property='value'),
)
def update_up_right_graph(energy, country, unit, date_from, date_to, product):
    return sf.make_up_right_graph(energy, country, unit, date_from, date_to, product)






if __name__ == '__main__':
    app.run(debug=True)



