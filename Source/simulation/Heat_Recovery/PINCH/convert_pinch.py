"""
alisboa/jmcunha

##############################
INFO: Main function of Heat Recovery Module. Compute GCC (Grand Composite Curve), find pinch point, pinch analysis above/below pinch
point and HX design for maximum energy recovery and co2 minimization

##############################
INPUT: object with:

        # id   # process id
        # equipment  # heat/cooling equipment id associated to
        # operation_temperature  # process operation_temperature [ºC]


##############################
RETURN: dictionary with 3 keys:

            # co2_optimization - vector with 3 dictionaries for the 3 best max co2 emissions saving
            # energy_recovered_optimization - vector with 3 dictionaries for the 3 best max energy recovered
            # energy_investment_optimization - vector with 3 dictionaries for the 3 best max energy_recovered/turnkey

            Where in each one:
                # total_turnkey [€]
                # total_co2_savings [kg CO2]
                # total_energy_recovered [kWh]
                # pinch_hx_data
                # equipment_detailed_savings

                Where in pinch_hx_data - a DF turned in a dictionary with:
                    DF  -['Power' [kW], 'Hot_Stream' [ID], 'Cold_Stream' [ID], 'Type' [hx type], 'HX_Turnkey_Cost' [€], 'OM_Fix_Cost'  [€/year],
                    'Hot_Stream_T_Hot'  [ºC],'Hot_Stream_T_Cold'  [ºC],'Original_Hot_Stream' [ID], 'Original_Cold_Stream ' [ID], 'Storage'  [m3],
                     'Storage_Satisfies' [%], 'Storage_Turnkey_Cost'  [€],
                     'Total_Turnkey_Cost'  [€], 'Recovered_Energy'  [kWh]]

                Where in equipment_detailed_savings - a DF turned in a dictionary with:
                    DF - ['Equipment_ID' [ID], 'CO2_Savings_Year' [kg] ,'Recovered_Energy'  [kWh],'Savings_Year'  [€] :  ,
                    'Total_Turnkey_Cost'  [€]]

"""

from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.pinch_analysis import pinch_analysis
import pandas as pd
from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.get_best_3_outputs import get_best_3_outputs
from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.eco_env_analysis import eco_env_analysis
from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.streams_detailed_info import streams_detailed_info
from .....KB_General.fuel_properties import fuel_properties

