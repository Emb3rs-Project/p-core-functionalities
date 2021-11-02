"""
##############################
INFO: GET SINK CONVERTION TECHNOLOGIES TO SEND TEO

##############################
INPUT: group_of_sinks = [sink_1,sink_2,...] each sink with dictionary {sink_id,sink_location,streams}
      Where:
         # id
         # location = [country,latitude,longitude]
         # consumer_type - 'household' or 'non-household'
         # streams -> array with dictionaries with {id, object_type, stream_type, fluid, capacity, supply_temperature, target_temperature,hourly_generation}

     Important:
         # hourly_generation for streams (profile 1 and 0), hourly_generation for building  (kWh profile)

##############################
OUTPUT: vector with multiple dictionaries {'sink_id', 'stream_id', 'hourly_stream_capacity', 'conversion_technologies'}
      Where:
         # sink_group_grid_supply_temperature [ºC]
         # sink_group_grid_return_temperature [ºC]
         # grid_specific -  dictionary with 'heating' and 'cooling'
         # sinks - dictionary

         Where in grid_specific:
            # heating - vector with dictionaries of the technologies
            # cooling
                In each technology dictionary:
                      #  {
                      #         'equipment',
                      #         'fuel_type',
                      #         'max_input_capacity'  [kW]
                      #         'turnkey_a' [€/kW]
                      #         'turnkey_b' [€]
                      #         'conversion_efficiency' []
                      #         'om_fix' [€/year.kW]
                      #         'om_var' [€/kWh]
                      #         'emissions' [kg.CO2/kWh]
                      #         },


        Where in sinks:
         # sink_id
         # streams

             Where in streams:
             # stream_id
             # hourly_stream_capacity [kWh]
             # conversion_technologies - multiple dictionaries with technologies possible to implement

              Where in conversion_technologies:
                 # conversion_technologies = {
                 #         'equipment'
                 #         'max_capacity'  [kW]
                 #         'turnkey_a' [€/kW]
                 #         'turnkey_b' [€]
                 #         'conversion_efficiency'  []
                 #         'om_fix'   [€/year.kW]
                 #         'om_var'  [€/kWh]
                 #         'emissions'  [kg.CO2/kWh]
                 #         'tecnhologies' - technologies info in detail,
                 #     }


"""

from General.Convert_Equipments.Auxiliary.sink_get_hx_temperatures import sink_get_hx_temperatures
from General.Convert_Equipments.Convert_Options.add_boiler import Add_Boiler
from General.Convert_Equipments.Convert_Options.add_hx import Add_HX
from General.Convert_Equipments.Convert_Options.add_solar_thermal import Add_Solar_Thermal
from General.Convert_Equipments.Convert_Options.add_heat_pump import Add_Heat_Pump
from General.Convert_Equipments.Convert_Options.add_chp import Add_CHP
from General.Convert_Equipments.Convert_Options.add_absorption_chiller import Add_Absorption_Chiller
from General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from General.Convert_Equipments.Auxiliary.join_hx_and_technology import join_hx_and_technology
from General.Convert_Equipments.Convert_Options.add_electric_chiller import Add_Electric_Chiller
import json
from General.Auxiliary_General.get_country import get_country



