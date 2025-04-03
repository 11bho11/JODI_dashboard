import nasdaqdatalink
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objects as go
import pycountry
import app_design as des
from dotenv import load_dotenv


###########################################DICTIONARIES#############################################
energy_list = ['Primary Oil', 'Secondary Oil', 'Gas']
country_dict = {i.name: i.alpha_3 for i in pycountry.countries}

primary_oil_products_dict = {
    'Crude Oil': 'CR',
    'NGL': 'NG',
    'Other Primary Oil Products': 'OC',
    'Total Primary Oil Products': 'TC'
    }

secondary_oil_products_dict = {
    'Liquefied petroleum gases': 'LP',
    'Naphtha': 'NA',
    'Motor and aviation gasoline': 'GS',
    'Kerosenes': 'KE',
    'Kerosene type jet fuel': 'JT',
    'Gas/diesel Oil': 'GD',
    'Fuel Oil': 'RS',
    'Other Secondary Oil Products': 'ON',
    'Total Secondary Oil Products': 'TP'
    }

primary_oil_flow_dict = {
    "Production": "PR",
    "From Other Sources": "OS",
    "Imports": "IM",
    "Exports": "EX",
    "Products Transferred": "PT",
    "Direct Use": "DU",
    "Stock Change": "SC",
    "Statistical Difference": "SD",
    "Refinery Intake": "RI",
    "Closing Stock": "CS",
}

secondary_oil_flow_dict = {
    "Refinery Output": "RO",
    "Receipts": "RE",
    "Imports": "IM",
    "Exports": "EX",
    "Products Transferred": "PT",
    "Interproduct Transfers": "IT",
    "Stock Change": "SC",
    "Statistical Difference": "SD",
    "Demand": "DE",
    "Closing Stock": "CS",
}


gas_flow_dict = {
    'Production': 'PR',
    'From Other Sources': 'OS',
    'Total Imports': 'TI',
    'LNG Imports': 'LI',
    'Pipeline Imports': 'PI',
    'Total Exports': 'TE',
    'LNG Exports': 'LE',
    'Pipeline Exports': 'PE',
    'Stock Change': 'SE',
    'Gross Inland Deliveries (Calculated)': 'DC',
    'Gross Inland Deliveries (Observed)': 'DO',
    'Electricity and Heat Generation': 'EH',
    'Closing Stock': 'CS'
    }

oil_units_dict = {
    "Thousand Barrels per day (kb/d)": "KD",
    "Thousand Barrels (kbbl)": "KB",
    "Thousand Kilolitres (kl)": "KL",
    "Thousand Metric Tons (kmt)": "KT",
    "Conversion factor barrels/ktons": "BK",
    }

gas_units_dict = {
    "Million Cubic Meters": "GC",
    "Terajoules": "GT",
    "1000 Metric Tons (LNG)": "GL",
    }


###########################################FUNCTIONS#############################################


def get_key(key_id):
    load_dotenv
    return os.getenv(key_id)



def get_code(energy, flow, unit, product=None):
    if energy in [energy_list[0], energy_list[1]]:  
        product_code = primary_oil_products_dict.get(product) or secondary_oil_products_dict.get(product)
        flow_code = primary_oil_flow_dict.get(flow) or secondary_oil_flow_dict.get(flow)
        unit_code = oil_units_dict.get(unit)
        return f'{product_code}{flow_code}{unit_code}'

    elif energy == energy_list[2]:  
        flow_code = gas_flow_dict.get(flow)
        unit_code = gas_units_dict.get(unit)
        return f'{unit_code}{flow_code}'
    


def get_nasdaq_table(
        code_id: str|list, 
        country_id: str, 
        date_from_id: str, 
        date_to_id: str
        ):
    
    nasdaqdatalink.ApiConfig.api_key = get_key('nasdaq_api_key')
    df = nasdaqdatalink.get_table('QDL/JODI',
                                  qopts = {"columns":['code','country','date','value']},
                                  code = code_id,
                                  country = country_id,
                                  date = {'gte': date_from_id , 'lte': date_to_id })
    
    df['value'] = df['value'].replace(['x', None], '0')
    df['value'] = df['value'].astype(float)
    
    return df



def make_line_chart(energy, country, unit, date_from, date_to, product):

    fig = go.Figure(layout=des.layout_simple)
    df_graph = get_nasdaq_table(energy, country, date_from, date_to)


    #if energy == (energy_list[0] or energy_list[1]) and not unit:
    #    fig.update_layout(title='Please select unit to view data.')

    if energy in [energy_list[0], energy_list[1]] and not product:
        fig.update_layout(title='Please select a product to view all flows.')
    

    code_list = []

    if energy == energy_list[0] and unit and product:
        for i in primary_oil_flow_dict.keys():
            code = get_code(energy, i, unit, product)
            code_list.append(code)
    
        df_graph = get_nasdaq_table(code_id=code_list, 
                                    country_id=country, 
                                    date_from_id=date_from, 
                                    date_to_id=date_to
                                    )
        
        for i,code in zip(primary_oil_flow_dict.keys(), code_list):
            fig.add_trace(
                go.Scatter(
                    x=df_graph.loc[df_graph['code'] == code, 'date'],
                    y=df_graph.loc[df_graph['code'] == code, 'value'],
                    mode='lines',
                    name=i)
                    )
    
    
    if energy == energy_list[1] and unit and product:
        for i in secondary_oil_flow_dict.keys():
            code = get_code(energy, i, unit, product)
            code_list.append(code)

        df_graph = get_nasdaq_table(code_id=code_list, 
                                    country_id=country, 
                                    date_from_id=date_from, 
                                    date_to_id=date_to
                                    )
        
        for i,code in zip(secondary_oil_flow_dict.keys(), code_list):
            fig.add_trace(
                go.Scatter(
                    x=df_graph.loc[df_graph['code'] == code, 'date'],
                    y=df_graph.loc[df_graph['code'] == code, 'value'],
                    mode='lines',
                    name=i)
                    )

    if energy == energy_list[2] and unit:
        for i in gas_flow_dict.keys():
            code = get_code(energy, i, unit)
            code_list.append(code)
        
        df_graph = get_nasdaq_table(code_id=code_list, 
                                    country_id=country, 
                                    date_from_id=date_from, 
                                    date_to_id=date_to
                                    )
        
        for i,code in zip(gas_flow_dict.keys(), code_list):
            fig.add_trace(
                go.Scatter(
                    x=df_graph.loc[df_graph['code'] == code, 'date'],
                    y=df_graph.loc[df_graph['code'] == code, 'value'],
                    mode='lines',
                    name=i)
                    )
                    
    fig.update_layout(transition_duration=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), xaxis_title='Time', yaxis_title=unit)
    return fig



