"""
alisboa/jmcunha


##############################
INFO: Sources conversion technologies.

      For each source are designed the conversion technologies needed. The design may be done for each stream individually or
      it can be made to the aggregated of streams (the user must provide his preference). After the designing, it is known
      the power available from each source.

      When performing the conversion, three design options may occur:
            1) when the stream is flue_gas or the supply temperature is larger than the defined safety_temperature=100ºC,
            it is always designed an intermediate oil circuit between stream and grid, for a more realistic approach
            (it is safer to implement intermediate circuit)
            2) when the source streams supply temperature are lower then the desired grid temperature, heating technologies
            are designed to reach its temperature

     Possible conversions: HX, ORC cascaded, HX + intermediate circuit + HX, heating technology + HX

     !!!!!
     IMPORTANT: it is expected that this script runs twice. The first time without knowing the grid losses and thus
     overestimating the source power available to be converted to the grid. The second time with estimated grid losses
     by the GIS, which will be used to give a better estimate of the real power available by the sources.


##############################
INPUT:  object with:

        # group_of_sources = [source_1,source_2,...] each source dictionary
        # last_iteration_data = [] or output from first iteration - all_sources_info
        # sink_group_grid_supply_temperature
        # sink_group_grid_return_temperature
        # grid_losses - array with vectors with grid losses for each stream of source  [[source_1_stream_1_loss, source_1_stream_2_loss],...]

            Where, for example:
             # source_1 = {
             #              'id'
             #              'location' = [latitude,longitude]
             #              'consumer_type' - 'household' or 'non-household'
             #              'streams' - array with dictionaries
             #             }

                     Where, for example:
                         # streams = {
                         #              'stream_id'
                         #              'object_type'
                         #              'stream_type'
                         #              'fluid'
                         #              'capacity'
                         #              'supply_temperature'
                         #              'target_temperature'
                         #              'hourly_generation'
                         #          }


##############################
OUTPUT: vector with multiple dictionaries [source_1,source_2,...]  [{'source_id', 'stream_id', 'hourly_stream_capacity', 'conversion_technologies'},..]

      Where, for example:
         # source_1 {
         #          'source_id',
         #          'source_grid_supply_temperature',
         #          'source_grid_return_temperature',
         #          'streams_converted',
         #          }

            Where in streams_converted:
                 # streams_converted = {
                 #          'stream_id'
                 #          'hourly_stream_capacity' [kWh]
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
                     #                              'tecnhologies' - technologies info in detail, - RIGHT NOW, NOT ON THE OUTPUT
                     #                            }


"""

from copy import copy
import json
from ....General.Convert_Equipments.Auxiliary.source_get_hx_temperatures import source_get_hx_temperatures
from ....General.Convert_Equipments.Convert_Options.add_boiler import Add_Boiler
from ....General.Convert_Equipments.Convert_Options.add_hx import Add_HX
from ....General.Convert_Equipments.Convert_Options.add_solar_thermal import Add_Solar_Thermal
from ....General.Convert_Equipments.Convert_Options.add_heat_pump import Add_Heat_Pump
from ....General.Convert_Equipments.Convert_Options.add_chp import Add_CHP
from ....General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from ....General.Convert_Equipments.Convert_Options.add_orc_cascaded import Add_ORC_Cascaded
from ....General.Convert_Equipments.Auxiliary.join_hx_and_technology import join_hx_and_technology
from ....Source.simulation.Auxiliary.design_orc import design_orc
from ....General.Auxiliary_General.get_country import get_country


