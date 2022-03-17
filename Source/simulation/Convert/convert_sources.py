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
     IMPORTANT: it is expected that this script runs multiple times. The first time without knowing the grid losses and thus
     overestimating the source power available to be converted to the grid. The remaining times with estimated grid losses
     by the GIS, which will be used to give a better estimate of the real power available by the sources.


##############################
INPUT:  dict with:

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
                 #          'teo_capacity_factor'
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
                     #                              'tecnhologies' - technologies info in detail
                     #                            }


"""

from copy import copy
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
from ....General.Convert_Equipments.Auxiliary.coef_solar_thermal_backup import coef_solar_thermal_backup


def convert_sources(in_var, kb):


    ############################################################################################################
    # INPUT
    group_of_sources = in_var['platform']['group_of_sources']
    sink_group_grid_supply_temperature = in_var['cf-module']['sink_group_grid_supply_temperature']
    sink_group_grid_return_temperature = in_var['cf-module']['sink_group_grid_return_temperature']

    try:
        grid_losses = in_var['gis-module']['grid_losses']  # vector with losses for each source and stream
        last_iteration_data = in_var['cf-module']['last_iteration_data']  # data output from this function from first iteration
    except:
        grid_losses = []
        last_iteration_data = []


    ############################################################################################################
    # Defined vars
    ambient_temperature = 15

    # Grid Characteristics
    max_grid_temperature = 120  # defined maximum hot water grid temperature [ºC]
    grid_fluid = 'water'
    grid_delta_T = sink_group_grid_supply_temperature - sink_group_grid_return_temperature

    # HX Characteristics
    hx_efficiency = 0.95
    hx_delta_T = 5
    intermediate_fluid = 'thermal_oil'

    # ORC Cascaded Characteristics
    orc_intermediate_fluid = 'water'
    orc_evap_cond_delta_T = 50  # temperature difference between condenser and evaporator

    # Convert_Options Characteristics
    safety_temperature = 100  # if heat stream above this temperature, use intermediate oil circuit [ºC]
    minimum_coef_solar_thermal = 0.3  # solar thermal has to provide at least 30% of streams demand to be considered for TEO
    power_fraction = 0.05  # default value; equipment are designed for max_power and power_fraction*max_power
    boiler_fuel_type = ['electricity', 'natural_gas', 'fuel_oil', 'biomass']  # types of fuel
    chp_fuel_type = ['natural_gas', 'fuel_oil', 'biomass']
    fuels_teo_nomenclature = {'natural_gas': 'ng', 'fuel_oil': 'oil', 'biomass': 'biomass', 'electricity': 'electricity' }

    # Initialize array
    all_sources_info = []


    for source_index,source in enumerate(group_of_sources):
        for stream_index,stream in enumerate(source['streams']):
            hourly_stream_capacity = stream['hourly_generation']
            break

        break


    teo_group_of_sources_capacity_factor = list({} for i in range(len(hourly_stream_capacity)))


    ############################################################################################################
    # ROUTINE
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
                delta_T_supply = 0
                delta_T_return = 0

            # other iterations - grid losses considered
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

            #####################################################################################
            #####################################################################################

            source_grid_return_temperature = sink_group_grid_return_temperature - delta_T_return
            source_grid_supply_temperature = sink_group_grid_supply_temperature + delta_T_supply

            #####################################################################################
            #####################################################################################


            # only convert sources where grid supply temperature is inferior to max_grid_temperature
            if source_grid_supply_temperature <= max_grid_temperature:

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

                                    info_hx_intermediate = Add_HX(kb, hx_stream_supply_temperature, hx_stream_target_temperature, stream['fluid'], hx_intermediate_supply_temperature, hx_intermediate_return_temperature,intermediate_fluid,  hx_power,power_fraction)

                                    # add intermediation circulation pumping
                                    info_pump_intermediate = Add_Pump(kb, country, consumer_type,intermediate_fluid, info_hx_intermediate.available_power, power_fraction,hx_intermediate_supply_temperature, hx_intermediate_return_temperature)

                                    # add HX to grid
                                    hx_power = info_hx_intermediate.available_power
                                    info_hx_grid = Add_HX(kb, hx_intermediate_supply_temperature, hx_intermediate_return_temperature, intermediate_fluid, source_grid_supply_temperature, source_grid_return_temperature,grid_fluid, hx_power,power_fraction)

                                    # add circulation pumping to grid
                                    info_pump_grid = Add_Pump(kb, country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction,source_grid_supply_temperature, source_grid_return_temperature)

                                    teo_equipment_name = 'mhe'
                                    info = join_hx_and_technology(source['id'],[info_hx_intermediate,info_pump_intermediate,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source', teo_equipment_name, stream['id'])
                                    conversion_technologies.append(info)

                                else:
                                    # add HX to grid
                                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(source_grid_supply_temperature,source_grid_return_temperature,stream['supply_temperature'], stream['target_temperature'],  hx_delta_T)
                                    hx_power = stream_nominal_capacity / (abs(stream['target_temperature'] - stream['supply_temperature'])) * abs(hx_stream_supply_temperature - hx_stream_target_temperature)
                                    stream_available_capacity = copy(hx_power)
                                    info_hx_grid = Add_HX(kb, hx_stream_supply_temperature, hx_stream_target_temperature, stream['fluid'], source_grid_supply_temperature, source_grid_return_temperature, grid_fluid, hx_power,power_fraction)

                                    # add circulation pumping to grid
                                    info_pump_grid = Add_Pump(kb, country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction, hx_grid_supply_temperature, hx_grid_return_temperature)
                                    teo_equipment_name = 'she'
                                    info = join_hx_and_technology(source['id'],[info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source', teo_equipment_name, stream['id'])
                                    conversion_technologies.append(info)

                                # add ORC cascaded
                                orc_T_cond = source_grid_supply_temperature + hx_delta_T
                                orc_T_evap = orc_T_cond + orc_evap_cond_delta_T
                                orc_type,stream_available_capacity,orc_electrical_generation,overall_thermal_capacity,hx_stream_target_temperature,intermediate_circuit,hx_intermediate_supply_temperature,hx_intermediate_return_temperature = design_orc(stream['capacity'],stream['fluid'], stream['supply_temperature'],stream['target_temperature'], hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,aggregate_streams=False)
                                if intermediate_circuit == True:
                                    hx_number = 2
                                else:
                                    hx_number = 1

                                if stream['supply_temperature'] >= (orc_T_evap + hx_delta_T*hx_number):
                                    info_technology = Add_ORC_Cascaded(kb, orc_T_cond, orc_type, overall_thermal_capacity, orc_electrical_generation, power_fraction)

                                    # get intermediate circuit
                                    if intermediate_circuit == True:
                                        # add HX intermediate
                                        hx_stream_supply_temperature = stream['supply_temperature']
                                        hx_power = copy(stream_available_capacity)
                                        info_hx_intermediate = Add_HX(kb, hx_stream_supply_temperature,hx_stream_target_temperature, stream['fluid'],hx_intermediate_supply_temperature,hx_intermediate_return_temperature,intermediate_fluid, hx_power, power_fraction)

                                        # add circulation pumping to intermediate circuit
                                        info_pump_intermediate = Add_Pump(kb, country, consumer_type,orc_intermediate_fluid, info_hx_intermediate.available_power, power_fraction,hx_intermediate_supply_temperature,hx_intermediate_return_temperature)

                                    info_pump_grid = Add_Pump(kb, country, consumer_type, grid_fluid,info_technology.supply_capacity ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                    teo_equipment_name = 'orc'

                                    if intermediate_circuit == True:
                                        info = join_hx_and_technology(source['id'],[info_hx_intermediate, info_pump_intermediate, info_technology, info_pump_grid],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source',teo_equipment_name, stream['id'])
                                    else:
                                        info = join_hx_and_technology(source['id'],[info_technology, info_pump_grid],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source',teo_equipment_name, stream['id'])

                                    conversion_technologies.append(info)


                            # grid may not supply enough heat to the source; add heating technologies
                            else:
                                if stream['supply_temperature'] > source_grid_return_temperature + hx_delta_T:
                                    # get heat extra needed to be supplied
                                    booster_outlet_temperature = source_grid_supply_temperature
                                    booster_inlet_temperature = stream['supply_temperature'] - hx_delta_T
                                    needed_supply_capacity = stream['capacity'] * (booster_outlet_temperature - booster_inlet_temperature) / (stream['supply_temperature'] - stream['target_temperature'])

                                    # add HX to grid
                                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature, = source_get_hx_temperatures(booster_inlet_temperature, source_grid_return_temperature, stream['supply_temperature'], stream['target_temperature'], hx_delta_T)
                                    hx_power = stream_nominal_capacity * (abs(hx_stream_supply_temperature - hx_stream_target_temperature)) / abs(stream['supply_temperature'] - stream['target_temperature'])
                                    info_hx_grid = Add_HX(kb, hx_stream_supply_temperature,hx_stream_target_temperature, stream['fluid'], source_grid_supply_temperature, source_grid_return_temperature,grid_fluid, hx_power, power_fraction)

                                    stream_available_capacity = stream_nominal_capacity * (abs(stream['supply_temperature'] - hx_stream_target_temperature)) / abs(stream['supply_temperature'] - stream['target_temperature'])

                                    # add circulation pumping to grid
                                    info_pump_grid = Add_Pump(kb, country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction, booster_inlet_temperature, source_grid_return_temperature)

                                    # add boiler
                                    for fuel in boiler_fuel_type:
                                        info_technology = Add_Boiler(kb, fuel, country, consumer_type,needed_supply_capacity, power_fraction, booster_outlet_temperature, booster_inlet_temperature)
                                        teo_equipment_name = fuels_teo_nomenclature[info_technology.fuel_type] + '_whrb'

                                        info = join_hx_and_technology(source['id'],[info_technology,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source',teo_equipment_name, stream['id'])
                                        conversion_technologies.append(info)

                                    # add solar thermal + boiler as backup

                                    info_technology_solar_thermal = Add_Solar_Thermal(kb, country, consumer_type, latitude, longitude, needed_supply_capacity, power_fraction, booster_outlet_temperature, booster_inlet_temperature,hx_delta_T,hx_efficiency)
                                    for fuel in boiler_fuel_type:
                                        info_technology_boiler = Add_Boiler(kb, fuel, country, consumer_type, needed_supply_capacity,power_fraction,  booster_outlet_temperature, booster_inlet_temperature)
                                        teo_equipment_name = 'solar_thermal_' + fuels_teo_nomenclature[info_technology_boiler.fuel_type] + '_boiler'

                                        coef_solar_thermal, info_technology_boiler = coef_solar_thermal_backup(stream['hourly_generation'], info_technology_solar_thermal, info_technology_boiler)
                                        info = join_hx_and_technology(source['id'],[info_technology_solar_thermal,info_technology_boiler,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source',teo_equipment_name, stream['id'])

                                        if coef_solar_thermal >= minimum_coef_solar_thermal:
                                            conversion_technologies.append(info)


                                    # add solar thermal + heat pump as backup
                                    info_technology_heat_pump = Add_Heat_Pump(kb, country, consumer_type, power_fraction, booster_outlet_temperature, booster_inlet_temperature,ambient_temperature,supply_capacity=needed_supply_capacity)
                                    teo_equipment_name = 'solar_thermal_' + 'hp'
                                    coef_solar_thermal, info_technology_heat_pump = coef_solar_thermal_backup(stream['hourly_generation'], info_technology_solar_thermal, info_technology_heat_pump)
                                    info = join_hx_and_technology(source['id'],[info_technology_solar_thermal,info_technology_heat_pump,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source',teo_equipment_name, stream['id'])

                                    if coef_solar_thermal >= minimum_coef_solar_thermal:
                                        conversion_technologies.append(info)

                                    # add heat pump
                                    heat_pump_T_evap = stream['target_temperature'] - hx_delta_T
                                    heat_pump_evap_capacity = stream_nominal_capacity
                                    info_technology = Add_Heat_Pump(kb, country, consumer_type, power_fraction, source_grid_supply_temperature, source_grid_return_temperature,heat_pump_T_evap,evap_capacity=heat_pump_evap_capacity)
                                    teo_equipment_name = 'hp'
                                    # hp - add circulation pumping to grid
                                    info_pump_grid = Add_Pump(kb, country, consumer_type, grid_fluid, info_technology.supply_capacity, power_fraction,source_grid_supply_temperature, source_grid_return_temperature)
                                    info = join_hx_and_technology(source['id'],[info_technology,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source',teo_equipment_name, stream['id'])
                                    conversion_technologies.append(info)

                                    # add chp
                                    for fuel in chp_fuel_type:
                                        info_technology = Add_CHP(kb, fuel, country, consumer_type,needed_supply_capacity, power_fraction, booster_outlet_temperature, booster_inlet_temperature)
                                        teo_equipment_name = 'chp_' + fuels_teo_nomenclature[info_technology.fuel_type]
                                        info = join_hx_and_technology(source['id'],[info_technology,info_hx_grid,info_pump_grid],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source',teo_equipment_name, stream['id'])
                                        conversion_technologies.append(info)

                                # add heat pump
                                heat_pump_T_evap = stream['target_temperature'] - hx_delta_T
                                heat_pump_evap_capacity = stream_available_capacity = stream_nominal_capacity
                                info_technology = Add_Heat_Pump(kb, country, consumer_type, power_fraction, source_grid_supply_temperature,source_grid_return_temperature,heat_pump_T_evap,evap_capacity=heat_pump_evap_capacity)
                                teo_equipment_name = 'boost_hp'
                                # add HX to hp
                                hx_hp_supply_temperature, hx_hp_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature, = source_get_hx_temperatures(stream['supply_temperature'] - hx_delta_T, stream['target_temperature'] - hx_delta_T,stream['supply_temperature'], stream['target_temperature'], hx_delta_T)
                                hx_power = stream_nominal_capacity
                                info_hx_pump = Add_HX(kb, hx_stream_supply_temperature, hx_stream_target_temperature,stream['fluid'], hx_hp_supply_temperature, hx_hp_return_temperature, 'water', hx_power,power_fraction)

                                # hp - add circulation pumping to grid
                                info_pump_grid = Add_Pump(kb, country, consumer_type, grid_fluid,info_technology.supply_capacity, power_fraction, source_grid_supply_temperature, source_grid_return_temperature)
                                info = join_hx_and_technology(source['id'],
                                                              [info_technology, info_hx_pump, info_pump_grid],
                                                              power_fraction, stream_available_capacity,
                                                              info_pump_grid.supply_capacity, 'source',
                                                              teo_equipment_name, stream['id'])
                                conversion_technologies.append(info)

                            teo_capacity_factor = [i / max(hourly_stream_capacity) for i in hourly_stream_capacity]

                            gis_capacity = conversion_technologies[0]['max_capacity'] * conversion_technologies[0][
                                'conversion_efficiency']

                            output_converted.append({
                                'stream_id': stream['id'],
                                "teo_stream_id": 'source' + str(source['id']) + 'stream' + str(stream['id']),
                                "input_fuel": None,
                                "output_fuel": "excessheat",
                                "output": 1,
                                'gis_capacity': gis_capacity,  # [kW]
                                'hourly_stream_capacity': hourly_stream_capacity,  # [kWh]
                                'teo_capacity_factor': teo_capacity_factor,
                                'max_stream_capacity': max(hourly_stream_capacity),
                                'conversion_technologies': conversion_technologies,  # [€/kW]
                            })



                            for index,i in enumerate(teo_group_of_sources_capacity_factor):
                                teo_id = 'source' + str(source['id']) + 'stream' + str(stream['id'])
                                i[teo_id] = teo_capacity_factor[index]


        # get conversion for each source
        all_sources_info.append({
            'source_id': source['id'],
            'location': [latitude, longitude],
            'source_grid_supply_temperature': source_grid_supply_temperature,
            'source_grid_return_temperature': source_grid_return_temperature,
            'streams_converted': output_converted
        })

    n_supply_list = []
    for source in all_sources_info:
        total_cap = 0
        for stream in source['streams_converted']:
            total_cap += stream['gis_capacity'],  # [kW]

        gis_dict = {
                'id': source['source_id'],
                'coords': source['location'],
                'cap': total_cap
            }

        n_supply_list.append(gis_dict)

    teo_dhn = {
        "technology": "dhn",
        "input_fuel": "dhnwatersupply",
        "output_fuel": "dhnwaterdemand",
        "output": 1,
        "input": 1,
        "max_capacity": 1000000.1,
        "turnkey_a": 0.1,
        "conversion_efficiency": 1,
        "om_fix": 0.1,
        "om_var": 0.1,
        "emissions_factor": 0.1,
        "emissions": "co2",
        "emission": "co2"
    }

    all_info = {
        'all_sources_info': all_sources_info,
        'teo_string': 'dhn',
        "input_fuel": "dhnwatersupply" ,
        "output_fuel": "dhnwaterdemand",
        "output": 1,
        "input": 1,
        'n_supply_list': n_supply_list,
        "teo_capacity_factor_group": teo_group_of_sources_capacity_factor,
        "teo_dhn": teo_dhn
    }

    return all_info



