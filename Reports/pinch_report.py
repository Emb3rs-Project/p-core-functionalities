import os
import json
from module.utilities.kb import KB
from module.utilities.kb_data import kb
from module.Source.simulation.Heat_Recovery.Pinch.convert_pinch import convert_pinch
from module.Source.simulation.Heat_Recovery.Pinch.make_pinch_design_draw import make_pinch_design_draw
import pandas as pd

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
        'name': "Energy Savings",
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
        'name': "Energy Savings Specific Cost",
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

    return html

def get_round(df, decimal=2):
    return df.round(decimals=decimal)

def get_int(df):
    return df.astype(int)


def pinch_report(test):

    for key in test:
        category_solutions_data = test[str(key)]

        # GET Overview Category Solutions
        if test[str(key)]['best_options'] == []:
            best_options_data[str(key)] = []
        else:
            df_best_design = pd.DataFrame(test[str(key)]['best_options']).drop(columns=['energy_investment'])
            df_best_design.columns = ['Solution ID', 'CO2 Savings [kgCO2/year]', 'Money Savings [€/year]','Energy Recovered [kWh/year]', 'CAPEX  [€]', 'OM Fix [€/year]']
            best_options_data[str(key)] = styling(df_best_design)

        # GET Each Designed Solutions
        for solution in category_solutions_data["solutions"]:

            # stream table
            df_streams = solution['stream_table'].copy()
            df_streams.insert(0, 'Stream ID', df_streams.index.copy())
            df_streams.columns = ['Stream ID', 'Fluid', "Supply Temperature [ºC]", "Target Temperature [ºC]", "Capacity [kW]", "Stream Type", "mcp [kJ/K]"]
            df_streams["Capacity [kW]"] = get_int(df_streams["Capacity [kW]"])
            df_streams = styling(df_streams)

            # stream combination not feasible
            stream_combination_not_feasible_data = solution['stream_combination_not_feasible']

            df = pd.DataFrame(solution['pinch_hx_data']).copy()
            df.insert(0, 'HX ID', df['id'])

            # df HX overview
            df_overview = df[['HX ID', 'Total_Turnkey_Cost', 'Recovered_Energy']]
            df_overview.columns = ['HX ID', 'Total Turnkey [€]', 'Recovered Energy [kWh/year]']
            solutions_data[key]['df_overview'].append(styling(df_overview))

            # df HX Technical
            df_hx = df[['HX ID', "HX_Power", "HX_Original_Cold_Stream", "HX_Cold_Stream_mcp", "HX_Cold_Stream_T_Cold",
                        "HX_Cold_Stream_T_Hot", "HX_Original_Hot_Stream", "HX_Hot_Stream_mcp", "HX_Hot_Stream_T_Hot",
                        "HX_Hot_Stream_T_Cold"]]

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
            df_hx_economic.columns = ["HX ID",'Type', 'CAPEX [€]', 'OM Fix [€/year]']
            solutions_data[key]['df_hx_economic'].append(styling(df_hx_economic))

            # HX storage
            df_storage = df[["HX ID",'Storage', 'Storage_Satisfies', 'Storage_Turnkey_Cost']]
            df_storage.columns = ["HX ID",'Storage Volume [m3]', 'Storage Match [%]', 'CAPEX [€]']
            solutions_data[key]['df_storage'].append(styling(df_storage))

            # HX Network
            solutions_data[key]['hx_network'].append(make_pinch_design_draw(solution['_info_pinch']))

            # DF streams each solution
            df_streams_each_solution = solution['stream_table'].loc[solution['streams']]
            df_streams_each_solution.insert(0, 'Stream ID', df_streams_each_solution.index.copy())
            solutions_data[key]['df_streams_each_solution'].append(styling(df_streams_each_solution))

    # Stream combination not feasible
    if stream_combination_not_feasible_data == []:
        stream_combination_not_feasible_data = 'NOTE: All streams combinations were analyzed.'
    else:
        stream_combination_not_feasible_data = 'NOTE: The following combination of streams simulation was infeasible:' + str(stream_combination_not_feasible_data)

    ### REPORT_RENDERING_codes [BEGIN]
    from jinja2 import Environment, FileSystemLoader

    env = Environment(
        loader=FileSystemLoader('asset'),
        autoescape=False
    )

    template = env.get_template('index.pinch_template.html')
    template_content = template.render(designed_solutions=solutions_data,
                                       stream_table=df_streams,
                                       stream_combination_not_feasible=stream_combination_not_feasible_data,
                                       best_options=best_options_data)

    f = open("./asset/output.html", "w")
    f.write(template_content)
    f.close()

    output = {
        "every" : "thing",
        "else" : "yes",
        "report" : template_content
    }
    return output


script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir,
                                        "../Tests/Sources/simulation/test_files/pinch_isolated_streams_test_2.json")))
test = convert_pinch(data_test, KB(kb))

a = pinch_report(test)