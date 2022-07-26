import os
from ..Source.simulation.Heat_Recovery.Pinch.make_pinch_design_draw import make_pinch_design_draw
import pandas as pd
from datetime import date

### GETTING DATA ###
solutions_data = {
    'co2_optimization':
        {
            'df_streams_each_solution': [],
            'name': "CO<sub>2</sub> Savings",
            'hx_network': [],
            'body_color': '#EAFAF1',
            'header_color': '#A9DFBF',
            'df_overview': [],
            'df_hx': [],
            'df_hx_economic': [],
            'df_storage': []

        },
    'energy_recovered_optimization': {
        'df_streams_each_solution': [],
        'name': "Heat Recovery",
        'hx_network': [],
        'body_color': '#FDF9E9',
        'header_color': '#F7DC6F'
        ,
        'df_overview': [],
        'df_hx': [],
        'df_hx_economic': [],
        'df_storage': []
    },
    'energy_investment_optimization': {
        'df_streams_each_solution': [],
        'name': "Heat Recovery Specific Cost",
        'hx_network': [],
        'body_color': '#EAF2F8',
        'header_color': '#AED6F1 ',
        'df_overview': [],
        'df_hx': [],
        'df_hx_economic': [],
        'df_storage': []
    },
}

best_options_data = {}

def styling(df):
    html = df.to_html(index=False,
                      classes=['table', 'bg-white', 'table-striped', "text-center"]
                      ).replace("<th>", "<th class='align-middle text-center'>")

    html = html.replace("CO2","CO<sub>2</sub>")
    html = html.replace("mcp","mc<sub>p</sub>")
    html = html.replace("Tin","T<sub>in</sub>")
    html = html.replace("Tout","T<sub>out</sub>")


    return html

def get_round(df, decimal=2):
    return df.round(decimals=decimal)

def get_int(df):
    return df.astype(int)

def put_line_if_zero(df):
    df = df.map(str)
    return df.apply(lambda x: x.replace('0', "-") if len(x) == 1 else x)

def convert_to_megawatt(df):
    return df/1000

