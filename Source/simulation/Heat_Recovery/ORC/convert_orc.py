"""
##############################
INFO: Convert_Options Raw Data to ORC/RC, for maximum electrical generation.

##############################
INPUT:  streams =
        consumer_type =
        country =
        get_best_number =

##############################
OUTPUT:


"""

import matplotlib.pyplot as plt
from Source.simulation.Heat_Recovery.ORC.Auxiliary.convert_aux import convert_aux
import itertools
from KB_General.equipment_details import equipment_details
import pandas as pd
from General.Simple_User.simple_user import simple_user

def convert_orc(in_var):

    # INPUT ----
    streams = in_var.streams
    consumer_type = in_var.consumer_type
    country = in_var.country
    get_best_number = in_var.get_best_number

    # Initialize Arrays
    output = []
    convert_info = []

    # Defined vars
    minimum_orc_power = 100  # [kW]
    hx_delta_T = 5
    hx_efficiency = 0.95
    power_fraction = 0.05
    pumping_delta_T = 30  # [ºC]

    # ORC Characteristics
    orc_T_evap = 110  # [ºC]
    orc_T_cond = 30   # [ºC]
    hx_orc_supply_temperature = orc_T_evap + hx_delta_T
    hx_orc_return_temperature = hx_orc_supply_temperature - pumping_delta_T

    # Intermediate Circuit Characteristics
    intermediate_fluid = 'water'

    # COMPUTE ------
    # check if streams temperature enough to be converted
    df_streams = pd.DataFrame.from_dict(streams)
    df_streams = df_streams.drop(df_streams[df_streams['target_temperature'] < hx_orc_return_temperature].index)
    df_streams = df_streams.drop(df_streams[df_streams['supply_temperature'] < hx_orc_supply_temperature].index)
    df_streams = df_streams.drop(df_streams[df_streams['capacity'] < minimum_orc_power].index)

    # get best 5
    df_streams['sum_hourly_generation'] = df_streams.apply(lambda x: sum(x['hourly_generation']), axis=1)
    df_streams_best_five = df_streams.sort_values('hourly_generation',ascending=False).head(n=get_best_number)
    streams_best_five_index = df_streams_best_five.index.tolist()

    # do all possible combinations between the 5 streams
    combinations = []
    for L in range(0, len(streams_best_five_index) + 1):
        for subset in itertools.combinations(streams_best_five_index, L):
            if list(subset) != []:
                combinations.append(list(subset))

    # compute stream convertion info when aggregated and not aggregated
    streams_info = {}
    for stream_index in streams_best_five_index:
        stream = streams[stream_index]

        # Individual Stream
        aggregate_streams = False
        stream_thermal_capacity_max_power,orc_type,orc_electrical_generation,intermediate_turnkey_max_power,intermediate_om_fix_max_power,intermediate_om_var_max_power = convert_aux(stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,power_fraction,intermediate_fluid, country,consumer_type,aggregate_streams)
        info_individual = {'orc_type':orc_type, 'stream_thermal_capacity_max_power':stream_thermal_capacity_max_power, 'orc_electrical_generation':orc_electrical_generation, 'intermediate_turnkey_max_power':intermediate_turnkey_max_power, 'intermediate_om_fix_max_power': intermediate_om_fix_max_power, 'intermediate_om_var_max_power': intermediate_om_var_max_power}

        # Aggregated
        aggregate_streams = True
        stream_thermal_capacity_max_power,orc_type,orc_electrical_generation,intermediate_turnkey_max_power,intermediate_om_fix_max_power,intermediate_om_var_max_power = convert_aux(stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,power_fraction,intermediate_fluid, country,consumer_type,aggregate_streams)
        info_aggregate = {'orc_type':orc_type, 'stream_thermal_capacity_max_power':stream_thermal_capacity_max_power, 'orc_electrical_generation':orc_electrical_generation, 'intermediate_turnkey_max_power':intermediate_turnkey_max_power, 'intermediate_om_fix_max_power': intermediate_om_fix_max_power, 'intermediate_om_var_max_power': intermediate_om_var_max_power}

        streams_info[str(stream_index)] = {'info_individual':info_individual,'info_aggregate': info_aggregate}

    # convert streams - all combinations possible
    for combination in combinations:
        electrical_generation_yearly = 0
        electrical_generation_nominal_total = 0
        om_fix_intermediate = 0
        turnkey_intermediate = 0
        om_var_intermediate = 0
        electrical_generation_nominal = 0
        stream_thermal_capacity_total = 0
        combo = []
        combination_streams_id = []

        for stream_index in combination:

            if len(combination) > 1:  # aggregated
                electrical_generation_nominal = streams_info[str(stream_index)]['info_aggregate']['orc_electrical_generation']
                stream_thermal_capacity_total += streams_info[str(stream_index)]['info_aggregate']['stream_thermal_capacity_max_power']
                om_fix_intermediate += streams_info[str(stream_index)]['info_aggregate']['intermediate_om_fix_max_power']
                turnkey_intermediate += streams_info[str(stream_index)]['info_aggregate']['intermediate_turnkey_max_power']
                om_var_intermediate += streams_info[str(stream_index)]['info_aggregate']['intermediate_om_var_max_power']
                combo.append(streams[stream_index]['id'])

            else:  # not aggregated
                electrical_generation_nominal = streams_info[str(stream_index)]['info_individual']['orc_electrical_generation']
                stream_thermal_capacity_total += streams_info[str(stream_index)]['info_individual']['stream_thermal_capacity_max_power']
                om_fix_intermediate = streams_info[str(stream_index)]['info_individual']['intermediate_om_fix_max_power']
                turnkey_intermediate = streams_info[str(stream_index)]['info_individual']['intermediate_turnkey_max_power']
                om_var_intermediate = streams_info[str(stream_index)]['info_individual']['intermediate_om_var_max_power']

            electrical_generation_nominal_total += electrical_generation_nominal
            electrical_generation_yearly += electrical_generation_nominal * sum(streams[stream_index]['schedule'])

        if len(combination) > 1:
            combination_streams_id.append(combo)
            global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details('orc',electrical_generation_nominal_total)

        else:
            combination_streams_id.append([streams[stream_index]['id']])
            global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details(streams_info[str(stream_index)]['info_individual']['orc_type'],electrical_generation_nominal_total)

        # total costs
        om_var_total = om_var_intermediate
        om_fix_total = om_fix_orc + om_fix_intermediate
        total_turnkey = turnkey_orc + turnkey_intermediate

        # all convert options
        convert_info.append({
            'streams': combination_streams_id[0],
            'electrical_generation_nominal': electrical_generation_nominal_total,  # [kW]
            'electrical_generation_yearly':electrical_generation_yearly,  # [kWh]
            'excess_heat_supply_capacity': stream_thermal_capacity_total,  # [kW]
            'conversion_efficiency': electrical_generation_nominal / stream_thermal_capacity_total,  # [%]
            'turnkey': total_turnkey,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total , # [€/h]
            'electrical_generation_yearly_turnkey':electrical_generation_yearly/total_turnkey
            })

    new_df = pd.DataFrame()
    for dict in convert_info:
        new_df = new_df.append(dict,ignore_index=True)

    # get best
    electricity_generation_max = new_df.sort_values('electrical_generation_yearly', ascending=False).head(n=get_best_number).to_dict(orient='records')
    electricity_generation_investment = new_df.sort_values('electrical_generation_yearly_turnkey', ascending=False).head(n=get_best_number).to_dict(orient='records')

    output = {
            'electricity_generation_max': electricity_generation_max,
            'electricity_generation_investment': electricity_generation_investment
        }

    return output




