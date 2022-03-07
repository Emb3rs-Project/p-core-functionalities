"""
alisboa/jmcunha


##############################
INFO: Sinks conversion technologies.

      For the group of sinks given, it is set the grid supply and return temperatures. Moreover, grid specific technologies
      are designed to meet the heating/cooling requirements of the group.

      For each sink are designed the conversion technologies needed. The design may be done for each stream individually or
      it can be made to the aggregated of streams (the user must provide his preference).
      When performing the conversion, three design options may occur:

          Sink needs HEATING
            1) the grid temperature meets the sink target temperature requirements, thus only a grid-sink HX and correspondent
            circulation pumping is needed
            2) the grid temperature does not meet the sink target temperature requirements, thus adding to the grid-sink HX
            and correspondent circulation pumping, it is also necessary to add a technology to raise the temperature (chp,
            solar thermal, heat pump, boiler)

          Sink needs COOLING
            3) it is always necessary to add a cooling technology (thermal_chiller), since we are only designing DHNs


      Possible conversions: HX, HX + heating/cooling technology + HX


##############################
INPUT: group_of_sinks = [sink_1,sink_2,...] each sink with a dict

      Where, for example:
        # sink_1 {
        #       'id'
        #       'location' = [latitude,longitude]
        #       'consumer_type' - 'household' or 'non-household'
        #       'streams' - array with dictionaries with {id, object_type, stream_type, fluid, capacity, supply_temperature,target_temperature, hourly_generation}
        #    }

 

##############################
OUTPUT: the following dictionary,

         # all_sinks_info = {
         #              'sink_group_grid_supply_temperature' [ºC]
         #              'sink_group_grid_return_temperature' [ºC]
         #              'grid_specific' -  dictionary with 'heating' and 'cooling'
         #              'sinks' - dictionary
         #        }

             Where in grid_specific:
                # grid_specific = {
                #               'heating' - array with dictionaries of the technologies
                #               'cooling'
                #               }

                    In each technology dictionary:
                          #  {
                          #   'equipment',
                          #   'fuel_type',
                          #   'max_input_capacity'  [kW]
                          #   'turnkey_a' [€/kW]
                          #   'turnkey_b' [€]
                          #   'conversion_efficiency' []
                          #   'om_fix' [€/year.kW]
                          #   'om_var' [€/kWh]
                          #   'emissions' [kg.CO2/kWh]
                          #   },


            Where in sinks:
                # sinks = {
                #          'sink_id'
                #          'streams'
                #          }

                 Where in streams:
                 # streams = {
                 #          'stream_id'
                 #          'hourly_stream_capacity' [kWh]
                 #          'teo_demand_factor'
                 #          'teo_yearly_demand'
                 #          'conversion_technologies' - multiple dictionaries with technologies possible to implement
                 #          }

                  Where in conversion_technologies:
                     # conversion_technologies = {
                     #                              'equipment'
                     #                              'max_capacity'  [kW]
                     #                              'turnkey_a' [€/kW]
                     #                              'turnkey_b' [€]
                     #                              'conversion_efficiency'  []
                     #                              'om_fix'   [€/year.kW]
                     #                              'om_var'  [€/kWh]
                     #                              'emissions'  [kg.CO2/kWh]
                     #                              'tecnhologies' - technologies info in detail, - RIGHT NOW, NOT AN OUTPUT
                     #                            }


"""

from ....General.Convert_Equipments.Auxiliary.sink_get_hx_temperatures import sink_get_hx_temperatures
from ....General.Convert_Equipments.Convert_Options.add_boiler import Add_Boiler
from ....General.Convert_Equipments.Convert_Options.add_hx import Add_HX
from ....General.Convert_Equipments.Convert_Options.add_solar_thermal import Add_Solar_Thermal
from ....General.Convert_Equipments.Convert_Options.add_heat_pump import Add_Heat_Pump
from ....General.Convert_Equipments.Convert_Options.add_thermal_chiller import Add_Thermal_Chiller
from ....General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from ....General.Convert_Equipments.Auxiliary.join_hx_and_technology import join_hx_and_technology
from ....General.Convert_Equipments.Convert_Options.add_electric_chiller import Add_Electric_Chiller
from ....General.Auxiliary_General.get_country import get_country
from ....General.Convert_Equipments.Auxiliary.coef_solar_thermal_backup import coef_solar_thermal_backup
import numpy as np