def convert_sinks(in_var):

    # INPUT -------
    group_of_sinks = in_var.group_of_sinks  # e.g. building, greenhouse, stream inflow

    # Initialize array
    output = []
    output_sink = []
    conversion_technologies = []
    vector_sink_max_target_temperature = []
    vector_sink_max_supply_temperature = []
    output_converted = []
    grid_specific_heating = []
    grid_specific_cooling = []
    boiler_fuel_type =['electricity','natural_gas','fuel_oil','biomass']  # types of fuel
    chp_fuel_type = ['natural_gas','fuel_oil','biomass']

    # Defined vars -----------------------
    # Grid Characteristics
    grid_fluid = 'water'
    fix_grid_supply_temperature = 85
    fix_grid_return_temperature = 55
    hot_grid_delta_T = 30  # defined minimum grid delta_T  on sink side for oil and hot water

    # HX Characteristics
    hx_efficiency = 0.95
    hx_delta_T = 5

    # Convert_Options Characteristics
    power_fraction = 0.05  # Defined as 5%
    thermal_chiller_evap_T_cold = 70  # [ºC]
    thermal_chiller_evap_T_hot = 90  # [ºC]
    thermal_chiller_supply_temperature = 7  # [ºC]
    thermal_chiller_efficiency = 0.71  # COP
    boiler_efficiency = 0.95


    for sink in group_of_sinks:
        # get grid temperature according to max sink target temperature
        for stream in sink['streams']:
            if stream['stream_type'] == 'inflow':
                vector_sink_max_target_temperature.append(stream['target_temperature'])
                vector_sink_max_supply_temperature.append(stream['supply_temperature'])

            grid_supply_temperature = max(vector_sink_max_target_temperature) + hx_delta_T
            grid_return_temperature = max(vector_sink_max_supply_temperature) + hx_delta_T

            # check if grid delta_T is respected
            delta_T = hot_grid_delta_T
            if grid_supply_temperature - grid_return_temperature < delta_T:
                grid_supply_temperature = grid_return_temperature + delta_T


        ###################################################################################################
        ###################################################################################################
        # FIXED TEMPERATURES - IF NOT DESIRED, IT MUST BE DELETED
        grid_supply_temperature = fix_grid_supply_temperature
        grid_return_temperature = fix_grid_return_temperature
        ###################################################################################################
        ###################################################################################################


    ###################################################################################################
    # create backup for sink group
    # for sink in group_of_sinks:
    group_of_sinks_grid_specific_power_heating = 0
    group_of_sinks_grid_specific_power_cooling = 0
    group_latitude = 0
    group_longitude = 0
    group_of_sinks_grid_specific_minimum_supply_temperature = []

    for sink in group_of_sinks:
        latitude, longitude = sink['location']
        group_latitude += latitude
        group_longitude += longitude

        for stream in sink['streams']:
            if stream['target_temperature'] > stream['supply_temperature']:
                group_of_sinks_grid_specific_power_heating += stream['capacity']
                group_of_sinks_grid_yearly_specific_power_heating = stream['hourly_generation']
            else:
                group_of_sinks_grid_specific_power_cooling += stream['capacity']
                group_of_sinks_grid_specific_minimum_supply_temperature.append(stream['target_temperature'])

    group_latitude /= len(group_of_sinks)
    group_longitude /= len(group_of_sinks)
    country = get_country(group_latitude, group_longitude)

    try:
        # add boiler
        for fuel in boiler_fuel_type:
            info_technology_group = Add_Boiler(fuel, country, 'non_household', group_of_sinks_grid_specific_power_heating, power_fraction,grid_supply_temperature, grid_return_temperature)
            grid_specific_heating.append(info_technology_group.data_teo)

        # add solar thermal
        info_technology_group = Add_Solar_Thermal(country,'non_household',group_latitude, group_longitude, group_of_sinks_grid_yearly_specific_power_heating, power_fraction, grid_supply_temperature, grid_return_temperature)
        grid_specific_heating.append(info_technology_group.data_teo)

        # add heat pump
        info_technology_group = Add_Heat_Pump(country, 'non_household', group_of_sinks_grid_specific_power_heating, power_fraction,grid_supply_temperature, grid_return_temperature)
        grid_specific_heating.append(info_technology_group.data_teo)
    except:
        pass

    try:
        info_technology_group = Add_Electric_Chiller(country, 'non_household',group_of_sinks_grid_specific_power_cooling, power_fraction,min(group_of_sinks_grid_specific_minimum_supply_temperature),min(group_of_sinks_grid_specific_minimum_supply_temperature)+5)
        grid_specific_cooling.append(info_technology_group.data_teo)
    except:
        pass


    ###################################################################################################


    # convert each stream
    for sink in group_of_sinks:

        latitude, longitude = sink['location']
        country = get_country(latitude, longitude)
        consumer_type = sink['consumer_type']

        # get conversion technologies for each stream
        for stream in sink['streams']:
            hourly_stream_capacity = stream['hourly_generation']  # [kWh]

            # get stream nominal capacity
            stream_nominal_capacity = max(hourly_stream_capacity)  # [kW]

            # design/cost equipment
            if stream['stream_type'] == 'inflow':

                # get heating technologies
                if stream['target_temperature'] > stream['supply_temperature']:

                    # add HX to grid
                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_sink_supply_temperature, hx_sink_target_temperature = sink_get_hx_temperatures(grid_supply_temperature, grid_return_temperature, stream['supply_temperature'],stream['target_temperature'],hx_delta_T)

                    if hx_grid_supply_temperature == hx_grid_return_temperature:  # safety - occurs when -> grid_supply_temperature < stream_supply_temperature:
                        hx_power = 0
                        hx_power_supply = 0
                    else:
                        hx_power_supply = stream_nominal_capacity * abs(hx_sink_target_temperature - hx_sink_supply_temperature) / (abs(stream['target_temperature'] - stream['supply_temperature']))
                        hx_power = hx_power_supply/hx_efficiency

                    info_hx_grid = Add_HX(hx_grid_supply_temperature, hx_grid_return_temperature, grid_fluid,hx_sink_target_temperature, hx_sink_supply_temperature, stream['fluid'], hx_power,power_fraction)

                    # add circulation pumping to grid
                    info_pump_grid = Add_Pump(country, consumer_type, grid_fluid, hx_power, power_fraction, hx_grid_supply_temperature, hx_grid_return_temperature)

                    # grid may not supply enough heat to the sink
                    needed_supply_capacity = stream_nominal_capacity - hx_power_supply  # [kW]
                    needed_yearly_capacity = sum([i - hx_power_supply for i in hourly_stream_capacity])  # [kWh]


                    if stream['target_temperature'] == hx_sink_target_temperature:
                        info = join_hx_and_technology([info_pump_grid,info_hx_grid],power_fraction,info_pump_grid.supply_capacity,stream_nominal_capacity,'sink')
                        conversion_technologies.append(info)

                    elif stream['target_temperature'] > hx_sink_target_temperature:

                        # add boiler
                        for fuel in boiler_fuel_type:
                            info_technology = Add_Boiler(fuel, country, consumer_type, needed_supply_capacity, power_fraction, stream['target_temperature'],hx_sink_target_temperature)
                            info = join_hx_and_technology([info_pump_grid,info_hx_grid,info_technology],power_fraction,info_pump_grid.supply_capacity,stream_nominal_capacity,'sink')
                            conversion_technologies.append(info)

                        # add solar thermal
                        info_technology = Add_Solar_Thermal(country, consumer_type, latitude, longitude, needed_yearly_capacity, power_fraction,stream['target_temperature'], hx_sink_target_temperature)
                        info = join_hx_and_technology([info_pump_grid,info_hx_grid,info_technology],power_fraction,info_pump_grid.supply_capacity,stream_nominal_capacity,'sink')
                        info['hourly_supply_capacity_normalize'] = info_technology['hourly_supply_capacity_normalize']  # add solar thermal profile
                        conversion_technologies.append(info)

                        # add heat pump
                        info_technology = Add_Heat_Pump(country, consumer_type, needed_supply_capacity, power_fraction, stream['target_temperature'],hx_sink_target_temperature)
                        info = join_hx_and_technology([info_pump_grid,info_hx_grid,info_technology],power_fraction,info_pump_grid.supply_capacity,stream_nominal_capacity,'sink')
                        conversion_technologies.append(info)

                        # add chp
                        for fuel in chp_fuel_type:
                            info_technology = Add_CHP(fuel, country, consumer_type, needed_supply_capacity, power_fraction, stream['target_temperature'], hx_sink_target_temperature)
                            info = join_hx_and_technology([info_pump_grid,info_hx_grid,info_technology],power_fraction,info_pump_grid.supply_capacity,stream_nominal_capacity,'sink')
                            conversion_technologies.append(info)


                # get cooling technologies
                else:
                    if grid_supply_temperature < thermal_chiller_evap_T_hot:
                        after_hx_global_conversion_efficiency = boiler_efficiency * thermal_chiller_efficiency
                    else:
                        after_hx_global_conversion_efficiency = thermal_chiller_efficiency

                    # add electric chiller - stream target temperature inferior to absorption chiller supply temperature
                    if stream['target_temperature'] < thermal_chiller_supply_temperature:
                        electric_chiller_supply_capacity = stream_nominal_capacity * (thermal_chiller_supply_temperature - stream['target_temperature'])/(stream['supply_temperature'] - stream['target_temperature'])
                        thermal_chiller_supply_capacity = stream_nominal_capacity - electric_chiller_supply_capacity
                        info_electric_chiller = Add_Electric_Chiller(electric_chiller_supply_capacity, power_fraction, stream['target_temperature'],thermal_chiller_supply_temperature)
                    else:
                        electric_chiller_supply_capacity = 0
                        thermal_chiller_supply_capacity = stream_nominal_capacity
                        info_electric_chiller = []

                    # add HX to grid
                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_sink_supply_temperature, hx_sink_target_temperature = sink_get_hx_temperatures(grid_supply_temperature, grid_return_temperature, thermal_chiller_evap_T_cold,thermal_chiller_evap_T_hot, hx_delta_T)

                    if hx_grid_supply_temperature == hx_grid_return_temperature:
                        hx_power_supply = 0
                        hx_power = 0
                    else:
                        hx_power_supply = thermal_chiller_supply_capacity / (abs(thermal_chiller_evap_T_hot - thermal_chiller_evap_T_cold)) * abs(hx_grid_supply_temperature - hx_grid_return_temperature)
                        hx_power = hx_power_supply / hx_efficiency

                    info_hx_grid = Add_HX(hx_grid_supply_temperature, hx_grid_return_temperature, grid_fluid,hx_sink_target_temperature, hx_sink_supply_temperature, stream['fluid'], hx_power,power_fraction)

                    # add circulation pumping to grid
                    info_pump_grid = Add_Pump(country, consumer_type, grid_fluid, hx_power, power_fraction, hx_grid_supply_temperature,hx_grid_return_temperature)

                    # grid may not supply enough heat to the sink
                    needed_supply_capacity = stream_nominal_capacity/after_hx_global_conversion_efficiency - hx_power_supply  # [kW]

                    # add absorption chiller
                    info_technology = Add_Absorption_Chiller(country, consumer_type, thermal_chiller_supply_capacity, power_fraction)

                    # absorption chiller evaporation temperature not reached
                    if hx_sink_target_temperature < thermal_chiller_evap_T_hot:
                        # add boiler
                        for fuel in boiler_fuel_type:
                            info_boiler = Add_Boiler(fuel,country, consumer_type, needed_supply_capacity, power_fraction, thermal_chiller_evap_T_hot,hx_sink_target_temperature)
                            info = join_hx_and_technology([info_pump_grid, info_hx_grid, info_boiler,info_technology], power_fraction, info_pump_grid.supply_capacity,stream_nominal_capacity, 'sink')
                            conversion_technologies.append(info)

                        # add heat pump
                        info_heat_pump = Add_Heat_Pump(country, consumer_type, needed_supply_capacity, power_fraction,thermal_chiller_evap_T_hot, hx_sink_target_temperature)
                        info = join_hx_and_technology([info_pump_grid, info_hx_grid, info_heat_pump,info_technology], power_fraction, info_pump_grid.supply_capacity,stream_nominal_capacity, 'sink')
                        conversion_technologies.append(info)

                    else:
                        if info_electric_chiller == []:
                            info = join_hx_and_technology([info_pump_grid,info_hx_grid,  info_technology], power_fraction,info_pump_grid.supply_capacity,stream_nominal_capacity,'sink')
                        else:
                            info = join_hx_and_technology([info_pump_grid,info_hx_grid,info_electric_chiller,  info_technology], power_fraction,info_pump_grid.supply_capacity,stream_nominal_capacity,'sink')

                    conversion_technologies.append(info)

            output_converted.append({
                     'stream_id': stream['id'],
                     'hourly_stream_capacity': hourly_stream_capacity,  # [kWh]
                     'conversion_technologies': conversion_technologies,  # [€/kW]
                    })

        output_sink.append({
            'sink_id': sink['id'],
            'streams': output_converted
            })

    output.append({
        'sink_group_grid_supply_temperature': grid_supply_temperature,
        'sink_group_grid_return_temperature': grid_return_temperature,
        'grid_specific': {'heating':grid_specific_heating,'cooling':grid_specific_cooling},
        'sinks': output_sink
        })



    output = json.dumps(output, indent=2)

    return output



class VAR():
    def __init__(self):
        self.a = 1

invar = VAR()

stream_1 = {'id':2,
            'object_type':'stream',
            'stream_type':'inflow',
            'fluid':'water',
            'capacity':263,
            'supply_temperature': 10,
            'target_temperature':80,
            'hourly_generation':[1000,1000,1000]}


invar.group_of_sinks = [ {'id':1,
                        'consumer_type': 'non-household',
                        'location':[10,10],
                        'streams':[stream_1]
                                }]

out = convert_sinks(invar)
print(out)
