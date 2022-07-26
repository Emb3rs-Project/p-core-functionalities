from .....Source.simulation.Heat_Recovery.Pinch.Auxiliary.pinch_analysis import pinch_analysis
from .....Source.simulation.Heat_Recovery.Pinch.Auxiliary.get_best_x_outputs import get_best_x_outputs
from .....General.Auxiliary_General.get_country import get_country
import itertools
import pandas as pd
from .....utilities.kb import KB
from .....Error_Handling.runtime_error import ModuleRuntimeException
from .....Error_Handling.error_pinch import error_convert_pinch
from .....Reports.pinch_report import pinch_report


def convert_pinch(in_var, kb: KB):
    """Main function of Pinch Analysis

    Includes data pretreatment, pinch analysis, and economic/co2 analysis of the options designed.
    Return the best three solutions for: minimum CO2 emissions ,maximize energy recovery, and energy recovery specific cost.

    Parameters
    ----------
    in_var : dict
        Data for pinch analysis, with the following key:

            platform :  dict
                Platform Data

                    streams_to_analyse : list
                        List with streams ID to analyse

                    pinch_delta_T_min: float
                        Minimum delta temperature for pinch analysis [ºC]

                    all_input_objects : list
                        List with:
                            - equipments (check Source/characterization/Generate_Equipment)
                            - processes (check Source/characterization/Process/process)
                            - isolated streams (check General/Simple_User/isolated_stream)

                    location:  list
                        [latitude, longitude] [º]

                    lifetime : int, optional
                        Heat exchangers lifetime. DEFAULT=20

                    fuels_data: dict:
                        Fuels price and CO2 emission, with the following keys:

                            - natural_gas: dict
                                Natural gas data

                                    - co2_emissions: float:
                                        Fuel CO2 emission [kg CO2/kWh]

                                    - price: float:
                                        Fuel price [€/kWh]

                            - fuel_oil
                                Same keys as "natural_gas"

                            - electricity
                                Same keys as "natural_gas"

                            - biomass
                                Same keys as "natural_gas"

                    number_output_options: int, optional
                        Number of solutions of each category to return. DEFAULT=3

                    interest_rate : float, optional
                        Interest rate considered for BM

    kb : dict
        Knowledge Base

    Returns
    -------
    pinch_output : dict
        Pinch analysis, with the following keys:

            best_options : dict
                Three categories, with the respective following keys:

                    co2_optimization : list
                        List with dicts, with best design options that minimize CO2 emissions. Each solution with the following
                        keys:

                            ID : int
                                Designed solution ID

                            streams : list
                                Streams ID in pinch design

                            streams_info : list
                                array with dicts

                            capex : float
                                Solution capex [€]

                            om_fix : float
                                Yearly OM fix costs [€/year]

                            hot_utility : float
                                Power of the hot utility needed, so that the cold streams reach their target_temperature [kW]

                            cold_utility : float
                                Power of the cold utility needed, so that the hot streams reach their target_temperature [kW]

                            lifetime : float
                                Considered lifetime  [year]

                            co2_savings : float
                                Annualized co2 savings by implementing the pinch design [kg CO2/kWh]

                            money_savings : float
                                Annualized energy savings by implementing the pinch design  [€/kWh]

                            energy_dispatch : float
                                Yearly energy recovered by implementing the pinch design [kWh/year]

                            discount_rate : float
                                Financial parameter for the BM []

                            pinch_temperature : float
                                Design pinch temperature [ºC]

                            theo_minimum_hot_utility : float
                                Theoretical power of the hot utility needed, so that the cold streams reach their target temperature [kW]

                            theo_minimum_cold_utility : float
                                Theoretical power of the cold utility needed, so that the hot streams reach their target temperature [kW]

                            pinch_hx_data : list
                                Each heat exchanger technical/economical data,with the following keys:

                                    - HX_Power : float
                                        Heat exchanger power [kW]

                                    - HX_Hot_Stream : int
                                        Hot stream ID

                                    - HX_Cold_Stream : int
                                        Cold stream ID

                                    - HX_Original_Hot_Stream : int
                                        Hot stream ID (there might be a split, meaning that  HX_Original_Hot_Stream != HX_Hot_Stream)

                                    - HX_Original_Cold_Stream : int
                                        Cold stream ID (there might be a split, meaning that  HX_Original_Cold_Stream != HX_Cold_Stream)

                                    - HX_Type : str
                                        Heat exchanger type

                                    - HX_Turnkey_Cost : float
                                        Heat exchanger capex [€]

                                    - HX_OM_Fix_Cost : float
                                        Heat exchanger OM Fix [€/year]

                                    - HX_Hot_Stream_T_Hot : float
                                        Hot stream hot temperature[ºC]

                                    - HX_Hot_Stream_T_Cold : float
                                        Hot stream cold temperature[ºC]

                                    - HX_Cold_Stream_T_Hot : float
                                        Cold stream hot temperature[ºC]

                                    - HX_Cold_Stream_T_Cold : float
                                        Cold stream cold temperature[ºC]

                                    - Storage : float
                                        Storage volume [m3]

                                    - Storage_Satisfies : float
                                        Percentage of capacity in mismatch hours that storaeg satisfies [%]

                                    - Storage_Turnkey_Cost : float
                                        Storage capex [€]

                                    - Total_Turnkey_Cost : float
                                        Heat exchanger + storage copex [€]

                                    - Recovered_Energy : float
                                        Amount of energy recovered [kWh]


                    energy_recovered_optimization : list
                        List with best design options of the respective category -> similar to "co2_optimization"

                    energy_investment_optimization : list
                        List with best design options of the respective category -> similar to "co2_optimization"

            report : str
                HTML Report
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
                'capex': df_hx['Total_Turnkey_Cost'].sum(),
                'om_fix': df_hx['HX_OM_Fix_Cost'].sum()
            })


    df_optimization = pd.DataFrame(list_df_optimization)

    if df_optimization.empty == True:
        raise Exception('Heat Recovery solutions were not found.')


    df_optimization['index'] = df_optimization['index'] + 1

    # drop duplicates
    df_optimization = df_optimization.drop_duplicates(subset=['co2_savings', 'energy_recovered', 'energy_investment', 'capex'])

    # info for HTML
    df_char.drop(['Supply_Shift','Target_Shift'], axis=1,inplace=True)
    df_char.rename(columns=lambda name: name.replace('_', ' '),inplace=True)
    df_char['Fluid'] = df_char['Fluid'].apply(lambda x: x.replace("_", " "))
    stream_table = df_char

    stream_combination_not_feasible = subset_not_possible_to_analyze


    # get best options that recover maximum energy
    energy_recovered = df_optimization.sort_values('energy_recovered', ascending=False).head(number_output_options).copy()
    energy_recovered_options = get_best_x_outputs(pinch_designed_solutions, energy_recovered,  lifetime, pinch_delta_T_min,
                                                  stream_table,stream_combination_not_feasible, interest_rate=interest_rate)

    # get best options that give best energy_recovery/turnkey ratio
    energy_investment = df_optimization.sort_values('energy_investment').head(number_output_options).copy()
    energy_investment_options = get_best_x_outputs(pinch_designed_solutions, energy_investment, lifetime,
                                                   pinch_delta_T_min, stream_table,stream_combination_not_feasible, interest_rate=interest_rate)

    # get best options that save maximum amount of CO2
    co2_savings = df_optimization.sort_values('co2_savings', ascending=False).head(number_output_options).copy()
    co2_savings_options = get_best_x_outputs(pinch_designed_solutions, co2_savings, lifetime, pinch_delta_T_min, stream_table,stream_combination_not_feasible, interest_rate=interest_rate)


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

    new_co2_savings_options = []
    for option in co2_savings_options:
        new_co2_savings_options.append({your_key: option[your_key] for your_key in ["ID",
                                                                           "capex",
                                                                           "om_fix",
                                                                           "lifetime",
                                                                           "co2_savings",
                                                                           "money_savings",
                                                                           "energy_dispatch",
                                                                           "discount_rate"]})
    new_energy_investment_options = []
    for option in energy_investment_options:
        new_energy_investment_options.append({your_key: option[your_key] for your_key in ["ID",
                                                                           "capex",
                                                                           "om_fix",
                                                                           "lifetime",
                                                                           "co2_savings",
                                                                           "money_savings",
                                                                           "energy_dispatch",
                                                                           "discount_rate"]})

    new_energy_recovered_options = []
    for option in energy_recovered_options:
        new_energy_recovered_options.append({your_key: option[your_key] for your_key in ["ID",
                                                                           "capex",
                                                                           "om_fix",
                                                                           "lifetime",
                                                                           "co2_savings",
                                                                           "money_savings",
                                                                           "energy_dispatch",
                                                                           "discount_rate"]})

    # output
    output_pinch = {
        'co2_optimization': new_co2_savings_options,
        'energy_recovered_optimization': new_energy_recovered_options, # energy_recovered.to_dict(orient='records'),
        'energy_investment_optimization': new_energy_investment_options  #energy_investment.to_dict(orient='records')
    }

    output = {
            'best_options': output_pinch,
            'report': report_html
    }


    return output