import itertools

  
def convert_pinch(in_var):

    # INPUT -------
    all_objects = in_var.all_objects  # equipments/processes/isolated streams
    pinch_delta_T_min = in_var.pinch_delta_T_min
    hx_delta_T = in_var.hx_delta_T

    # Defined Vars
    perform_hourly_analysis = False  # only perform hourly analysis for isolated streams and processes
    vector_df_hx =[]
    objects = []
    streams = []
    individual_equipment_optimization = False
    just_isolated_streams = False

    ############################################################################################################
    # DATA PRE-TREATMENT
    pinch_delta_T_min = (pinch_delta_T_min)/2
    # analyse processes and isolated streams to build the streams list
    for object in all_objects:
        if object['object_type'] == 'process':  # from processes
            perform_hourly_analysis = True
            objects.append(object)
            for stream in object['streams']:
                if stream['stream_type'] != 'maintenance' and stream['stream_type'] != 'startup':
                    streams.append(stream)
        elif object['object_type'] == 'stream':  # isolated stream
            perform_hourly_analysis = True
            object['id'] = object['id']
            streams.append(object)


   # if 'objects' is empty, it means analyse equipment internal heat recovery
    if objects == [] and streams == []:
        object = all_objects[0]
        if object['object_type'] == 'equipment':
            objects.append(object)
            # get equipment excess heat and inflow to perform energy recovery
            for stream in object['streams']:
                if stream['stream_type'] == 'excess_heat' or stream['stream_type'] == 'inflow':
                    streams.append(stream)


    # create DF with streams characteristics (df_char) and  DF with only streams profiles (df_profile)
    df_char = pd.DataFrame(columns=['ID', 'Fluid', 'Flowrate', 'Supply_Temperature', 'Target_Temperature'])
    df_profile_data = []

    for stream in streams:
        if stream['stream_type'] != 'supply_heat':
            df_char = df_char.append({'ID':stream['id'],
                                      'Fluid': stream['fluid'],
                                      'Flowrate': stream['flowrate'],
                                      'Supply_Temperature': stream['supply_temperature'],
                                      'Target_Temperature': stream['target_temperature']}, ignore_index=True)

            # create vector with streams profiles
            df_profile_data.append(stream['schedule'])

    df_profile = pd.DataFrame(data=df_profile_data)  # create df
    df_profile.set_index(df_char['ID'],inplace=True)
    df_char.set_index('ID',inplace=True)

    # get all streams info necessary for pinch analysis
    df_char = streams_detailed_info(df_char, pinch_delta_T_min)


    ############################################################################################################
    # PINCH ANALYSIS

    # pinch analysis for all streams
    df_operating = df_char.copy()  # provide streams to be analyzed
    df_hx_bulk = pinch_analysis(df_operating, df_profile, pinch_delta_T_min,hx_delta_T)
    for df in df_hx_bulk:
        vector_df_hx.append(df)


    get_data = []
    # do all possible combinations between the streams
    for L in range(0, len(range(df_char.shape[0]))):
            for subset in itertools.combinations(range(df_char.shape[0]), L):
                if list(subset) != [] and len(list(subset)) > 1:
                    get_data.append(subset)
    #print('lenn',len(get_data))

   # df_operating_powerful = df_char.copy()
   # df_operating_powerful['mcp_delta_T'] = df_operating_powerful['mcp'] * abs(df_operating_powerful['Supply_Temperature'] - df_operating_powerful['Target_Temperature'])
   # get_max_powerful_hot = df_operating_powerful[df_operating_powerful['Stream_Type'] == 'Hot']
    #get_max_powerful_cold

    # pinch analysis for all stream combination
    # (overlap schedule 80% e/ou 30% energy)
    i = 0
    perform_hourly_analysis = True
    if perform_hourly_analysis is True:
        # do all possible combinations between the streams
        for L in range(0, len(range(df_char.shape[0]))):
            for subset in itertools.combinations(range(df_char.shape[0]), L):
                if list(subset) != [] and len(list(subset)) > 1:
                    df_operating = (df_char.copy()).iloc[list(subset)]
                    if df_operating[df_operating['Stream_Type'] == 'Hot'].empty == False and df_operating[df_operating['Stream_Type'] == 'Cold'].empty == False:
                        df_hx_hourly = pinch_analysis(df_operating, df_profile, pinch_delta_T_min,hx_delta_T)
                        if df_hx_hourly != []:
                            for df in df_hx_hourly:
                                vector_df_hx.append(df)
                    i += 1


    ############################################################################################################
    # ECONOMIC/CO2 EMISSIONS ANALYSIS

    # economic DF's (e.g total_investment, energy and money saved yearly - and in which equipment)
    all_df = []
    if objects != []:
        all_df = eco_env_analysis(vector_df_hx,objects,all_objects,all_df)
    else:
        individual_equipment_optimization = True
        empty_data = None
        empty_df = pd.DataFrame(empty_data,columns=['None'])

        for df in vector_df_hx:
            all_df.append([df,empty_df])



    optimization_row = pd.DataFrame(columns=['index',
                                            'co2_savings',
                                            'energy_saving',
                                            'energy_investment',
                                            'turnkey'
                                            ])
    try:
        if individual_equipment_optimization is False:
            for index,info in enumerate(all_df):
                pinch_data, economic_data = info
                optimization_row = optimization_row.append({'index':index,
                                       'co2_savings':economic_data['CO2_Savings_Year'].sum(),
                                       'money_savings':economic_data['Savings_Year'].sum(),
                                       'energy_recovered':economic_data['Recovered_Energy'].sum(),
                                       'energy_investment':pinch_data['Total_Turnkey_Cost'].sum() /economic_data['Recovered_Energy'].sum() ,
                                       'turnkey':pinch_data['Total_Turnkey_Cost'].sum(),
                                       'om_fix':pinch_data['HX_OM_Fix_Cost'].sum()}
                                       ,ignore_index=True)

        #############################################################################
        # only recovering equipments excess heat in its inflow - STILL DEVELOPING
        else:

            for index,info in enumerate(all_df):
                pinch_data, economic_data = info

                if object['object_type'] == 'equipment':
                    data = fuel_properties('Portugal', object['fuel_type'], 'non-household')
                    co2_emission_per_kw = data['co2_emissions']
                    fuel_cost_kwh = data['price']
                else:
                    co2_emission_per_kw = 0
                    fuel_cost_kwh = 0
                    just_isolated_streams = True

                optimization_row = optimization_row.append({'index':index,
                                       'co2_savings': pinch_data['Recovered_Energy'].sum() * co2_emission_per_kw,
                                       'money_savings': pinch_data['Recovered_Energy'].sum() * fuel_cost_kwh,
                                       'energy_recovered': pinch_data['Recovered_Energy'].sum(),
                                       'energy_investment': pinch_data['Total_Turnkey_Cost'].sum()/pinch_data['Recovered_Energy'].sum() ,
                                       'turnkey': pinch_data['Total_Turnkey_Cost'].sum(),
                                       'om_fix': pinch_data['HX_OM_Fix_Cost'].sum()}
                                       ,ignore_index=True)


        optimization_row = optimization_row.drop_duplicates(subset=['co2_savings', 'energy_recovered', 'energy_investment', 'turnkey'])

        # get best 3 options that recover maximum energy
        energy_recovered = optimization_row.sort_values('energy_recovered', ascending=False).head(3)
        energy_recovered_options = get_best_3_outputs(all_df, energy_recovered)

        # get best 3 options that give best energy_recovery/turnkey ratio
        energy_investment = optimization_row.sort_values('energy_investment').head(3)
        energy_investment_options = get_best_3_outputs(all_df, energy_investment)

        # get best 3 options that save maximum amount of co2
        co2_savings = optimization_row.sort_values('co2_savings', ascending=False).head(3)
        co2_savings_options = get_best_3_outputs(all_df, co2_savings)

        if just_isolated_streams == True:
            co2_savings_options = []

        output = {'co2_optimization': co2_savings_options,
                  'energy_recovered_optimization': energy_recovered_options,
                  'energy_investment_optimization': energy_investment_options
                  }

    except:
        print('Error in convert_pinch. Probably no HX designed')
        output = []


    return output



