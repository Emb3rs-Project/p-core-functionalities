"""
alisboa/jmcunha


############################################################
INFO: Main function of Heat Recovery Module.
      Includes data pretreatment, pinch analysis, and economic/co2 analysis of the options designed. Economic/CO2
      analysis done for the designed options. Three analysis are done: minimum CO2,maximize energy recovery, and energy
      recovery specific cost according to the solution's CAPEX. The best three solutions for each analysis are provided
      for the user.

      This module runs when isolated streams (streams without equipment associated), equipment and processes or only
      equipment are provided. Analysing the input options:
          - When processes and equipments are provided, it is analyzed the heat recovery only between processes. The
            output,are the three best solutions for the three economic/co2 analysis.
          - When only an equipment is provided, it is analyzed internal heat recovery (e.g. on a boiler, flue gas on air
           inflow). The output is one solution only for the three economic/co2 analysis, since it only designs one HX
           for the equipment internal heat recovery.
          - When isolated streams are provided, it is analyzed its heat recovery . The output are only solutions for the
            two economic analysis (co2 not included), since these streams are not associated to any equipment, and thus
            co2 savings cannot be computed

      Important:
        - Isolated streams may also be provided when equipment and processes are provided.
        - So that the best heat recovery options are found, pinch analysis is, by default, done for all streams
          combination possible.


############################################################
INPUT: object with:
        # pinch_delta_T_min - delta temperature for pinch analysis  [ºC]
        # all_input_objects  - array with equipments/processes/isolated_stream dicts
        # country - country name
        # lifetime  (not mandatory, it is assumed lifetime=20 years)
        # number_output_options (not mandatory, it is assumed number_output_options=3)

            When an equipment (check script at Source/characterization/Generate_Equipment):
            # equipment = {
            #              'id',
            #              'streams', - array with streams dicts
            #              'fuel_type'
            #             }

            When a process (check script at Source/characterization/Process/process):
            # process = {
            #            'id',
            #            'object_type',
            #            'equipment', - associated equipment ID
            #            'streams', - array with streams dicts
            #            }

            When a isolated_stream or streams (from the above objects), for example:
            # stream = {
            #           'id',
            #           'fluid' - fluid name
            #           'flowrate'  [kg/h]
            #           'supply_temperature'  [ºC]
            #           'target_temperature'  [ºC]
            #           'object_id' - associated process/equipment ID
            #           'schedule' - array with hourly schedule, 1=operating and 0_not_operating
            #           'hourly_generation' - array with hourly power [kWh]
            #           }


############################################################
RETURN: dictionary with 3 keys:
            # co2_optimization - array with dictionaries for the best max co2 emissions savings, e.g. co2_optimization = [co2_option_1, co2_option_2,...]
            # energy_recovered_optimization - array with 3 dictionaries for the 3 best max energy recovered
            # energy_investment_optimization - array with 3 dictionaries for the 3 best max energy_recovered/turnkey

            Each one provides the three best design options in dictionaries, each option with the following keys:
            For example in :
                # co2_option_1 = {
                #                 'ID' - designed solution ID  [ID]
                #                 'streams' - streams in pinch design ID [ID]
                #                 'capex'  [€]
                #                 'om_fix' - yearly om fix costs [€/year]
                #                 'hot_utility' - power of the hot utility needed, so that the cold streams reach their target_temperature  [kW]
                #                 'cold_utility' - power of the cold utility needed, so that the hot streams reach their target_temperature  [kW]
                #                 'lifetime' - considered lifetime  [year]
                #                 'co2_savings' - annualized co2 savings by implementing the pinch design [kg CO2/kWh]
                #                 'money_savings' - annualized energy savings by implementing the pinch design  [€/kWh]
                #                 'energy_dispatch' - yearly energy recovered by implementing the pinch design [kWh/year]
                #                 'discount_rate'  []
                #                 'pinch_temperature' - design pinch temperature [ºC]
                #                 'theo_minimum_hot_utility' - theoretical power of the hot utility needed, so that the cold streams reach their target_temperature  [kW]
                #                 'theo_minimum_cold_utility' - theoretical power of the cold utility needed, so that the hot streams reach their target_temperature  [kW]
                #                 'equipment_detailed_savings', - list with equipment details saving when implementing the pinch design
                #                 'pinch_hx_data' - list with pinch design data
                #                 }

                Where in pinch_hx_data various dict with HX designed, e.g. pinch_hx_data=[hx_1,hx_2,...] :
                For example:
                    # hx_1 = {
                    #         'HX_Power'  [kW]
                    #         'HX_Hot_Stream'  [ID]
                    #         'HX_Cold_Stream'  [ID]
                    #         'HX_Original_Hot_Stream'  [ID]
                    #         'HX_Original_Cold_Stream'  [ID]
                    #         'HX_Type'  [hx type]
                    #         'HX_Turnkey_Cost'  [€]
                    #         'HX_OM_Fix_Cost'  [€/year]
                    #         'HX_Hot_Stream_T_Hot'  [ºC]
                    #         'HX_Hot_Stream_T_Cold'  [ºC]
                    #         'HX_Cold_Stream_T_Hot'  [ºC]
                    #         'HX_Cold_Stream_T_Cold'  [ºC]
                    #         'Storage'  [m3]
                    #         'Storage_Satisfies'  [%]
                    #         'Storage_Turnkey_Cost'  [€]
                    #         'Total_Turnkey_Cost'  [€]
                    #         'Recovered_Energy'  [kWh/year]
                    #          }

                Where in equipment_detailed_savings, the following keys:
                    # equipment_detailed_savings = {
                    #                               'Equipment_ID'  [ID]
                    #                               'CO2_Savings_Year'  [kg CO2/year]
                    #                               'Recovered_Energy'  [kWh/year]
                    #                               'Savings_Year'  [€]
                    #                               'Total_Turnkey_Cost'  [€]
                    #                               }


"""

