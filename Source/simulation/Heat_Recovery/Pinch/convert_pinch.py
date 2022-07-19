"""
alisboa/jmcunha
"""

from .....Source.simulation.Heat_Recovery.Pinch.Auxiliary.pinch_analysis import pinch_analysis
from .....Source.simulation.Heat_Recovery.Pinch.Auxiliary.get_best_x_outputs import get_best_x_outputs
from .....KB_General.fuel_properties import FuelProperties
from .....General.Auxiliary_General.get_country import get_country
import itertools
import pandas as pd
from .....utilities.kb import KB
from .....Error_Handling.runtime_error import ModuleRuntimeException
from .....Error_Handling.error_pinch import error_convert_pinch
from .....Reports.pinch_report import pinch_report


def convert_pinch(in_var, kb: KB):
    """
    Main function of Heat Recovery Module.
    Includes data pretreatment, pinch analysis, and economic/co2 analysis of the options designed.
    Return the best three solutions for: minimum CO2 emissions ,maximize energy recovery, and energy recovery specific cost.

    :param in_var:

        streams_to_analyse: list
            List with streams ID to analyse

        pinch_delta_T_min: float
            Minimum delta temperature for pinch analysis
            Use ºC

        all_input_objects: list
            List with:
                - equipments (check Source/characterization/Generate_Equipment)
                - processes (check Source/characterization/Process/process)
                - isolated streams
                       id,
                       fluid - fluid name
                       flowrate  [kg/h]
                       supply_temperature  [ºC]
                       target_temperature  [ºC]
                       object_id - associated process/equipment ID
                       schedule - array with hourly schedule, 1=operating and 0_not_operating
                       hourly_generation - array with hourly power [kWh]

        location: list
            [latitude, longitude]

        lifetime: int [OPTIONAL]
            Heat exchangers lifetime

        number_output_options: int [OPTIONAL]
            Number of solutions of each category to return
            Assumed number_output_options=3


    :param kb: Knowledge Base

    :return:
        report: str
            HTML report

        best_options: dict
            Categories with list of dicts of the best solutions:
                co2_optimization
                energy_recovered_optimization
                energy_investment_optimization

            Each one provides the best design options in dicts, with the following keys:
            For example in :
                co2_option_1 = {
                                'ID' - designed solution ID  [ID]
                                'streams' - streams in pinch design ID [ID]
                                'streams_info' - array with dicts
                                'capex'  [€]
                                'om_fix' - yearly om fix costs [€/year]
                                'hot_utility' - power of the hot utility needed, so that the cold streams reach their target_temperature  [kW]
                                'cold_utility' - power of the cold utility needed, so that the hot streams reach their target_temperature  [kW]
                                'lifetime' - considered lifetime  [year]
                                'co2_savings' - annualized co2 savings by implementing the pinch design [kg CO2/kWh]
                                'money_savings' - annualized energy savings by implementing the pinch design  [€/kWh]
                                'energy_dispatch' - yearly energy recovered by implementing the pinch design [kWh/year]
                                'discount_rate'  []
                                'pinch_temperature' - design pinch temperature [ºC]
                                'theo_minimum_hot_utility' - theoretical power of the hot utility needed, so that the cold streams reach their target_temperature  [kW]
                                'theo_minimum_cold_utility' - theoretical power of the cold utility needed, so that the hot streams reach their target_temperature  [kW]
                                'pinch_hx_data' - list with pinch design data
                                }

                Where in pinch_hx_data various dict with HX designed, e.g. pinch_hx_data=[hx_1,hx_2,...] :
                For example:
                    hx_1 = {
                            'HX_Power'  [kW]
                            'HX_Hot_Stream'  [ID]
                            'HX_Cold_Stream'  [ID]
                            'HX_Original_Hot_Stream'  [ID]
                            'HX_Original_Cold_Stream'  [ID]
                            'HX_Type'  [hx type]
                            'HX_Turnkey_Cost'  [€]
                            'HX_OM_Fix_Cost'  [€/year]
                            'HX_Hot_Stream_T_Hot'  [ºC]
                            'HX_Hot_Stream_T_Cold'  [ºC]
                            'HX_Cold_Stream_T_Hot'  [ºC]
                            'HX_Cold_Stream_T_Cold'  [ºC]
                            'Storage'  [m3]
                            'Storage_Satisfies'  [%]
                            'Storage_Turnkey_Cost'  [€]
                            'Total_Turnkey_Cost'  [€]
                            'Recovered_Energy'  [kWh/year]
                             }
    """

    ############################################################################################################
    # INPUT
    platform_data = error_convert_pinch(in_var["platform"])

    all_input_objects = platform_data.all_input_objects  # equipments/processes/isolated streams
    all_input_objects = [vars(new_object) for new_object in all_input_objects]

    pinch_delta_T_min = platform_data.pinch_delta_T_min
    latitude, longitude = platform_data.location
    perform_all_combinations = platform_data.perform_all_combinations  # parameter to only perform all combinations for isolated streams and processes.
    number_output_options = platform_data.number_output_options
    lifetime = platform_data.lifetime
    streams_to_analyse = platform_data.streams_to_analyse
    fuels_data = platform_data.fuels_data
    interest_rate = platform_data.interest_rate


    ############################################################################################################
    # Defined Vars
    country = get_country(latitude, longitude)
    objects_to_analyze = []
    streams = []
    subset_not_possible_to_analyze = []

    ############################################################################################################
    # DATA PRE-TREATMENT
    hx_delta_T = pinch_delta_T_min
    pinch_delta_T_min = pinch_delta_T_min / 2

    try:
        # create the streams list
        #get_equipment = {str(input_object['id']): input_object for input_object in all_input_objects if
        #                 input_object['object_type'] == 'equipment'}
        for object in all_input_objects:  # objet can be stream/process/equipment
            if object['object_type'] == 'process':  # from processes get streams
                objects_to_analyze.append(object)
                for stream in object['streams']:
                    if stream['id'] in streams_to_analyse:
                        if stream['stream_type'] != "outflow":
                            stream['fuel_price'] = fuels_data[stream['fuel']]["price"]
                            stream['fuel_co2_emissions'] = fuels_data[stream['fuel']]["co2_emissions"]
                        else:
                            stream['fuel'] = None
                            stream['eff_equipment'] = None
                            object['fuel_co2_emissions'] = None
                            object['eff_equipment'] = None

                        streams.append(stream)

            elif object['object_type'] == 'stream':  # isolated streams
                if object['id'] in streams_to_analyse:
                    if object['fuel'] != "none":
                        object['fuel_price'] = fuels_data[object['fuel']]["price"]
                        object['fuel_co2_emissions'] = fuels_data[object['fuel']]['co2_emissions']
                    else:
                        object['fuel'] = None
                        object['fuel_price'] = None
                        object['fuel_co2_emissions'] = None
                        object['eff_equipment'] = None

                    streams.append(object)

            elif object['object_type'] == 'equipment':
                objects_to_analyze.append(object)
                for stream in object['streams']:
                    if stream['id'] in streams_to_analyse:
                        if stream['stream_type'] == "supply_heat":
                            stream['fuel_co2_emissions'] = fuels_data[stream['fuel']]['co2_emissions']
                            stream['fuel_price'] = fuels_data[stream['fuel']]['price']
                        else:
                            stream['fuel'] = None
                            stream['eff_equipment'] = None
                            stream['fuel_price'] = None
                            stream['fuel_co2_emissions'] = None

                        streams.append(stream)


    except:
        raise ModuleRuntimeException(
            code="1",
            type="convert_pinch.py",
            msg="Error obtaining streams to analyze. Check your inputs. \n "
                "If all inputs are correct report to the platform."
        )

    # create DF with streams characteristics (df_char) and  DF with only streams profiles (df_profile)
    list_char = []
    list_profile_data = []
    for stream in streams:
        list_char.append(stream['schedule'])
        list_profile_data.append({
            'ID': stream['id'],
            'Name': stream['name'],
            'Fluid': stream['fluid'],
            'Supply_Temperature': stream['supply_temperature'],
            'Target_Temperature': stream['target_temperature'],
            'Capacity': stream['capacity'],
            'Fuel': stream['fuel'],
            'Eff_Equipment': stream['eff_equipment'],
            'Fuel_Price': stream['fuel_price'],
            'Fuel_CO2_Emissions': stream['fuel_co2_emissions']

        })




    df_profile_data = pd.DataFrame(list_char)
    df_char = pd.DataFrame(list_profile_data)
    df_profile = pd.DataFrame(data=df_profile_data)  # create df
    df_profile.set_index(df_char['ID'], inplace=True)
    df_char.set_index('ID', inplace=True)


    # get all streams info necessary for pinch analysis
    df_char['Stream_Type'] = df_char.apply(
        lambda row: 'Hot' if row['Supply_Temperature'] > row['Target_Temperature']
        else 'Cold', axis=1
    )

    df_char['Supply_Shift'] = df_char.apply(
        lambda row: row['Supply_Temperature'] - pinch_delta_T_min if row['Stream_Type'] == 'Hot'
        else row['Supply_Temperature'] + pinch_delta_T_min, axis=1
    )

    df_char['Target_Shift'] = df_char.apply(
        lambda row: row['Target_Temperature'] - pinch_delta_T_min if row['Stream_Type'] == 'Hot'
        else row['Target_Temperature'] + pinch_delta_T_min, axis=1
    )

    df_char['mcp'] = df_char['Capacity'] /abs(df_char['Supply_Shift']- df_char['Target_Shift'])  # [kW/K]



    ############################################################################################################
    # PINCH ANALYSIS
    design_id = 1  # give each design an ID - initial value
    df_operating = df_char.copy()

    # pinch analysis for all streams
    pinch_designed_solutions, design_id = pinch_analysis(kb,
                                           df_operating,
                                           df_profile,
                                           pinch_delta_T_min,
                                           hx_delta_T,
                                           design_id)



    # pinch analysis for all streams COMBINATIONS
    if perform_all_combinations == True:
        for L in range(0, len(range(df_char.shape[0]))+1):
            for subset in itertools.combinations(range(df_char.shape[0]), L):

                index_see = list(subset)
                index_print = df_char.iloc[index_see].index.values

                if list(subset) != [] and len(list(subset)) > 1:
                    df_operating = (df_char.copy()).iloc[list(subset)]

                    if df_operating[df_operating['Stream_Type'] == 'Hot'].empty == False \
                            and df_operating[df_operating['Stream_Type'] == 'Cold'].empty == False:

                        try:

                            df_hx_hourly, design_id = pinch_analysis(kb,
                                                                     df_operating,
                                                                     df_profile,
                                                                     pinch_delta_T_min,
                                                                     hx_delta_T,
                                                                     design_id)
                            if df_hx_hourly != []:
                                for df in df_hx_hourly:
                                    pinch_designed_solutions.append(df)
                        except:
                            subset_not_possible_to_analyze.append(tuple(index_print))


    ############################################################################################################
    # ECONOMIC/CO2 EMISSIONS ANALYSIS
    list_df_optimization = []

    # Isolated streams
    for index, info in enumerate(pinch_designed_solutions):
        if info['analysis_state'] == 'performed':
            df_hx = info['df_hx']
            total_co2_emissions_savings = 0
            total_money_savings = 0

            for index_df_hx, row_df_hx in df_hx.iterrows():

                original_hot_stream_id = row_df_hx['HX_Original_Hot_Stream']
                original_cold_stream_id = row_df_hx['HX_Original_Cold_Stream']

                hot_stream_fuel = df_char['Fuel'].loc[df_char.index == original_hot_stream_id].values[0]
                cold_stream_fuel = df_char['Fuel'].loc[df_char.index == original_cold_stream_id].values[0]

                # hot stream
                if hot_stream_fuel is not None:

                    data_stream_hot = fuel_properties.get_values(country, hot_stream_fuel, 'non-household')
                    co2_emission_per_kw_stream_hot = data_stream_hot['co2_emissions']
                    fuel_cost_kwh_stream_hot = data_stream_hot['price']
                    eff_equipment = df_char['Eff_Equipment'].loc[df_char.index == original_hot_stream_id].values[0]

                    total_co2_emissions_savings += co2_emission_per_kw_stream_hot * row_df_hx[
                        'Recovered_Energy'] / eff_equipment
                    total_money_savings += fuel_cost_kwh_stream_hot * row_df_hx['Recovered_Energy'] / eff_equipment

                # cold stream
                if cold_stream_fuel is not None:
                    data_stream_cold = fuel_properties.get_values(country, cold_stream_fuel, 'non-household')
                    co2_emission_per_kw_stream_cold = data_stream_cold['co2_emissions']
                    fuel_cost_kwh_stream_cold = data_stream_cold['price']
                    eff_equipment = df_char['Eff_Equipment'].loc[df_char.index == original_cold_stream_id].values[0]

                    total_co2_emissions_savings += co2_emission_per_kw_stream_cold * row_df_hx[
                        'Recovered_Energy'] / eff_equipment
                    total_money_savings += fuel_cost_kwh_stream_cold * row_df_hx['Recovered_Energy'] / eff_equipment

            list_df_optimization.append({
                'index': index,
                'co2_savings': total_co2_emissions_savings,
                'money_savings': total_money_savings,
                'energy_recovered': df_hx['Recovered_Energy'].sum(),
                'energy_investment': df_hx['Total_Turnkey_Cost'].sum() / df_hx['Recovered_Energy'].sum(),
                'turnkey': df_hx['Total_Turnkey_Cost'].sum(),
                'om_fix': df_hx['HX_OM_Fix_Cost'].sum()
            })


    df_optimization = pd.DataFrame(list_df_optimization)

    if df_optimization.empty == True:
        raise Exception('Heat Recovery solutions were not found.')


    df_optimization['index'] = df_optimization['index'] + 1

    # drop duplicates
    df_optimization = df_optimization.drop_duplicates(subset=['co2_savings', 'energy_recovered', 'energy_investment', 'turnkey'])

    # info for HTML
    df_char.drop(['Supply_Shift','Target_Shift'], axis=1,inplace=True)
    df_char.rename(columns=lambda name: name.replace('_', ' '),inplace=True)
    df_char['Fluid'] = df_char['Fluid'].apply(lambda x: x.replace("_", " "))
    stream_table = df_char

    stream_combination_not_feasible = subset_not_possible_to_analyze


    # get best options that recover maximum energy
    energy_recovered = df_optimization.sort_values('energy_recovered', ascending=False).head(number_output_options).copy()
    energy_recovered_options = get_best_x_outputs(pinch_designed_solutions, energy_recovered, country, lifetime, pinch_delta_T_min,
                                                  kb,stream_table,stream_combination_not_feasible, type='Energy Savings', interest_rate=interest_rate)

    # get best options that give best energy_recovery/turnkey ratio
    energy_investment = df_optimization.sort_values('energy_investment').head(number_output_options).copy()
    energy_investment_options = get_best_x_outputs(pinch_designed_solutions, energy_investment, country, lifetime,
                                                   pinch_delta_T_min, kb,stream_table,stream_combination_not_feasible, type='Energy Savings Specific Cost', interest_rate=interest_rate)

    # get best options that save maximum amount of CO2
    co2_savings = df_optimization.sort_values('co2_savings', ascending=False).head(number_output_options).copy()
    co2_savings_options = get_best_x_outputs(pinch_designed_solutions, co2_savings, country, lifetime, pinch_delta_T_min, kb,stream_table,stream_combination_not_feasible,type='CO<sub>2</sub> Emissions Savings', interest_rate=interest_rate)


    # build report
    output_pinch = {
        'co2_optimization': {
            "best_options": co2_savings.to_dict(orient='records'),
            "solutions": co2_savings_options},
        'energy_recovered_optimization': {
            "best_options": energy_recovered.to_dict(orient='records'),
            "solutions": energy_recovered_options},
        'energy_investment_optimization': {
            "best_options": energy_investment.to_dict(orient='records'),
            "solutions": energy_investment_options},
    }

    report_html = pinch_report(output_pinch)

    # output
    output_pinch = {
        'co2_optimization': co2_savings.to_dict(orient='records'),
        'energy_recovered_optimization': energy_recovered.to_dict(orient='records'),
        'energy_investment_optimization': energy_investment.to_dict(orient='records')
    }

    output = {
            'best_options': output_pinch,
            'report': report_html
    }


    return output



