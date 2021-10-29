"""
##############################
INFO: Convert_Options Raw Data to ORC/RC, for maximum electrical generation.

##############################
INPUT:

##############################
OUTPUT:


"""

from Source.simulation.Heat_Recovery.ORC.Auxiliary.convert_aux import convert_aux
import itertools
from KB_General.equipment_details import equipment_details
import pandas as pd
from General.Simple_User.simple_user import simple_user

def convert_orc(in_var):

    # INPUT
    streams = in_var.streams
    consumer_type = in_var.consumer_type
    country = in_var.country

    # Initialize Arrays
    output = []
    convert_info = []

    # Defined vars
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

    # Generate Electricity Available Profile
    streams_able = []
    streams_able_index = []
    stream_power = []
    i=0
    for stream in streams:
        if stream['target_temperature'] > (hx_orc_return_temperature):
            if stream['supply_temperature'] > (hx_orc_supply_temperature):
                stream_power.append(sum(stream['hourly_generation']))

        i += 1

    streams_able_index_tuple = sorted(((value, index) for index, value in enumerate(stream_power)), reverse=True)
    streams_able_index = [index[1] for index in streams_able_index_tuple[0:5]]
    print(streams_able_index)
    combinations = []

    for L in range(0, len(streams_able_index) + 1):
        for subset in itertools.combinations(streams_able_index, L):
            if list(subset) != []:
                combinations.append(list(subset))



        combination_streams_id = []

    streams_info = []
    for stream_index in streams_able_index:
        stream = streams[stream_index]

        # Individual Stream
        aggregate_streams = False
        stream_thermal_capacity_max_power,orc_type,orc_electrical_generation,intermediate_turnkey_max_power,intermediate_om_fix_max_power,intermediate_om_var_max_power = convert_aux(stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,power_fraction,intermediate_fluid, country,consumer_type,aggregate_streams)
        info_individual = {'orc_type':orc_type, 'stream_thermal_capacity_max_power':stream_thermal_capacity_max_power, 'orc_electrical_generation':orc_electrical_generation}

        # Aggregate
        aggregate_streams = True
        stream_thermal_capacity_max_power,orc_type,orc_electrical_generation,intermediate_turnkey_max_power,intermediate_om_fix_max_power,intermediate_om_var_max_power = convert_aux(stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,power_fraction,intermediate_fluid, country,consumer_type,aggregate_streams)
        info_aggregate = {'orc_type':orc_type, 'stream_thermal_capacity_max_power':stream_thermal_capacity_max_power, 'orc_electrical_generation':orc_electrical_generation,}

        streams_info.append([info_individual,info_aggregate])

    ###################################################################
    ###################################################################

    # Test all combinations possible
    for combination in combinations:
        electrical_generation_yearly = 0
        electrical_generation_nominal_total = 0
        total_turnkey = 0
        electrical_generation_over_turnkey = 0
        electrical_generation_nominal = 0
        stream_thermal_capacity_total = 0
        combo = []
        combination_streams_id = []

        for stream_index in combination:

            if len(combination) > 1:
                electrical_generation_nominal = streams_info[stream_index][0]['orc_electrical_generation']
                stream_thermal_capacity_total += streams_info[stream_index][0]['stream_thermal_capacity_max_power']

                combo.append(streams[stream_index]['id'])
            else:
                electrical_generation_nominal = streams_info[stream_index][1]['orc_electrical_generation']
                stream_thermal_capacity_total += streams_info[stream_index][1]['stream_thermal_capacity_max_power']

            electrical_generation_nominal_total += electrical_generation_nominal
            electrical_generation_yearly += electrical_generation_nominal * sum(streams[stream_index]['schedule'])

        if len(combination) > 1:
            combination_streams_id.append(combo)
        else:
            combination_streams_id.append(streams[stream_index]['id'])

        if len(combination) > 1 == True:
            global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details('orc',electrical_generation_nominal_total)
        else:
            global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details(orc_type,electrical_generation_nominal_total)

    
        om_var_total = 1
        om_fix_total = 1
        total_turnkey = turnkey_orc

        ###################################################################
        ###################################################################
        ###################################################################


        convert_info.append({
            'streams': combination_streams_id,
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

    print(new_df)

    # get best 3
    electricity_generation_max = new_df.sort_values('electrical_generation_yearly', ascending=False).head(3).to_dict(orient='records')
    # get best 3
    electricity_generation_investment = new_df.sort_values('electrical_generation_yearly_turnkey').head(3).to_dict(orient='records')


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
        self.streams = [{'supply_temperature':900,'target_temperature':500,'fluid':'flue_gas','fluid_cp':1.3,'flowrate':16864,'saturday_on':1
                         ,'sunday_on':1,'shutdown_periods':[],'daily_periods':[[10,18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]},
                        {'supply_temperature': 900, 'target_temperature': 500, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[10, 18]]}]


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

