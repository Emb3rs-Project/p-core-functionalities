def styling(df):
    html = df.to_html(index=False,
                      classes=['table', 'bg-white', 'table-striped', "text-center"]
                      ).replace("<th>", "<th class='align-middle text-center'>")

    return html


def get_round(df, decimal=2):
    return df.round(decimals=decimal)


def get_int(df):
    return df.astype(int)


def orc_report(convert_orc_output):
    # Get data
    elec_cost_data = convert_orc_output["elec_cost_data"]
    co2_emission_data = convert_orc_output["co2_emission_data"]
    stream_table_data = convert_orc_output['df_streams'][
        ["id", "supply_temperature", "target_temperature", "fluid", "capacity"]].copy()
    df_solutions = convert_orc_output['best_options']

    # Stream table
    stream_table_data["capacity"] = get_int(stream_table_data["capacity"])
    stream_table_data.columns = ["Stream ID", "Supply Temperature [ºC]", "Target Temperature[ºC]", "Fluid", "Capacity [kW]"]
    stream_table_data["Fluid"] = stream_table_data["Fluid"].apply(lambda x: x.replace("_", " "))

    # Designed Solutions
    df_solutions["electrical_generation_yearly"] = get_int(df_solutions["electrical_generation_yearly"])
    df_solutions["turnkey"] = get_int(df_solutions["turnkey"])
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
        ["ID", "streams_id", "CO2 Savings", "Money Savings", "electrical_generation_yearly", "turnkey",
         "om_fix"]].copy()
    df_overview_data.columns = ["Solution ID", "Streams ID", "CO2 Savings [kgCO2/year]", "Money Savings [€/year]",
                                "Yearly Electrical Generation [kWh]", "CAPEX [€]", "OM Fix [€/year]"]

    # Technical Data
    df_technical_data = df_solutions[
        ["ID", "electrical_generation_nominal", "conversion_efficiency", "orc_T_evap", "orc_T_cond"]].copy()
    df_technical_data['conversion_efficiency'] = df_technical_data['conversion_efficiency'] * 100

    df_technical_data.columns = ["Solution ID", "ORC Power [kW]", "ORC eff [%]", "T evaporator [ºC]",
                                 "T condenser [ºC]"]

    # Economic Data
    df_economic_data = df_solutions[["ID", "turnkey", "om_fix", "om_var"]].copy()

    df_economic_data['om_var'] = df_economic_data['om_var'] * df_solutions["electrical_generation_yearly"]
    df_economic_data['om_var'] = get_int(df_economic_data['om_var'])

    df_economic_data.columns = ["Solution ID", "Turnkey [€]", "OM Fix [€/year]", "OM Variable [€/year]"]

    # Styling
    stream_table_data = styling(stream_table_data)
    df_overview_data = styling(df_overview_data)
    df_technical_data = styling(df_technical_data)
    df_economic_data = styling(df_economic_data)

    ### REPORT_RENDERING_codes [BEGIN]
    from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
    import os

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