from .....Source.simulation.Heat_Recovery.Pinch.Auxiliary.pinch_analysis import pinch_analysis
from .....Source.simulation.Heat_Recovery.Pinch.Auxiliary.get_best_x_outputs import get_best_x_outputs
from .....Source.simulation.Heat_Recovery.Pinch.Auxiliary.eco_env_analysis import eco_env_analysis
from .....KB_General.fluid_material import fluid_material_cp
from .....KB_General.fuel_properties import fuel_properties
import itertools
import pandas as pd
  
def convert_pinch(in_var):

    ############################################################################################################
    # INPUT
    all_input_objects = in_var.all_input_objects  # equipments/processes/isolated streams
    pinch_delta_T_min = in_var.pinch_delta_T_min
    country = in_var.country
    perform_all_combinations = in_var.perform_all_combinations  # parameter to only perform all combinations for isolated streams and processes.

    try:
        number_output_options = in_var.number_output_options
    except:
        number_output_options = 3

    try:
        lifetime = in_var.lifetime
    except:
        lifetime = 20

    # Defined Vars
    objects_to_analyze = []
    streams = []
    individual_equipment_optimization = False  # parameter to only perform equipment heat recovery
    only_isolated_streams = False  # parameter to check if only isolated streams are given

    ############################################################################################################
    # DATA PRE-TREATMENT
    hx_delta_T = pinch_delta_T_min
    pinch_delta_T_min = pinch_delta_T_min / 2

    # analyse processes and isolated streams to build the streams list
    for object in all_input_objects:

        if object['object_type'] == 'process':  # from processes get streams
            objects_to_analyze.append(object)
            for stream in object['streams']:
                if stream['stream_type'] == 'inflow' or stream['stream_type'] == 'outflow':
                    streams.append(stream)
        elif object['object_type'] == 'stream':  # isolated streams
            streams.append(object)

    # if empty, it means analyse equipment internal heat recovery
    if streams == []:
        object = all_input_objects[0]
        perform_all_combinations = False
        individual_equipment_optimization = True
        if object['object_type'] == 'equipment':
            objects_to_analyze.append(object)
            for stream in object['streams']:
                if stream['stream_type'] == 'excess_heat' or stream['stream_type'] == 'inflow':
                    streams.append(stream)


    # create DF with streams characteristics (df_char) and  DF with only streams profiles (df_profile)
    df_char = pd.DataFrame(columns=['ID', 'Fluid', 'Flowrate', 'Supply_Temperature', 'Target_Temperature'])
    df_profile_data = []

    for stream in streams:
        df_char = df_char.append({'ID': stream['id'],
                                  'Fluid': stream['fluid'],
                                  'Flowrate': stream['flowrate'],
                                  'Supply_Temperature': stream['supply_temperature'],
                                  'Target_Temperature': stream['target_temperature']}, ignore_index=True)

        df_profile_data.append(stream['schedule'])


    df_profile = pd.DataFrame(data=df_profile_data)  # create df
    df_profile.set_index(df_char['ID'], inplace=True)
    df_char.set_index('ID', inplace=True)

    # get all streams info necessary for pinch analysis
    df_char['Cp'] = df_char.apply(
        lambda row: fluid_material_cp(row['Fluid'], row['Supply_Temperature']), axis=1
    )

    df_char['mcp'] = df_char['Flowrate'] * df_char['Cp'] / 3600  # [kW/K]

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


    ############################################################################################################
    # PINCH ANALYSIS
    design_id = 0  # give each design an ID - initial value
    df_operating = df_char.copy()  # provide streams to be analyzed

    # pinch analysis for all streams
    info_pinch, design_id = pinch_analysis(df_operating, df_profile, pinch_delta_T_min, hx_delta_T, design_id)

    # pinch analysis for all streams combinations
    if perform_all_combinations == True:
        for L in range(0, len(range(df_char.shape[0]))):
            for subset in itertools.combinations(range(df_char.shape[0]), L):
                if list(subset) != [] and len(list(subset)) > 1:
                    df_operating = (df_char.copy()).iloc[list(subset)]
                    if df_operating[df_operating['Stream_Type'] == 'Hot'].empty == False and df_operating[
                        df_operating['Stream_Type'] == 'Cold'].empty == False:
                        df_hx_hourly, design_id = pinch_analysis(df_operating, df_profile, pinch_delta_T_min,
                                                                 hx_delta_T, design_id)
                        if df_hx_hourly != []:
                            for df in df_hx_hourly:
                                info_pinch.append(df)


    ############################################################################################################
    # ECONOMIC/CO2 EMISSIONS ANALYSIS
    all_df = []
    empty_data = None
    empty_df = pd.DataFrame(empty_data, columns=['None'])

    # economic and environmental analysis for pinch data
    if objects_to_analyze != []:
        info_pinch = eco_env_analysis(info_pinch, objects_to_analyze, all_input_objects, country)
    else:
        # isolated streams
        only_isolated_streams = True
        for pinch_case in info_pinch:
            pinch_case['df_equipment_economic'] = empty_df


    # DF created to store a template with info needed for all designs
    df_optimization = pd.DataFrame(columns=['index',
                                            'co2_savings',
                                            'energy_saving',
                                            'energy_investment',
                                            'turnkey'
                                            ])

    try:
        # perform full analysis
        if individual_equipment_optimization is False and only_isolated_streams is False:
            for index, info in enumerate(info_pinch):

                if info['analysis_state'] == 'performed':
                    pinch_data = info['df_hx']

                    economic_data = info['df_equipment_economic']
                    df_optimization = df_optimization.append({
                        'index': index,
                        'streams':info['streams'],
                        'co2_savings': economic_data['CO2_Savings_Year'].sum(),
                        'money_savings': economic_data['Savings_Year'].sum(),
                        'energy_recovered': economic_data['Recovered_Energy'].sum(),
                        'energy_investment': pinch_data['Total_Turnkey_Cost'].sum() / economic_data[
                        'Recovered_Energy'].sum(),
                        'turnkey': pinch_data['Total_Turnkey_Cost'].sum(),
                        'om_fix': pinch_data['HX_OM_Fix_Cost'].sum()
                    }, ignore_index=True)


        # equipment internal heat recovery/ only isolated streams
        else:
            for index, info in enumerate(info_pinch):
                pinch_data = info['df_hx']
                if object['object_type'] == 'equipment':
                    data = fuel_properties(country, object['fuel_type'], 'non-household')
                    co2_emission_per_kw = data['co2_emissions']
                    fuel_cost_kwh = data['price']
                else:
                    only_isolated_streams = True
                    co2_emission_per_kw = 0
                    fuel_cost_kwh = 0

                df_optimization = df_optimization.append({
                    'index': index,
                    'co2_savings': pinch_data['Recovered_Energy'].sum() * co2_emission_per_kw,
                    'money_savings': pinch_data['Recovered_Energy'].sum() * fuel_cost_kwh,
                    'energy_recovered': pinch_data['Recovered_Energy'].sum(),
                    'energy_investment': pinch_data['Total_Turnkey_Cost'].sum() / pinch_data['Recovered_Energy'].sum(),
                    'turnkey': pinch_data['Total_Turnkey_Cost'].sum(),
                    'om_fix': pinch_data['HX_OM_Fix_Cost'].sum()
                }, ignore_index=True)


        # drop duplicates
        df_optimization = df_optimization.drop_duplicates(
            subset=['co2_savings', 'energy_recovered', 'energy_investment', 'turnkey'])

        # get best options that recover maximum energy
        energy_recovered = df_optimization.sort_values('energy_recovered', ascending=False).head(number_output_options)
        energy_recovered_options = get_best_x_outputs(info_pinch, energy_recovered, country, lifetime)

        # get best options that give best energy_recovery/turnkey ratio
        energy_investment = df_optimization.sort_values('energy_investment').head(number_output_options)
        energy_investment_options = get_best_x_outputs(info_pinch, energy_investment, country, lifetime)

        # get best options that save maximum amount of CO2
        co2_savings = df_optimization.sort_values('co2_savings', ascending=False).head(number_output_options)
        co2_savings_options = get_best_x_outputs(info_pinch, co2_savings, country, lifetime)

        # isolated streams are not linked to any equipment, thus not possible to know how much CO2 is saved
        if only_isolated_streams == True:
            co2_savings_options = []

        output = {
            'co2_optimization': co2_savings_options,
            'energy_recovered_optimization': energy_recovered_options,
            'energy_investment_optimization': energy_investment_options
        }

    except:
        print('Error in convert_pinch. Probably no possible solution or complex case. ')
        output = []


    return output