def convert_sinks(in_var, kb):


    ##################################################################################################################
    # INPUT
    group_of_sinks = in_var['platform']['group_of_sinks']  # e.g. building, greenhouse, streams


    ##################################################################################################################
    # Initialize array
    output_sink = []
    vector_sink_max_target_temperature = []
    vector_sink_max_supply_temperature = []
    grid_specific_heating = []
    grid_specific_cooling = []
    boiler_fuel_type = ['natural_gas', 'fuel_oil', 'biomass']  # types of fuel
    fuels_teo_nomenclature = {'natural_gas': 'ng', 'fuel_oil': 'oil', 'biomass': 'biomass'}


    ##################################################################################################################
    # Defined vars
    ambient_temperature = 15
    minimum_coef_solar_thermal = 0.5  # solar thermal has to provide at least 50% of streams demand to be considered for TEO

    # Grid Characteristics
    grid_fluid = 'water'
    fix_grid_supply_temperature = 100
    fix_grid_return_temperature = 70
    hot_grid_delta_T = 30  # defined minimum grid delta_T  on sink side for oil and hot water

    # HX Characteristics
    hx_efficiency = 0.95
    hx_delta_T = 5

    # Convert_Options Characteristics
    power_fraction = 0.05  # Defined as 5%
    thermal_chiller_generator_T_cold = 70  # [ºC]
    thermal_chiller_generator_T_hot = 85  # [ºC]
    thermal_chiller_supply_temperature = 7  # [ºC]
    thermal_chiller_efficiency = 0.71  # COP
    boiler_efficiency = 0.95


    for sink_index,source in enumerate(group_of_sinks):
        for stream_index,stream in enumerate(source['streams']):
            hourly_stream_capacity = stream['hourly_generation']
            break
        break

    teo_group_of_sinks_demand_factor = [{}] * len(hourly_stream_capacity)


    ##################################################################################################################
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

    # create backup for sink group
    group_of_sinks_grid_specific_power_heating = 0
    group_of_sinks_grid_specific_power_cooling = 0
    group_latitude = 0
    group_longitude = 0
    group_of_sinks_grid_specific_minimum_supply_temperature = []
    needed_yearly_capacity = 0
    group_of_sinks_grid_specific_hourly_capacity = np.empty(len(group_of_sinks[0]['streams'][0]['hourly_generation']))

    for sink in group_of_sinks:
        latitude, longitude = sink['location']
        group_latitude += latitude
        group_longitude += longitude

        for stream in sink['streams']:
            if stream['target_temperature'] > stream['supply_temperature']:
                group_of_sinks_grid_specific_power_heating += stream['capacity']
                needed_yearly_capacity += sum(stream['hourly_generation'])  # [kWh]
                group_of_sinks_grid_specific_hourly_capacity += np.asarray(stream['hourly_generation'])
            else:
                group_of_sinks_grid_specific_power_cooling += stream['capacity']
                group_of_sinks_grid_specific_minimum_supply_temperature.append(stream['target_temperature'])

    group_latitude /= len(group_of_sinks)
    group_longitude /= len(group_of_sinks)
    country = get_country(group_latitude, group_longitude)

    try:
        # add boiler
        for fuel in boiler_fuel_type:
            info_technology_group = Add_Boiler(kb, fuel, country, 'non_household',
                                               group_of_sinks_grid_specific_power_heating, power_fraction,
                                               grid_supply_temperature, grid_return_temperature)

            teo_equipment_name = fuels_teo_nomenclature[info_technology_group.fuel_type] + '_boiler_sink'
            info = join_hx_and_technology('grid_specific', [info_technology_group], power_fraction,
                                          info_technology_group.data_teo['max_input_capacity'],
                                          group_of_sinks_grid_specific_power_heating, 'sink',
                                          teo_equipment_name, 'grid_specific')

            grid_specific_heating.append(info)

        # add heat pump
        info_technology_group_hp = Add_Heat_Pump(kb, country, 'non_household',
                                                 power_fraction, grid_supply_temperature, grid_return_temperature,
                                                 ambient_temperature,supply_capacity=group_of_sinks_grid_specific_power_heating)

        teo_equipment_name = 'hp_sink'
        info = join_hx_and_technology('grid_specific', [info_technology_group_hp], power_fraction,
                                      info_technology_group_hp.data_teo['max_input_capacity'],
                                      group_of_sinks_grid_specific_power_heating, 'sink',
                                      teo_equipment_name, 'grid_specific')
        grid_specific_heating.append(info)

        # add solar thermal + hp
        info_technology_group_solar_thermal = Add_Solar_Thermal(kb, country, 'non_household', group_latitude, group_longitude,
                                                                group_of_sinks_grid_specific_power_heating, power_fraction,
                                                                grid_supply_temperature, grid_return_temperature,hx_delta_T,hx_efficiency)

        teo_equipment_name = 'solar_thermal_' + 'hp_sink'
        info = join_hx_and_technology('grid_specific', [info_technology_group_solar_thermal,
                                                        info_technology_group_hp], power_fraction,
                                      group_of_sinks_grid_specific_power_heating,
                                      group_of_sinks_grid_specific_power_heating, 'sink',
                                      teo_equipment_name, 'grid_specific')  # overall conversion efficiency will be 1

        coef_solar_thermal, info = coef_solar_thermal_backup(group_of_sinks_grid_specific_hourly_capacity, info, info_technology_group_solar_thermal)
        if coef_solar_thermal >= minimum_coef_solar_thermal:
            grid_specific_heating.append(info)

    except:
        pass

    try:
        info_technology_group = Add_Electric_Chiller(kb, country, 'non_household',
                                                     group_of_sinks_grid_specific_power_cooling, power_fraction,
                                                     min(group_of_sinks_grid_specific_minimum_supply_temperature),
                                                     min(group_of_sinks_grid_specific_minimum_supply_temperature) + 5)
        grid_specific_cooling.append(info_technology_group.data_teo)
    except:
        pass

    # convert each stream
    for sink in group_of_sinks:
        output_converted = []
        latitude, longitude = sink['location']
        country = get_country(latitude, longitude)
        consumer_type = sink['consumer_type']

        # get conversion technologies for each stream
        for stream in sink['streams']:
            conversion_technologies = []
            hourly_stream_capacity = stream['hourly_generation']  # [kWh]

            # get stream nominal capacity
            stream_nominal_capacity = max(hourly_stream_capacity)  # [kW]

            # design/cost equipment
            if stream['stream_type'] == 'inflow':

                # get heating technologies
                if stream['target_temperature'] > stream['supply_temperature']:

                    # vapour is needed - only heat pump is designed
                    if stream['target_temperature'] > 100 - hx_delta_T:

                        # add heat pump: evaporator_temperature = grid return temperature - hx_delta_T
                        info_technology = Add_Heat_Pump(kb, country, consumer_type, power_fraction,
                                                        stream['target_temperature'], stream['supply_temperature'],
                                                        grid_return_temperature,supply_capacity=stream_nominal_capacity)

                        # add circulation pumping to grid
                        power_from_grid = info_technology.evap_capacity
                        info_pump_grid = Add_Pump(kb, country, consumer_type, grid_fluid, power_from_grid, power_fraction,
                                                  grid_supply_temperature, grid_return_temperature)

                        teo_equipment_name = 'hp_sink'

                        info = join_hx_and_technology(sink['id'],[info_pump_grid, info_technology], power_fraction,
                                                      info_pump_grid.supply_capacity, stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])
                        conversion_technologies.append(info)


                    else:
                        # add HX to grid
                        hx_grid_supply_temperature, hx_grid_return_temperature, hx_sink_supply_temperature, hx_sink_target_temperature = sink_get_hx_temperatures(
                            grid_supply_temperature, grid_return_temperature, stream['supply_temperature'],
                            stream['target_temperature'], hx_delta_T)

                        if hx_grid_supply_temperature == hx_grid_return_temperature:  # safety - occurs when -> grid_supply_temperature < stream_supply_temperature:
                            hx_power = 0
                            hx_power_supply = 0
                        else:
                            hx_power_supply = stream_nominal_capacity * abs(
                                hx_sink_target_temperature - hx_sink_supply_temperature) / (
                                                  abs(stream['target_temperature'] - stream['supply_temperature']))
                            hx_power = hx_power_supply / hx_efficiency

                        info_hx_grid = Add_HX(kb, hx_grid_supply_temperature, hx_grid_return_temperature, grid_fluid,
                                              hx_sink_target_temperature, hx_sink_supply_temperature, stream['fluid'],
                                              hx_power, power_fraction)

                        # add circulation pumping to grid
                        info_pump_grid = Add_Pump(kb, country, consumer_type, grid_fluid, hx_power, power_fraction,
                                                  hx_grid_supply_temperature, hx_grid_return_temperature)

                        # grid may not supply enough heat to the sink
                        needed_supply_capacity = stream_nominal_capacity - hx_power_supply  # [kW]

                        if stream['target_temperature'] == hx_sink_target_temperature:
                            teo_equipment_name = 'heat_exchanger_sink'

                            info = join_hx_and_technology(sink['id'],[info_hx_grid, info_pump_grid], power_fraction,
                                                          info_pump_grid.supply_capacity, stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])
                            conversion_technologies.append(info)

                        elif stream['target_temperature'] > hx_sink_target_temperature:

                            # add boiler
                            for fuel in boiler_fuel_type:
                                info_technology = Add_Boiler(kb, fuel, country, consumer_type, needed_supply_capacity,
                                                             power_fraction, stream['target_temperature'],
                                                             hx_sink_target_temperature)
                                teo_equipment_name = fuels_teo_nomenclature[info_technology.fuel_type] + '_boiler_sink'
                                info = join_hx_and_technology(sink['id'],[info_hx_grid, info_pump_grid, info_technology],
                                                              power_fraction, info_pump_grid.supply_capacity,
                                                              stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])
                                conversion_technologies.append(info)

                            # add solar thermal + boiler as backup
                            info_technology_solar_thermal = Add_Solar_Thermal(kb, country, consumer_type, latitude, longitude,needed_supply_capacity, power_fraction, stream['target_temperature'], hx_sink_target_temperature,hx_delta_T,hx_efficiency)
                            info_technology_boiler = Add_Boiler(kb, 'natural_gas', country, consumer_type, needed_supply_capacity, power_fraction, stream['target_temperature'],hx_sink_target_temperature)
                            teo_equipment_name = 'solar_thermal_' + fuels_teo_nomenclature[info_technology_boiler.fuel_type] + '_boiler_sink'

                            coef_solar_thermal, info_technology_boiler = coef_solar_thermal_backup(stream['hourly_generation'], info_technology_solar_thermal,info_technology_boiler)
                            info = join_hx_and_technology(sink['id'],[info_hx_grid, info_pump_grid, info_technology_solar_thermal,info_technology_boiler], power_fraction, info_pump_grid.supply_capacity, stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])

                            conversion_technologies.append(info)

                            # add solar thermal + heat pump as backup
                            info_technology_heat_pump = Add_Heat_Pump(kb, country, consumer_type, power_fraction,stream['target_temperature'], hx_sink_target_temperature,ambient_temperature,supply_capacity=needed_supply_capacity)
                            teo_equipment_name = 'solar_thermal_' + 'hp_sink'
                            coef_solar_thermal, info_technology_heat_pump = coef_solar_thermal_backup(stream['hourly_generation'], info_technology_solar_thermal,info_technology_heat_pump)
                            info = join_hx_and_technology(sink['id'],[info_hx_grid, info_pump_grid, info_technology_solar_thermal,info_technology_heat_pump], power_fraction, info_pump_grid.supply_capacity, stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])

                            if coef_solar_thermal >= minimum_coef_solar_thermal:
                                info['hourly_supply_capacity_normalize'] = info_technology_solar_thermal.data_teo['hourly_supply_capacity_normalize']  # add solar thermal profile
                                conversion_technologies.append(info)


                            # add heat pump
                            info_technology = Add_Heat_Pump(kb, country, consumer_type, power_fraction,
                                                            hx_sink_target_temperature, hx_sink_supply_temperature,
                                                        grid_return_temperature,supply_capacity=stream_nominal_capacity)
                            teo_equipment_name = 'hp_sink'

                            # heat pump circulation pumping to grid
                            info_pump_grid = Add_Pump(kb, country, consumer_type, grid_fluid, info_technology.evap_capacity,
                                                      power_fraction,hx_grid_supply_temperature, hx_grid_return_temperature)

                            info = join_hx_and_technology(sink['id'],[info_hx_grid, info_pump_grid, info_technology], power_fraction,
                                                          info_pump_grid.supply_capacity, stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])
                            conversion_technologies.append(info)


                # get cooling technologies
                else:

                    if grid_supply_temperature < thermal_chiller_generator_T_hot:
                        after_hx_global_conversion_efficiency = boiler_efficiency * thermal_chiller_efficiency
                    else:
                        after_hx_global_conversion_efficiency = thermal_chiller_efficiency

                    # add electric chiller - stream target temperature inferior to absorption chiller supply temperature
                    if stream['target_temperature'] < thermal_chiller_supply_temperature:
                        electric_chiller_supply_capacity = stream_nominal_capacity * (
                                    thermal_chiller_supply_temperature - stream['target_temperature']) / (
                                                                       stream['supply_temperature'] - stream[
                                                                   'target_temperature'])
                        thermal_chiller_supply_capacity = stream_nominal_capacity - electric_chiller_supply_capacity
                        info_electric_chiller = Add_Electric_Chiller(kb, country, consumer_type, electric_chiller_supply_capacity,
                                                                     power_fraction,
                                                                     stream['target_temperature'],
                                                                     thermal_chiller_supply_temperature, )
                    else:
                        thermal_chiller_supply_capacity = stream_nominal_capacity
                        info_electric_chiller = []

                    # add HX to grid
                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_sink_supply_temperature, hx_sink_target_temperature = sink_get_hx_temperatures(
                        grid_supply_temperature, grid_return_temperature, thermal_chiller_generator_T_cold,
                        thermal_chiller_generator_T_hot, hx_delta_T)

                    if hx_grid_supply_temperature == hx_grid_return_temperature:
                        hx_power_supply = 0
                        hx_power = 0
                    else:
                        hx_power_supply = thermal_chiller_supply_capacity / (
                            abs(thermal_chiller_generator_T_hot - thermal_chiller_generator_T_cold)) * abs(
                            hx_grid_supply_temperature - hx_grid_return_temperature)
                        hx_power = hx_power_supply / hx_efficiency

                    info_hx_grid = Add_HX(kb, hx_grid_supply_temperature, hx_grid_return_temperature, grid_fluid,
                                          hx_sink_target_temperature, hx_sink_supply_temperature, stream['fluid'],
                                          hx_power, power_fraction)

                    # add circulation pumping to grid
                    info_pump_grid = Add_Pump(kb, country, consumer_type, grid_fluid, hx_power_supply, power_fraction,
                                              hx_sink_target_temperature, hx_sink_supply_temperature)

                    # grid may not supply enough heat to the sink
                    needed_supply_capacity = stream_nominal_capacity / after_hx_global_conversion_efficiency - hx_power_supply  # [kW]

                    # add absorption chiller
                    info_technology = Add_Thermal_Chiller(kb, country, consumer_type, thermal_chiller_supply_capacity,
                                                          power_fraction)

                    # absorption chiller evaporation temperature not reached
                    if hx_sink_target_temperature < thermal_chiller_generator_T_hot:
                        # add boiler
                        for fuel in boiler_fuel_type:
                            info_boiler = Add_Boiler(kb, fuel, country, consumer_type, needed_supply_capacity,
                                                     power_fraction, thermal_chiller_generator_T_hot,
                                                     hx_sink_target_temperature)

                            if info_electric_chiller == []:
                                teo_equipment_name = 'absorption_chiller_' + fuels_teo_nomenclature[info_boiler.fuel_type] + '_boiler_sink'
                                info = join_hx_and_technology(sink['id'],[info_hx_grid, info_pump_grid, info_boiler, info_technology],
                                                              power_fraction, info_pump_grid.supply_capacity,
                                                              stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])
                            else:
                                teo_equipment_name = 'absorption_chiller_with_electric_chiller_' + fuels_teo_nomenclature[info_boiler.fuel_type] + '_boiler_sink'
                                info = join_hx_and_technology(sink['id'],
                                    [info_hx_grid, info_pump_grid, info_boiler, info_technology,info_electric_chiller],
                                    power_fraction, info_pump_grid.supply_capacity,
                                    stream_nominal_capacity, 'sink', teo_equipment_name, stream['id'])

                            conversion_technologies.append(info)

                        # add heat pump
                        info_heat_pump = Add_Heat_Pump(kb, country, consumer_type, needed_supply_capacity, power_fraction,
                                                       thermal_chiller_generator_T_hot, hx_sink_target_temperature,
                                                       ambient_temperature)
                        if info_electric_chiller == []:
                            teo_equipment_name = 'absorption_chiller_' + 'hp_sink'
                            info = join_hx_and_technology(sink['id'],[info_hx_grid, info_pump_grid, info_heat_pump, info_technology],
                                                      power_fraction, info_pump_grid.supply_capacity,
                                                      stream_nominal_capacity, 'sink', teo_equipment_name, stream['id'])
                        else:
                            teo_equipment_name = 'absorption_chiller_with_electric_chiller_' + 'hp_sink'
                            info = join_hx_and_technology(sink['id'],
                                [info_hx_grid, info_pump_grid, info_heat_pump, info_technology,info_electric_chiller],
                                power_fraction, info_pump_grid.supply_capacity,
                                stream_nominal_capacity, 'sink', teo_equipment_name, stream['id'])

                        conversion_technologies.append(info)

                    else:
                        if info_electric_chiller == []:
                            teo_equipment_name = 'absorption_chiller_sink'

                            info = join_hx_and_technology(sink['id'],[info_hx_grid, info_pump_grid, info_technology],
                                                          power_fraction, info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])
                        else:
                            teo_equipment_name = 'absorption_chiller_with_electric_chiller_sink'
                            info = join_hx_and_technology(sink['id'],
                                [info_hx_grid, info_pump_grid, info_electric_chiller, info_technology], power_fraction,
                                info_pump_grid.supply_capacity, stream_nominal_capacity, 'sink',teo_equipment_name, stream['id'])

                        conversion_technologies.append(info)

            yearly_demand = sum(hourly_stream_capacity)
            teo_demand_factor = [i/yearly_demand for i in hourly_stream_capacity]

            gis_capacity = conversion_technologies[0]['max_capacity']

            output_converted.append({
                'stream_id': stream['id'],
                'demand_fuel': str(sink['id']) + '_' + str(stream['id']) + '_' + 'demand',
                'gis_capacity': gis_capacity,  # [kW]
                'hourly_stream_capacity': hourly_stream_capacity,  # [kWh]
                'teo_demand_factor': teo_demand_factor,
                'teo_yearly_demand': yearly_demand,
                'conversion_technologies': conversion_technologies,  # [€/kW]
            })

            for index, i in enumerate(teo_group_of_sinks_demand_factor):
                teo_id = 'sink' + str(sink['id']) + 'stream' + str(stream['id'])
                i[teo_id] = teo_demand_factor[index]




        output_sink.append({
            'sink_id': sink['id'],
            'location': [latitude, longitude],
            'streams': output_converted
        })

    all_sinks_info = {
        'sink_group_grid_supply_temperature': grid_supply_temperature,
        'sink_group_grid_return_temperature': grid_return_temperature,
        'grid_specific': {'heating': grid_specific_heating, 'cooling': grid_specific_cooling},
        'sinks': output_sink
    }

    n_demand_list = []
    for sink in all_sinks_info['sinks']:
        for stream in sink['streams']:
            gis_dict = {
                'id': sink['sink_id'],
                'stream_id': stream['stream_id'],
                'coords': sink['location'],
                'cap': stream['gis_capacity']  # [kW]
            }
            n_demand_list.append(gis_dict)

    all_info = {
        'all_sinks_info': all_sinks_info,
        'n_demand_list': n_demand_list,
        "teo_demand_factor": teo_group_of_sinks_demand_factor

    }


    return all_info