def convert_sources(in_var):

    # INPUT
    group_of_sources = in_var.group_of_sources
    sink_group_grid_supply_temperature = in_var.sink_group_grid_supply_temperature
    sink_group_grid_return_temperature = in_var.sink_group_grid_return_temperature

    try:
        grid_losses = in_var.grid_losses  # vector with losses for each source
        last_iteration_data = in_var.last_iteration_data  # data output from this function from first iteration
    except:
        grid_losses = []
        last_iteration_data = []

    # Initialize array
    all_sources_info = []
    info_all_boilers = []

    conversion_technologies = []

    # Defined vars
    ambient_temperature = 15
    max_grid_temperature = 120  # defined maximum hot water grid temperature [ºC]
    safety_temperature = 100  # if heat stream above this temperature, use intermediate oil circuit [ºC]
    boiler_fuel_type =['electricity','natural_gas','fuel_oil','biomass']  # types of fuel
    chp_fuel_type = ['natural_gas','fuel_oil','biomass']

    # Grid Characteristics
    grid_fluid = 'water'
    grid_delta_T = sink_group_grid_supply_temperature - sink_group_grid_return_temperature
    intermediate_fluid = 'thermal_oil'

    # HX Characteristics
    hx_efficiency = 0.95
    hx_delta_T = 5

    # ORC Cascaded Characteristics
    orc_intermediate_fluid = 'water'
    orc_T_evap = 140  # defined var [ºC]
    orc_cond_supply_temperature = 90  # defined var [ºC]
    orc_cond_target_temperature = 60  # defined var [ºC]

    # Convert_Options Characteristics
    power_fraction = 0.05  # Defined as 5%


    for source_index,source in enumerate(group_of_sources):
        output_converted = []

        latitude, longitude = source['location']
        country = get_country(latitude, longitude)
        consumer_type = source['consumer_type']

        # get conversion technologies for each stream
        for stream_index,stream in enumerate(source['streams']):
            conversion_technologies = []

            # first iteration - grid losses not considered
            if grid_losses == []:
                power_last_iteration = 0
                delta_T_supply = 0
                delta_T_return = 0

            # second iteration - grid losses not considered
            else:
                # get source grid losses
                grid_losses_power = grid_losses[source_index][stream_index]

                # 1st step - Compute grid supply/return at source correction coefficients, considering average pipe supply/return temperatures as sink supply/return temperatures
                hot_pipe_delta_T = sink_group_grid_supply_temperature - ambient_temperature  # delta T, grid supply temperature pipe
                cold_pipe_delta_T = sink_group_grid_return_temperature - ambient_temperature  # delta T, grid return temperature pipe

                supply_coef = hot_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)  # correction coefficient
                return_coef = cold_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)

                # get source max power supplied on last iteration
                power_last_iteration = last_iteration_data[source_index]['streams_converted'][stream_index]['conversion_technologies'][0]['max_capacity'] * last_iteration_data[source_index]['streams_converted'][stream_index]['conversion_technologies'][0]['conversion_efficiency']
                #  TEO chooses power supplied by the stream?

                # 2nd step - Compute and converge temperatures of grid supply/return at source
                add_delta_T = (grid_delta_T) / (1 - grid_losses_power / power_last_iteration) - grid_delta_T
                delta_T_supply = add_delta_T * supply_coef
                delta_T_return = add_delta_T * return_coef

                converge = False
                while converge == False:
                    hot_pipe_T_average = ((sink_group_grid_supply_temperature + delta_T_supply) + sink_group_grid_supply_temperature) / 2
                    cold_pipe_T_average = ((sink_group_grid_return_temperature - delta_T_return) + sink_group_grid_return_temperature) / 2

                    hot_pipe_delta_T = hot_pipe_T_average - ambient_temperature  # grid supply temperature pipe
                    cold_pipe_delta_T = cold_pipe_T_average - ambient_temperature  # grid return temperature pipe

                    supply_coef = hot_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)
                    return_coef = cold_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)

                    add_delta_T = (grid_delta_T) / (1 - grid_losses_power / power_last_iteration) - grid_delta_T
                    new_delta_T_supply = add_delta_T * supply_coef
                    new_delta_T_return = add_delta_T * return_coef

                    if abs(new_delta_T_supply - delta_T_supply) < 0.001 and abs(new_delta_T_supply - delta_T_supply) < 0.001:
                        delta_T_supply = copy(new_delta_T_supply)
                        delta_T_return = copy(new_delta_T_return)
                        converge = True

                    else:
                        delta_T_supply = copy(new_delta_T_supply)
                        delta_T_return = copy(new_delta_T_return)


            source_grid_return_temperature = sink_group_grid_return_temperature - delta_T_return
            source_grid_supply_temperature = sink_group_grid_supply_temperature + delta_T_supply

            # only convert sources where grid supply temperature is inferior to max_grid_temperature
            if source_grid_supply_temperature <= max_grid_temperature:

                    # design/cost equipment
                    if stream['stream_type'] == 'excess_heat' or stream['stream_type'] == 'outflow':

                        # get stream hourly generation capacity
                        hourly_stream_capacity = stream['hourly_generation']

                        # get stream nominal capacity
                        stream_nominal_capacity = max(hourly_stream_capacity)  # [kW]


                        # design technologies
                        if stream['supply_temperature'] > stream['target_temperature']:

                            # get HX grid temperatures
                            hx_source_supply_temperature = source_grid_supply_temperature + hx_delta_T

                            if stream['supply_temperature'] >= safety_temperature:
                                hx_number = 2
                                intermediate_circuit = True
                            else:
                                hx_number = 1
                                intermediate_circuit = False

                            # heating technologies not needed
                            if stream['supply_temperature'] >= hx_source_supply_temperature + hx_delta_T*hx_number:

                                #  check if intermediate circuit is needed
                                if intermediate_circuit == True:
                                    # get intermediate circuit temperatures
                                    hx_intermediate_supply_temperature = source_grid_supply_temperature + hx_delta_T
                                    hx_intermediate_return_temperature = source_grid_return_temperature + hx_delta_T

                                    # add HX intermediate
                                    hx_intermediate_supply_temperature, hx_intermediate_return_temperature,hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(hx_intermediate_supply_temperature, hx_intermediate_return_temperature,stream['supply_temperature'], stream['target_temperature'], hx_delta_T)
                                    hx_power = stream_nominal_capacity * (abs(hx_stream_supply_temperature - hx_stream_target_temperature) / abs(stream['supply_temperature'] - stream['target_temperature']))
                                    stream_available_capacity = copy(hx_power)

                                    info_hx_intermediate = Add_HX(hx_stream_supply_temperature, hx_stream_target_temperature, stream['fluid'], hx_intermediate_supply_temperature, hx_intermediate_return_temperature,intermediate_fluid,  hx_power,power_fraction)

                                    # add intermediation circulation pumping
                                    info_pump_intermediate = Add_Pump(country, consumer_type,intermediate_fluid, info_hx_intermediate.available_power, power_fraction,hx_intermediate_supply_temperature, hx_intermediate_return_temperature)

                                    # add HX to grid
                                    hx_power = info_hx_intermediate.available_power
                                    info_hx_grid = Add_HX(hx_intermediate_supply_temperature, hx_intermediate_return_temperature, intermediate_fluid, source_grid_supply_temperature, source_grid_return_temperature,grid_fluid, hx_power,power_fraction)

                                    # add circulation pumping to grid
                                    info_pump_grid = Add_Pump(country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction,source_grid_supply_temperature, source_grid_return_temperature)

                                    info = join_hx_and_technology([info_hx_intermediate,info_pump_intermediate,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                    conversion_technologies.append(info)

                                else:
                                    # add HX to grid
                                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(stream['supply_temperature'], stream['target_temperature'], source_grid_supply_temperature,source_grid_return_temperature, hx_delta_T)
                                    hx_power = stream_nominal_capacity / (abs(stream['target_temperature'] - stream['supply_temperature'])) * abs(hx_stream_supply_temperature - hx_stream_target_temperature)
                                    stream_available_capacity = copy(hx_power)
                                    info_hx_grid = Add_HX(hx_stream_supply_temperature, hx_stream_target_temperature, stream['fluid'], source_grid_supply_temperature, source_grid_return_temperature, grid_fluid, hx_power,power_fraction)

                                    # add circulation pumping to grid
                                    info_pump_grid = Add_Pump(country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction, hx_grid_supply_temperature, hx_grid_return_temperature)

                                    info = join_hx_and_technology([info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                    conversion_technologies.append(info)


                                # add orc cascaded
                                orc_type,stream_available_capacity,orc_electrical_generation,overall_thermal_capacity,hx_stream_target_temperature,intermediate_circuit,hx_intermediate_supply_temperature,hx_intermediate_return_temperature = design_orc(stream['capacity'],stream['fluid'], stream['supply_temperature'],stream['target_temperature'], hx_delta_T,orc_cond_supply_temperature, orc_T_evap, hx_efficiency,aggregate_streams=False)
                                if intermediate_circuit == True:
                                    hx_number = 1
                                else:
                                    hx_number = 0

                                if stream['supply_temperature'] >= (orc_T_evap + hx_delta_T*hx_number):

                                    info_technology = Add_ORC_Cascaded(orc_cond_supply_temperature, orc_type, overall_thermal_capacity, orc_electrical_generation,power_fraction)

                                    # get intermediate circuit
                                    if intermediate_circuit == True:
                                        # add HX intermediate
                                        hx_stream_supply_temperature = stream['supply_temperature']
                                        hx_power = copy(stream_available_capacity)
                                        info_hx_intermediate = Add_HX(hx_stream_supply_temperature,hx_stream_target_temperature, stream['fluid'],hx_intermediate_supply_temperature,hx_intermediate_return_temperature,intermediate_fluid, hx_power, power_fraction)

                                        # add circulation pumping to intermediate circuit
                                        info_pump_intermediate = Add_Pump(country, consumer_type,orc_intermediate_fluid, info_hx_intermediate.available_power, power_fraction,hx_intermediate_supply_temperature,hx_intermediate_return_temperature)

                                    if orc_cond_supply_temperature < (source_grid_supply_temperature + hx_delta_T):
                                        boiler_supply_capacity = info_technology.supply_capacity * (hx_source_supply_temperature - orc_cond_supply_temperature)/(orc_cond_supply_temperature - orc_cond_target_temperature)
                                        for fuel in boiler_fuel_type:
                                            info_boiler = Add_Boiler(fuel, country, consumer_type, boiler_supply_capacity, power_fraction, hx_source_supply_temperature,orc_cond_supply_temperature)
                                            info_all_boilers.append(info_boiler)
                                    else:
                                        boiler_supply_capacity = 0
                                        info_all_boilers = []

                                    # add circulation pumping to grid
                                    if intermediate_circuit is True and orc_cond_supply_temperature < (source_grid_supply_temperature + hx_delta_T) and orc_cond_target_temperature > (source_grid_return_temperature + hx_delta_T):
                                        for info_boiler in info_all_boilers:
                                            info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,info_technology.supply_capacity ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                            info = join_hx_and_technology([info_hx_intermediate,info_pump_intermediate, info_technology,info_boiler, info_pump_grid],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                            conversion_technologies.append(info)

                                    elif intermediate_circuit is True and orc_cond_supply_temperature < (source_grid_supply_temperature + hx_delta_T):
                                        for info_boiler in info_all_boilers:
                                            info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,info_technology.supply_capacity * (orc_cond_supply_temperature - (source_grid_return_temperature + hx_delta_T))/(source_grid_supply_temperature-source_grid_return_temperature) ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                            info = join_hx_and_technology([info_hx_intermediate,info_pump_intermediate, info_technology, info_boiler,info_pump_grid],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                            conversion_technologies.append(info)

                                    elif orc_cond_supply_temperature < (source_grid_supply_temperature + hx_delta_T) and orc_cond_target_temperature > (source_grid_return_temperature + hx_delta_T):
                                        for info_boiler in info_all_boilers:
                                            info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,info_technology.supply_capacity,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                            info = join_hx_and_technology([info_technology, info_boiler, info_pump_grid],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                            conversion_technologies.append(info)

                                    elif orc_cond_supply_temperature < (source_grid_supply_temperature + hx_delta_T):
                                        for info_boiler in info_all_boilers:
                                            info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,(info_technology.supply_capacity + boiler_supply_capacity) * (hx_source_supply_temperature -(source_grid_return_temperature + hx_delta_T))/(hx_source_supply_temperature - orc_cond_target_temperature) ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                            info = join_hx_and_technology([info_technology, info_boiler, info_pump_grid],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                            conversion_technologies.append(info)
                                    else:
                                        info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,info_technology.supply_capacity ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                        info = join_hx_and_technology([info_technology, info_pump_grid],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                        conversion_technologies.append(info)


                            # grid may not supply enough heat to the source
                            # add heating technologies
                            else:

                                # get heat extra needed to be supplied
                                needed_supply_capacity = stream['capacity'] * (hx_source_supply_temperature - stream['supply_temperature']) / (stream['supply_temperature'] - stream['target_temperature'])

                                # add HX to grid
                                hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature, = source_get_hx_temperatures(source_grid_supply_temperature, source_grid_return_temperature, hx_source_supply_temperature, stream['target_temperature'], hx_delta_T)
                                hx_power = stream_nominal_capacity * (abs(hx_stream_supply_temperature - hx_stream_target_temperature)) / abs(stream['supply_temperature'] - stream['target_temperature'])
                                info_hx_grid = Add_HX(hx_stream_supply_temperature,hx_stream_target_temperature, stream['fluid'], source_grid_supply_temperature, source_grid_return_temperature,grid_fluid, hx_power, power_fraction)

                                needed_yearly_capacity = sum([needed_supply_capacity*i for i in stream['schedule']])  # [kWh]
                                stream_available_capacity = stream_nominal_capacity * (abs(stream['supply_temperature'] - hx_stream_target_temperature)) / abs(stream['supply_temperature'] - stream['target_temperature'])

                                # add circulation pumping to grid
                                info_pump_grid = Add_Pump(country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction, source_grid_supply_temperature, source_grid_return_temperature)

                                # add boiler
                                for fuel in boiler_fuel_type:
                                    info_technology = Add_Boiler(fuel, country, consumer_type,needed_supply_capacity, power_fraction, hx_source_supply_temperature, stream['supply_temperature'])
                                    info = join_hx_and_technology([info_technology,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                    conversion_technologies.append(info)

                                # add solar thermal + boiler as backup
                                info_technology_solar_thermal = Add_Solar_Thermal(country, consumer_type, latitude, longitude, needed_supply_capacity, power_fraction,hx_source_supply_temperature, stream['supply_temperature'])
                                info_technology_boiler = Add_Boiler('natural_gas', country, consumer_type, needed_supply_capacity,power_fraction, hx_source_supply_temperature,stream['supply_temperature'])
                                info = join_hx_and_technology([info_technology_solar_thermal,info_technology_boiler,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                info['hourly_supply_capacity_normalize'] = info_technology_solar_thermal.data_teo['hourly_supply_capacity_normalize']  # add solar thermal profile
                                # update om_var and emissions
                                coef_solar_thermal = info_technology_solar_thermal.data_teo[ 'hourly_supply_capacity'] / needed_yearly_capacity
                                info['emissions'] = info['emissions'] * (1 - coef_solar_thermal)
                                info['om_var'] = info['om_var'] * (1 - coef_solar_thermal)
                                info['om_fix'] = info['om_fix'] * (1 - coef_solar_thermal)
                                conversion_technologies.append(info)


                                # add solar thermal + boiler as backup
                                info_technology_heat_pump = Add_Heat_Pump(country, consumer_type,needed_supply_capacity, power_fraction, hx_source_supply_temperature, stream['supply_temperature'],ambient_temperature)
                                info = join_hx_and_technology([info_technology_solar_thermal,info_technology_heat_pump,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                # update om_var and emissions
                                info['emissions'] = info['emissions'] * (1 - coef_solar_thermal)
                                info['om_var'] = info['om_var'] * (1 - coef_solar_thermal)
                                info['om_fix'] = info['om_fix'] * (1 - coef_solar_thermal)
                                conversion_technologies.append(info)


                                # add heat pump
                                info_technology = Add_Heat_Pump(country, consumer_type,needed_supply_capacity, power_fraction, hx_source_supply_temperature, stream['supply_temperature'],ambient_temperature)
                                info = join_hx_and_technology([info_technology,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                conversion_technologies.append(info)

                                # add chp
                                for fuel in chp_fuel_type:
                                    info_technology = Add_CHP(fuel, country, consumer_type,needed_supply_capacity, power_fraction, hx_source_supply_temperature, stream['supply_temperature'])
                                    info = join_hx_and_technology([info_technology,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                    conversion_technologies.append(info)

                            output_converted.append({
                                'stream_id': stream['id'],
                                'hourly_stream_capacity': hourly_stream_capacity,  # [kWh]
                                'conversion_technologies': conversion_technologies,  # [€/kW]
                            })

        all_sources_info.append({
            'source_id': source['id'],
            'source_grid_supply_temperature': source_grid_supply_temperature,
            'source_grid_return_temperature': source_grid_return_temperature,
            'streams_converted': output_converted
        })


    #output = json.dumps(output, indent=2)

    return all_sources_info



