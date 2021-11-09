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
import itertools

  
def convert_pinch(in_var):

    # INPUT -------
    all_objects = in_var.all_objects  # equipments/processes/isolated streams
    delta_T_min = in_var.delta_T_min

    # Defined Vars
    perform_hourly_analysis = False  # only perform hourly analysis for isolated streams and processes
    vector_df_hx =[]
    objects = []
    streams = []
    individual_equipment_optimization = False
    new_id = 1

    ############################################################################################################
    # DATA PRE-TREATMENT

    pinch_delta_T_min = (delta_T_min)/2  # HX minimum DT

    # analyse processes and isolated streams to build the streams list
    for object in all_objects:
        if object['object_type'] == 'process':  # from processes
            perform_hourly_analysis = True
            objects.append(object)
            for stream in object['streams']:
                streams.append(stream)
        elif object['object_type'] == 'stream':  # isolated stream
            perform_hourly_analysis = True
            object['id'] = new_id
            streams.append(object)
            new_id += 1

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

    # Bulk Pinch Analysis  --------------------------------------------------------
    # pinch analysis for all streams
    df_operating = df_char.copy()  # provide streams to be analyzed
    df_hx_bulk = pinch_analysis(df_operating, df_profile, pinch_delta_T_min)
    vector_df_hx.append(df_hx_bulk)

    # pinch analysis for all stream combination
    if perform_hourly_analysis is True:
        # do all possible combinations between the streams
        for L in range(0, len(range(df_char.shape[0]))):
            for subset in itertools.combinations(range(df_char.shape[0]), L):
                if list(subset) != [] and len(list(subset)) > 1:
                    df_operating = (df_char.copy()).iloc[list(subset)]
                    df_hx_hourly = pinch_analysis(df_operating, df_profile, pinch_delta_T_min)
                    if df_hx_hourly.empty == False:
                        vector_df_hx.append(df_hx_hourly)



    hour = 0
    if hour == 1 :
        # Hourly Pinch Analysis  --------------------------------------------------------
        # DF Profile - compute hour ID's
        total = df_profile.sum(axis=0)
        total.name = 'Total'
        num_rows = df_profile.shape[0]
        factor = []

        for i in range(num_rows):  # necessary to create hour id
            factor.append(10 ** i)

        df_profile = df_profile.mul(factor, axis=0)
        hour_id = df_profile.iloc[0:].sum()
        df_profile = df_profile.div(factor, axis=0)
        hour_id.name = 'Hour_ID'
        df_profile = df_profile.append(total.transpose())
        df_profile = df_profile.append(hour_id.transpose())

        # pinch analysis for streams working in coincident hours ID
        if perform_hourly_analysis is True:
                # get sorted vector with Unique Hour_ID
                unique_hour_id = df_profile.iloc[-1].unique()
                all_streams_working_hour_id = sum([10**(i) for i in range(len(str(int(unique_hour_id[0]))))])
                if unique_hour_id[0] == all_streams_working_hour_id:
                    unique_hour_id = unique_hour_id[1:]

                for hour_id in unique_hour_id:
                    index_df = []
                    if hour_id != 0:
                        reverse_hour_id = str(int(hour_id))[::-1]
                        for i in range(len(reverse_hour_id)):
                            if reverse_hour_id[i] == '1':
                                index_df.append(int(i))  # list with equipments/processes ID operating

                        df_operating = (df_char.copy()).iloc[index_df]
                        df_hx_hourly = pinch_analysis(df_operating,df_profile,pinch_delta_T_min)
                        if df_hx_hourly.empty == False:
                            vector_df_hx.append(df_hx_hourly)


    ############################################################################################################
    # ECONOMIC/CO2 EMISSIONS ANALYSIS

    # economic DF's (e.g total_investment, energy and money saved yearly - and in which equipment)
    all_df = []
    if objects != []:
        all_df = eco_env_analysis(vector_df_hx,objects,all_objects,all_df)

    else:
        individual_equipment_optimization = True
        all_df.append([df_hx_bulk,[]])



    if individual_equipment_optimization is False:
        new_df = pd.DataFrame(columns=['index',
                                       'co2_savings',
                                       'energy_saving',
                                       'energy_investment',
                                       'turnkey'
                                       ])

        for index,info in enumerate(all_df):
            pinch_data, economic_data = info
            new_df = new_df.append({'index':index,
                                   'co2_savings':economic_data['CO2_Savings_Year'].sum(),
                                   'energy_recovered':economic_data['Recovered_Energy'].sum(),
                                   'energy_investment':economic_data['Recovered_Energy'].sum() / economic_data['Total_Turnkey_Cost'].sum(),
                                   'turnkey':economic_data['Total_Turnkey_Cost'].sum() }
                                   ,ignore_index=True)

        new_df = new_df.drop_duplicates(subset=['co2_savings', 'energy_recovered', 'energy_investment', 'turnkey'])

        # get best 3 options that save maximum amount of co2
        co2_savings = new_df.sort_values('co2_savings', ascending=False).head(3)
        co2_savings_options = get_best_3_outputs(all_df, co2_savings)

        # get best 3 options that recover maximum energy
        energy_recovered = new_df.sort_values('energy_recovered', ascending=False).head(3)
        energy_recovered_options = get_best_3_outputs(all_df, energy_recovered)

        # get best 3 options that give best energy_recovery/turnkey ratio
        energy_investment = new_df.sort_values('energy_investment').head(3)
        energy_investment_options = get_best_3_outputs(all_df, energy_investment)

        output = {
            'co2_optimization':co2_savings_options,
            'energy_recovered_optimization':energy_recovered_options,
            'energy_investment_optimization':energy_investment_options
            }

    #############################################################################
    # only recovering equipments excess heat in its inflow - STILL DEVELOPING
    else:
        output = {'co2_optimization': {'total': {'turnkey':0,
                                                 'co2_savings':0,
                                                 'energy_recovered':0},
                                       'equipment_detailed_savings':[],
                                       'pinch_hx_data': all_df[0][0].to_dict(orient='records')
                                          },
                 'energy_saving_options': [],
                 'energy_investment_options': []
        }


    return output