class Source_simplified():
    def __init__(self):
        # Input
        # Input
        self.object_id = 5
        self.type_of_object = 'source'
        self.streams = [{'supply_temperature':300,'target_temperature':500,'fluid':'flue_gas','fluid_cp':1.3,'flowrate':16864,'saturday_on':1
                         ,'sunday_on':1,'shutdown_periods':[],'daily_periods':[[10,18]]},
                        {'supply_temperature': 2, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 1000, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 20]]},
                        {'supply_temperature': 200, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 234530, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 21]]},
                        {'supply_temperature': 450, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 4240, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 24]]},
                        {'supply_temperature': 500, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 5035340, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 228550, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 800, 'target_temperature': 100, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 1224240, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 14]]},
                        {'supply_temperature': 900, 'target_temperature': 365, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 32540, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 15]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 224230, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 3245, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 11]]}]


source = Source_simplified()
industry_stream_test = simple_user(source)

industry_stream_test[0]['id'] = 1
industry_stream_test[1]['id'] = 2
industry_stream_test[2]['id'] = 3
industry_stream_test[3]['id'] = 4
industry_stream_test[4]['id'] = 5
industry_stream_test[5]['id'] = 6
industry_stream_test[6]['id'] = 7
industry_stream_test[7]['id'] = 8
industry_stream_test[8]['id'] = 9
industry_stream_test[9]['id'] = 10

class INVAR:
    def __init__(self,streams):

        self.streams = streams
        self.consumer_type = 'non_household'
        self.country = 'Portugal'

in_var = INVAR(industry_stream_test)

a = convert_orc(in_var)

for out in a.keys():
    print('NEWWWWWWWWWWWWWWWWW')
    for i in a[out]:
        print(i)
        plt.bar(str(i['streams']),i['electrical_generation_yearly'])

    plt.xlabel('Streams Index')
    plt.ylabel(out)
    plt.xticks(rotation=90)
    plt.show()