def pinch_report(data_pinch):

    """Build Pinch Analysis report HTML

    Parameters
    ----------
    data_pinch: dict
        Output from Pinch routine

    Returns
    -------
    report_html : str
        HTML report

    """

    today = date.today()

    # dd/mm/YY
    date_today = today.strftime("%d/%m/%Y")

    for key in data_pinch:
        category_solutions_data = data_pinch[str(key)]

        # GET Overview Category Solutions
        if data_pinch[str(key)]['best_options'] == []:
            best_options_data[str(key)] = []
        else:
            df_best_design = pd.DataFrame(data_pinch[str(key)]['best_options']).drop(columns=['energy_investment'])
            df_best_design.columns = ['Solution ID', 'CO2 Savings [kgCO2/year]', 'Monetary Savings [€/year]','Heat Recovered [kWh/year]', 'CAPEX  [€]', 'OM Fix [€/year]']
            df_best_design['Heat Recovered [kWh/year]'] = convert_to_megawatt(df_best_design['Heat Recovered [kWh/year]'])
            df_best_design = get_int(df_best_design)
            df_best_design.rename(columns={'Heat Recovered [kWh/year]': 'Heat Recovered [MWh/year]'}, inplace=True)
            df_best_design['CO2 Savings [kgCO2/year]'] = put_line_if_zero(df_best_design['CO2 Savings [kgCO2/year]'])
            df_best_design['Monetary Savings [€/year]'] = put_line_if_zero(df_best_design['Monetary Savings [€/year]'])

            best_options_data[str(key)] = styling(df_best_design)

        # GET Each Designed Solutions
        for solution in category_solutions_data["solutions"]:

            # stream table
            solution['stream_table'] = solution['stream_table'][['Name','Fluid', 'Supply Temperature', 'Target Temperature', 'Capacity', 'Stream Type', 'mcp']]
            solution['stream_table'].columns = ['Name','Fluid', "Supply Temperature [ºC]", "Target Temperature [ºC]", "Capacity [kW]", "Stream Type", "mcp [kJ/K]"]


            all_streams_table = solution['stream_table'][['Name','Fluid', "Supply Temperature [ºC]", "Target Temperature [ºC]", "Capacity [kW]", "mcp [kJ/K]", "Stream Type"]]
            all_streams_table["Capacity [kW]"] = get_int(all_streams_table["Capacity [kW]"])
            all_streams_table["Supply Temperature [ºC]"] = get_round(all_streams_table["Supply Temperature [ºC]"], decimal=1)
            all_streams_table["mcp [kJ/K]"] = get_round(all_streams_table["mcp [kJ/K]"], decimal=1)

            df_streams = all_streams_table.copy()
            df_streams.insert(0, 'Stream ID', df_streams.index.copy())
            df_streams = styling(df_streams)

            # stream combination not feasible
            stream_combination_not_feasible_data = solution['stream_combination_not_feasible']

            df = pd.DataFrame(solution['pinch_hx_data']).copy()
            df.insert(0, 'HX ID', df['id'])

            # df HX overview
            df_overview = df[['HX ID', 'Total_Turnkey_Cost', 'Recovered_Energy']]
            df_overview.columns = ['HX ID', 'Total Turnkey [€]', 'Recovered Heat [kWh/year]']
            solutions_data[key]['df_overview'].append(styling(df_overview))

            # df HX Technical
            df_hx = df[['HX ID', "HX_Power", "HX_Original_Cold_Stream", "HX_Cold_Stream_mcp", "HX_Cold_Stream_T_Cold",
                        "HX_Cold_Stream_T_Hot", "HX_Original_Hot_Stream", "HX_Hot_Stream_mcp", "HX_Hot_Stream_T_Hot",
                        "HX_Hot_Stream_T_Cold"]].copy()


            df_hx["HX_Cold_Stream_mcp"] = get_round(df_hx["HX_Cold_Stream_mcp"], decimal=2)
            df_hx["HX_Hot_Stream_mcp"] = get_round(df_hx["HX_Hot_Stream_mcp"], decimal=2)
            df_hx["HX_Power"] = get_int(df_hx["HX_Power"])
            df_hx["HX_Cold_Stream_T_Cold"] = get_round(df_hx["HX_Cold_Stream_T_Cold"], decimal=1)
            df_hx["HX_Cold_Stream_T_Hot"] = get_round(df_hx["HX_Cold_Stream_T_Hot"], decimal=1)
            df_hx["HX_Hot_Stream_T_Hot"] = get_round(df_hx["HX_Hot_Stream_T_Hot"], decimal=1)
            df_hx["HX_Hot_Stream_T_Cold"] = get_round(df_hx["HX_Hot_Stream_T_Cold"], decimal=1)

            columns = [("HX Info", "HX ID"),
                        ("HX Info", "HX Power"),
                        ("Cold Stream", "HX_Original_Cold_Stream"),
                        ("Cold Stream", "HX_Cold_Stream_mcp"),
                        ("Cold Stream", "HX_Cold_Stream_T_Cold"),
                        ("Cold Stream", "HX_Cold_Stream_T_Hot"),
                        ("Hot Stream", "HX_Original_Hot_Stream"),
                        ("Hot Stream", "HX_Hot_Stream_mcp"),
                        ("Hot Stream", "HX_Hot_Stream_T_Hot"),
                        ("Hot Stream", "HX_Hot_Stream_T_Cold"),
                        ]

            df_hx.columns = pd.MultiIndex.from_tuples(columns)
            new_columns = [("HX Info", "HX ID"),
                             ("HX Info", "HX Power [kW]"),
                             ("Cold Stream", "ID"),
                             ("Cold Stream", "mcp [kJ/K]"),
                             ("Cold Stream", "Tin [ºC]"),
                             ("Cold Stream", "Tout [ºC]"),
                             ("Hot Stream", "ID"),
                             ("Hot Stream", "mcp [kJ/K]"),
                             ("Hot Stream", "Tin [ºC]"),
                             ("Hot Stream", "Tout [ºC]"),
                             ]

            df_hx.columns = pd.MultiIndex.from_tuples(new_columns)

            solutions_data[key]['df_hx'].append(styling(df_hx))

            # HX economic
            df_hx_economic = df[["HX ID",'HX_Type', 'HX_Turnkey_Cost', 'HX_OM_Fix_Cost']].copy()
            df_hx_economic['HX_Type'] = df_hx_economic['HX_Type'].apply(lambda x: x.replace("_", " "))
            df_hx_economic['HX_Turnkey_Cost'] = get_int(df_hx_economic['HX_Turnkey_Cost'])
            df_hx_economic['HX_OM_Fix_Cost'] = get_int(df_hx_economic['HX_OM_Fix_Cost'])
            df_hx_economic.columns = ["HX ID",'Type', 'CAPEX [€]', 'OM Fix [€/year]']
            solutions_data[key]['df_hx_economic'].append(styling(df_hx_economic))

            # HX storage
            df_storage = df[["HX ID",'Storage', 'Storage_Satisfies', 'Storage_Turnkey_Cost']].copy()
            df_storage["Storage_Satisfies"] = get_round(df_storage["Storage_Satisfies"], decimal=2)
            df_storage["Storage_Turnkey_Cost"] = get_int(df_storage["Storage_Turnkey_Cost"])
            df_storage["Storage"] = get_round(df_storage["Storage"], decimal=2)

            df_storage.columns = ["HX ID",'Storage Volume [m3]', 'Storage Match [%]', 'CAPEX [€]']

            if (df_storage['Storage Volume [m3]'] == 0).sum() == df_storage.shape[0]:
                solutions_data[key]['df_storage'].append("no_solution")
            else:
                df_storage = df_storage[df_storage['Storage Volume [m3]'] > 0]
                solutions_data[key]['df_storage'].append(styling(df_storage))

            # HX Network
            solutions_data[key]['hx_network'].append(make_pinch_design_draw(solution['_info_pinch']))

            # DF streams each solution
            df_streams_each_solution = all_streams_table.loc[solution['streams']]
            df_streams_each_solution.insert(0, 'Stream ID', df_streams_each_solution.index.copy())
            solutions_data[key]['df_streams_each_solution'].append(styling(df_streams_each_solution))

    # Stream combination not feasible
    if stream_combination_not_feasible_data == []:
        stream_combination_not_feasible_data = 'NOTE: All streams combinations were analyzed.'
    else:
        stream_combination_not_feasible_data = 'NOTE: The following combination of streams simulation was infeasible:' + str(stream_combination_not_feasible_data)

    ### REPORT_RENDERING_codes [BEGIN]
    from jinja2 import Environment, FileSystemLoader


    script_dir = os.path.dirname(__file__)

    env = Environment(
        loader=FileSystemLoader(os.path.join(script_dir, "asset")),
        autoescape=False
    )

    template = env.get_template('index.pinch_template.html')
    report_html = template.render(date=date_today,
                                  designed_solutions=solutions_data,
                                  stream_table=df_streams,
                                  stream_combination_not_feasible=stream_combination_not_feasible_data,
                                  best_options=best_options_data)

    return report_html

