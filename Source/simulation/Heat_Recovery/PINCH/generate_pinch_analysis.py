"""
@author: jmcunha/alisboa

Info: This function only performs a pinch analysis.

Return: HX Design between streams

"""
from .....KB_General.fluid_material import fluid_material_cp
from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.pinch_analysis import pinch_analysis
import pandas as pd


def generate_heat_recovery(in_var):

    # Input
    all_objects = in_var.all_objects # equipments/processes
    delta_T_min =in_var.delta_T_min

    # Defined Vars
    perform_hourly = 0
    vector_df_hx =[]
    objects = []
    streams = []
    individual_equipment_optimization = False

    delta_T_min = (delta_T_min)/2 # HX Minimum DT
    new_id=1
    # Computation
    # Analyse processes, and build streams list
    for object in all_objects:
        print(object)
        if object['object_type'] == 'process':
            perform_hourly = 1
            objects.append(object)
            for stream in object['streams']:
                streams.append(stream)
        elif object['object_type'] == 'stream': # isolated stream
            perform_hourly = 1
            object['id'] = new_id
            streams.append(object)
            new_id += 1


   # If 'objects' is empty, it means analyse equipment internal heat recovery
    if objects == [] and streams == []:
        object = all_objects[0]
        if object['object_type'] == 'equipment':
            objects.append(object)
            for stream in object['streams']:
                if stream['stream_type'] == 'excess_heat' or stream['stream_type'] == 'inflow' or stream['stream_type'] == 'startup':
                    streams.append(stream)




    # Create DF's of streams (df_char) and profiles (df_profile)
    df_char = pd.DataFrame(columns=['ID','Fluid', 'Flowrate', 'Supply_Temperature', 'Target_Temperature'])
    df_profile_data = []

    for stream in streams:
        if stream['stream_type'] != 'supply_heat':
            df_char = df_char.append({'ID':stream['id'],
                                      'Fluid': stream['fluid'],
                                      'Flowrate': stream['flowrate'],
                                      'Supply_Temperature': stream['supply_temperature'],
                                      'Target_Temperature': stream['target_temperature']}, ignore_index=True)

            df_profile_data.append(stream['schedule'])  # create vector with streams profiles

    df_profile = pd.DataFrame(data=df_profile_data) # create df
    df_profile.set_index(df_char['ID'],inplace=True)
    df_char.set_index('ID',inplace=True)


    # DF Profile - Compute Hour ID's
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


    # DF Characteristics - Compute needed data
    df_char['Cp'] = df_char.apply(
        lambda row: fluid_material_cp(row['Fluid'], row['Supply_Temperature']), axis=1
    )

    df_char['mcp'] = df_char['Flowrate'] * df_char['Cp'] / 3600  # [kW/K]

    df_char['Stream_Type'] = df_char.apply(
        lambda row: 'Hot' if row['Supply_Temperature']>row['Target_Temperature']
        else 'Cold', axis=1
    )

    df_char['Supply_Shift'] = df_char.apply(
        lambda row:  row['Supply_Temperature'] - delta_T_min  if row['Stream_Type'] == 'Hot'
        else row['Supply_Temperature'] + delta_T_min, axis=1
    )

    df_char['Target_Shift'] = df_char.apply(
        lambda row:  row['Target_Temperature'] - delta_T_min  if row['Stream_Type'] == 'Hot'
        else row['Target_Temperature'] + delta_T_min, axis=1
    )


    # Bulk Pinch Analysis  --------------------------------------------------------
    df_operating = (df_char.copy())
    df_hx_bulk = pinch_analysis(df_operating, df_profile, delta_T_min)


    output = df_hx_bulk.__dict__
    return output