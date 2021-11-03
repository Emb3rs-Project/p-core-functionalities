"""

##############################
Info: Main function of Heat Recovery Module. Compute and plot GCC, find pinch point, pinch analysis above/below pinch
point and HX design for maximum energy recovery

##############################
INPUT: object with:

        # id   # process id
        # equipment  # heat/cooling equipment id associated to
        # operation_temperature  # process operation_temperature [ºC]


##############################
Return: dictionary with 3 keys:

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

from .....KB_General.fluid_material import fluid_material_cp
from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.pinch_analysis import pinch_analysis
from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.table_heat_cascade import table_heat_cascade
from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.pinch_point import pinch_point
import pandas as pd
from .....KB_General.fuel_properties import fuel_properties
from .....Source.simulation.Heat_Recovery.PINCH.Auxiliary.get_best_3_outputs import get_best_3_outputs


def convert_pinch(in_var):

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
    vector_df_hx.append(df_hx_bulk)

    # compute max total heat recoverable
    df_heat_cascade = table_heat_cascade(df_operating)
    pinch_point_T, net_heat_flow = pinch_point(df_heat_cascade)
    total_heat = 0

    if df_hx_bulk.empty == False:
        for i in range(df_operating.shape[0]) :
            total_heat += df_operating.iloc[i]['mcp'] * abs(
                df_operating.iloc[i]['Supply_Temperature'] - df_operating.iloc[i]['Target_Temperature'])

    minimum_heat = net_heat_flow[0] * 1000 + net_heat_flow[-1] * 1000  # kWh
    max_heat_recoverable = (total_heat - minimum_heat) / 2



    # Hourly Pinch Analysis  --------------------------------------------------------
    if perform_hourly == 1:
            # Get vector with Unique Hour_ID
            unique_hour_id = df_profile.iloc[-1].unique() # vector wih unique hour_id sorted

            for hour_id in unique_hour_id:
                index_df = []
                if hour_id != 0:
                    reverse_hour_id = str(int(hour_id))[::-1]
                    for i in range(len(reverse_hour_id)):
                        if reverse_hour_id[i] == '1':
                            index_df.append(int(i)) # list with equipments/processes ID operating

                    df_operating = (df_char.copy()).iloc[index_df]
                    df_hx = pinch_analysis(df_operating,df_profile,delta_T_min)

                    if df_hx.empty == False:
                        vector_df_hx.append(df_hx)

    # Hourly percentage recovered heat
    for df_hx in vector_df_hx:
            recovered_heat = sum(df_hx['Power'].values)


    # Create economic DF's (e.g total_investment, energy and money saved yearly - and in which equipment)
    all_df = []

    if objects != []:

        for df_hx in vector_df_hx:
            df_economic = pd.DataFrame(columns=['Equipment_ID',
                                                'Recovered_Energy',
                                                'CO2_Savings_Year',
                                                'Savings_Year',
                                                'Total_Turnkey_Cost'])
            for index, row in df_hx.iterrows():
                find = True
                while find == True:
                    for object in objects: #processes/equipment
                        for stream in object['streams']:
                            if stream['id'] == row['Original_Cold_Stream']:
                                save_object = object
                                find = False
                                break
                        if find == False: # match found
                            break
                    if find == True: # no match found - may happen with isolated streams
                        break
                if find == True:  # no match found - may happen with isolated streams
                    pass
                else:
                    if save_object['object_type'] == 'equipment':
                        data = fuel_properties('Portugal',save_object.fuel_type,'non-household')

                        CO2_emission_per_kw = float(data['CO2_emission'])
                        cost = data['price']
                        df_economic = df_economic.append({'Equipment_ID': save_object['id'],
                                                          'CO2_Savings_Year': row['Recovered_Energy'] * CO2_emission_per_kw,
                                                          'Recovered_Energy':  row['Recovered_Energy'],
                                                          'Savings_Year': row['Recovered_Energy'] * cost,
                                                          'Total_Turnkey_Cost': row['Total_Turnkey_Cost'], }
                                                         , ignore_index=True)

                    elif save_object['object_type'] == 'process':  # object.type = 'process'

                        for equipment in all_objects:
                            if save_object['equipment'] == equipment['id']:  # find equipment that supplies process
                                break
                            else:
                                equipment = 'not found'


                        data = fuel_properties('Portugal', equipment['fuel_type'], 'non-household')
                        cost = data['price']
                        CO2_emission_per_kw = data['co2_emissions']

                        df_economic = df_economic.append({
                                                             'Equipment_ID':save_object['equipment'],
                                                             'CO2_Savings_Year':row[
                                                                                    'Recovered_Energy'] * CO2_emission_per_kw,
                                                             'Recovered_Energy':row['Recovered_Energy'],
                                                             'Savings_Year':row['Recovered_Energy'] * cost,
                                                             'Total_Turnkey_Cost':row['Total_Turnkey_Cost'], }
                                                         , ignore_index=True)

                    else: # object.type = 'isolated_stream'
                        #################
                        #manuly flow
                        df_economic = df_economic.append({
                            'Equipment_ID':'isolated_stream',
                            'CO2_Savings_Year':row['Recovered_Energy'] * CO2_emission_per_kw,
                            'Recovered_Energy':row['Recovered_Energy'],
                            'Savings_Year':row['Recovered_Energy'] * cost,
                            'Total_Turnkey_Cost':row['Total_Turnkey_Cost'], }
                            , ignore_index=True)




                # Agreggate same Equipment ID savings in df_equipment_economic
                equipment_id = df_economic['Equipment_ID'].values

                for id in equipment_id:
                    df_equipment_economic = pd.DataFrame(columns=['Equipment_ID', 'Recovered_Energy', 'CO2_Savings_Year','Savings_Year','Total_Turnkey_Cost'])
                    df_equipment_id = df_economic[df_economic['Equipment_ID'] == id]
                    total_recovered_heat = df_equipment_id['Recovered_Energy'].sum()
                    total_savings_year = df_equipment_id['Savings_Year'].sum()
                    total_turnkey = df_equipment_id['Total_Turnkey_Cost'].sum()

                    for equipment in all_objects:
                        if id == equipment['id']:  # find equipment that supplies process
                            break
                    df_equipment_economic = df_equipment_economic.append({'Equipment_ID': id,
                                                                  'CO2_Savings_Year': row['Recovered_Energy'] * CO2_emission_per_kw,
                                                                  'Recovered_Energy': total_recovered_heat,
                                                                  'Savings_Year': total_savings_year,
                                                                  'Total_Turnkey_Cost': total_turnkey, }
                                                                 , ignore_index=True)

            all_df.append([df_hx,df_equipment_economic])


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



