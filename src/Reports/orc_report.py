from jinja2 import Environment, FileSystemLoader
import os
from datetime import date

def styling(df):
    html = df.to_html(index=False,
                      classes=['table', 'bg-white', 'table-striped', "text-center"]
                      ).replace("<th>", "<th class='align-middle text-center'>")



    html = html.replace("CO2","CO<sub>2</sub>")
    html = html.replace("T evaporator","T<sub>evaporator</sub>")
    html = html.replace("T condenser","T<sub>condenser</sub>")

    return html


def get_round(df, decimal=2):
    return df.round(decimals=decimal)


def get_int(df):
    return df.astype(int)


def convert_to_megawatt(df):
    return df/1000

def get_html(stream_table_data, df_overview_data, df_technical_data, df_economic_data, elec_cost_data, co2_emission_data):

    ### REPORT_RENDERING_codes [BEGIN]
    script_dir = os.path.dirname(__file__)

    env = Environment(
        loader=FileSystemLoader(os.path.join(script_dir, "asset")),
        autoescape=False
    )

    template = env.get_template('index.orc_template.html')
    report_html = template.render(stream_table=stream_table_data,
                                  df_overview=df_overview_data,
                                  df_technical=df_technical_data,
                                  df_economic=df_economic_data,
                                  elec_cost=elec_cost_data,
                                  co2_emission=co2_emission_data)

    return report_html


def orc_report(convert_orc_output):
    """ Build ORC report HTML

    Parameters
    ----------
    convert_orc_output: dict
        Output from ORC routine

    Returns
    -------
    report_html : str
        HTML report

    """

    today = date.today()

    #############################
    # Get data
    df_solutions = convert_orc_output['best_options']
    elec_cost_data = convert_orc_output["elec_cost_data"]
    co2_emission_data = convert_orc_output["co2_emission_data"]
    stream_table_data = convert_orc_output['df_streams'][
        ["id","name", "supply_temperature", "target_temperature", "fluid", "capacity"]].copy()

    #############################
    # Stream table
    stream_table_data["capacity"] = get_int(stream_table_data["capacity"])
    stream_table_data["fluid"] = stream_table_data["fluid"].apply(lambda x: x.replace("_", " "))

    stream_table_data.columns = ["Stream ID",
                                 "Name",
                                 "Supply Temperature [ºC]",
                                 "Target Temperature[ºC]",
                                 "Fluid",
                                 "Capacity [kW]"]

    # Designed Solutions
    df_solutions["electrical_generation_yearly"] = get_int(df_solutions["electrical_generation_yearly"])
    df_solutions["capex"] = get_int(df_solutions["capex"])
    df_solutions["om_fix"] = get_int(df_solutions["om_fix"])
    df_solutions["ID"] = get_int(df_solutions["ID"])
    df_solutions["electrical_generation_nominal"] = get_int(df_solutions["electrical_generation_nominal"])

    df_solutions['conversion_efficiency'] = get_round(df_solutions['conversion_efficiency'], 3)

    df_solutions["CO2 Savings"] = df_solutions["co2_savings"] * df_solutions["electrical_generation_yearly"]
    df_solutions["CO2 Savings"] = get_int(df_solutions["CO2 Savings"])

    df_solutions["Money Savings"] = df_solutions["money_savings"] * df_solutions["electrical_generation_yearly"]
    df_solutions['Money Savings'] = df_solutions['Money Savings'].astype(int)
    df_solutions["Money Savings"] = get_int(df_solutions["Money Savings"])

    # Overview Data
    df_overview_data = df_solutions[
        ["ID", "streams_id", "CO2 Savings", "Money Savings", "electrical_generation_yearly", "capex",
         "om_fix"]].copy()



    df_overview_data.columns = ["Solution ID",
                                "Streams ID",
                                "CO2 Savings [kgCO2/year]",
                                "Monetary Savings [€/year]",
                                "Yearly Electrical Generation [kWh]",
                                "CAPEX [€]",
                                "OM Fix [€/year]"]


    df_overview_data['Yearly Electrical Generation [kWh]'] = convert_to_megawatt(df_overview_data['Yearly Electrical Generation [kWh]'])
    df_overview_data.rename(columns={'Yearly Electrical Generation [kWh]': 'Yearly Electrical Generation [MWh]'}, inplace=True)
    df_overview_data['Yearly Electrical Generation [MWh]'] = get_int(df_overview_data['Yearly Electrical Generation [MWh]'])

    # Technical Data
    df_technical_data = df_solutions[
        ["ID", "electrical_generation_nominal", "conversion_efficiency", "orc_T_evap", "orc_T_cond"]].copy()

    df_technical_data['conversion_efficiency'] = df_technical_data['conversion_efficiency'] * 100

    df_technical_data.columns = ["Solution ID",
                                 "ORC Power [kW]",
                                 "ORC eff [%]",
                                 "T evaporator [ºC]",
                                 "T condenser [ºC]"]

    # Economic Data
    df_economic_data = df_solutions[["ID", "capex", "om_fix", "om_var"]].copy()

    df_economic_data['om_var'] = df_economic_data['om_var'] * df_solutions["electrical_generation_yearly"]
    df_economic_data['om_var'] = get_int(df_economic_data['om_var'])

    df_economic_data.columns = ["Solution ID",
                                "Turnkey [€]",
                                "OM Fix [€/year]",
                                "OM Variable [€/year]"]

    # Styling
    stream_table_data = styling(stream_table_data)
    df_overview_data = styling(df_overview_data)
    df_technical_data = styling(df_technical_data)
    df_economic_data = styling(df_economic_data)

    ### REPORT_RENDERING_codes [BEGIN]
    script_dir = os.path.dirname(__file__)

    env = Environment(
        loader=FileSystemLoader(os.path.join(script_dir, "asset")),
        autoescape=False
    )

    template = env.get_template('index.orc_template.html')
    report_html = template.render(
                                date=today, stream_table=stream_table_data,
                                df_overview=df_overview_data,
                                df_technical=df_technical_data,
                                df_economic=df_economic_data,
                                elec_cost=elec_cost_data,
                                co2_emission=co2_emission_data)

    return report_html