def make_bar_chart(energy, country, unit, date_from, date_to, flow, product):

    fig = go.Figure()

    if energy in [energy_list[0], energy_list[1]] and not flow and not unit:
        fig.update_layout(title='Please select a flow/unit to view data.')
        return fig
    

    if energy in [energy_list[0], energy_list[1]] and product:
        code = get_code(energy, flow, unit, product)
        df_graph = get_nasdaq_table(
                                    code_id=code, 
                                    country_id=country, 
                                    date_from_id=date_from, 
                                    date_to_id=date_to
                                    )
        fig.add_trace(
            go.Bar(
                x=df_graph.loc[df_graph['code'] == code, 'date'],
                y=df_graph.loc[df_graph['code'] == code, 'value'],
            ))


    if energy == energy_list[2] and unit:
        code = get_code(energy, flow, unit)
        df_graph = get_nasdaq_table(
                                    code_id=code, 
                                    country_id=country, 
                                    date_from_id=date_from, 
                                    date_to_id=date_to
                                    )
        fig.add_trace(
            go.Bar(
                x=df_graph.loc[df_graph['code'] == code, 'date'],
                y=df_graph.loc[df_graph['code'] == code, 'value'],
            ))


    fig.update_layout(transition_duration=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), xaxis_title='Time', yaxis_title=unit)

    return fig





def make_pie_chart(energy, country, unit, date_from, date_to, flow):

    fig = go.Figure()

    if energy in [energy_list[0], energy_list[1]] and not flow and not unit:
        fig.update_layout(title='Please select a flow/unit to view data.')
        return fig
    
    labels_list = []
    values_list = []
    code_list = []

    if energy == energy_list[0] and flow:
        for i,j in primary_oil_products_dict.items():
            if j == 'TC':
                continue

            code = get_code(energy, flow, unit, i)
            code_list.append(code)
        
        df_graph = get_nasdaq_table(code_id=code_list, 
                                    country_id=country, 
                                    date_from_id=date_from, 
                                    date_to_id=date_to
                                    )


        for i,code in zip(primary_oil_products_dict.keys(),code_list):
            values = df_graph[df_graph['code'] == code]['value'].sum()
            if values != 0:
                labels_list.append(i)
                values_list.append(values)
                    
        fig.add_trace(go.Pie(labels=labels_list,values=values_list))
        fig.update_traces(textinfo='percent+label')


    if energy == energy_list[1] and flow:
        for i,j in secondary_oil_products_dict.items():
            if j == 'TP':
                continue

            code = get_code(energy, flow, unit, i)
            code_list.append(code)
        
        df_graph = get_nasdaq_table(code_id=code_list, 
                                    country_id=country, 
                                    date_from_id=date_from, 
                                    date_to_id=date_to
                                    )
        
        for i,code in zip(secondary_oil_products_dict.keys(),code_list):
            values = df_graph[df_graph['code'] == code]['value'].sum()
            if values != 0:
                labels_list.append(i)
                values_list.append(values)
                    
        fig.add_trace(go.Pie(labels=labels_list,values=values_list))
        fig.update_traces(textinfo='percent+label')


    if energy == energy_list[2] and unit:
        if flow == 'Imports':
            for i in ['Pipeline Imports', 'LNG Imports']:
            
                code = get_code(energy, i, unit)
                code_list.append(code)
            df_graph = get_nasdaq_table(code_id=code_list, 
                                            country_id=country, 
                                            date_from_id=date_from, 
                                            date_to_id=date_to
                                            )
            
            for i,code in zip(['Pipeline Imports', 'LNG Imports'], code_list):
                values = df_graph[df_graph['code'] == code]['value'].sum()
                if values != 0:
                    labels_list.append(i)
                    values_list.append(values)
                    
            fig.add_trace(go.Pie(labels=labels_list,values=values_list))

        elif flow == 'Exports':
            for i in ['Pipeline Exports', 'LNG Exports']:
            
                code = get_code(energy, i, unit)
                code_list.append(code)
            
            df_graph = get_nasdaq_table(code_id=code_list, 
                                        country_id=country, 
                                        date_from_id=date_from, 
                                        date_to_id=date_to
                                        )
            
            for i,code in zip(['Pipeline Exports', 'LNG Exports'], code_list):
                values = df_graph[df_graph['code'] == code]['value'].sum()
                if values != 0:
                    labels_list.append(i)
                    values_list.append(values)
                    
            fig.add_trace(go.Pie(labels=labels_list,values=values_list))


    fig.update_layout(transition_duration=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), xaxis_title='Time', yaxis_title=unit)

    return fig