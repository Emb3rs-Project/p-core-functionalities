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
        # gis_info - array with vectors with grid losses for each stream of source  [[source_1_stream_1_loss, source_1_stream_2_loss],...]

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
from ....Error_Handling.error_convert_sources import MainErrorConvertSources
from ....Error_Handling.runtime_error import ModuleRuntimeException
from .dhn_correct_losses import dhn_correct_losses

def convert_sources(in_var, kb):
    ############################################################################################################
    # INPUT
    # error handling
    MainErrorConvertSources(**in_var)

    group_of_sources = in_var['platform']['group_of_sources']
    sink_group_grid_supply_temperature = in_var['cf_module']['sink_group_grid_supply_temperature']
    sink_group_grid_return_temperature = in_var['cf_module']['sink_group_grid_return_temperature']

    try:
        gis_sources_losses = in_var['gis_module']['source_losses']
        sources_to_analyse = [source['source_id'] for source in gis_sources_losses]

    except:
        gis_sources_losses = []

    try:
        existing_grid_data = in_var['platform']['existing_grid_data']
    except:
        existing_grid_data = None

    try:
        last_iteration_data = in_var['cf_module']['last_iteration_data']  # data output from this function from first iteration
    except:
        last_iteration_data = []


    ############################################################################################################
    # Defined vars
    ambient_temperature = 15
    delta_T_buffer = 6  # sources to grid delta_T buffer

    # Grid Characteristics
    max_grid_temperature = 120  # defined maximum hot water grid temperature [ºC]
    grid_fluid = 'water'

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
    fuels_teo_nomenclature = {'natural_gas': 'ng', 'fuel_oil': 'oil', 'biomass': 'biomass', 'electricity': 'electricity'}

    # Initialize array
    all_sources_info = []
    for source_index, source in enumerate(group_of_sources):
        for stream_index, stream in enumerate(source['streams']):
            hourly_stream_capacity = stream['hourly_generation']
            break
        break

    teo_group_of_sources_capacity_factor = list({} for i in range(len(hourly_stream_capacity)))

    ############################################################################################################
    # ROUTINE
    try:
        for source_index, source in enumerate(group_of_sources):

            output_converted = []
            latitude, longitude = source['location']
            country = get_country(latitude, longitude)
            consumer_type = source['consumer_type']

            #########################################################
            ###################### TO BE REMOVED ####################
            #########################################################
            old_version = True
            if old_version == True:
                if gis_sources_losses == []:
                    analyse_source = True  # first iteration analyse all sources
                else:
                    if str(source['id']) in sources_to_analyse:
                        analyse_source = True

                        for source_loss_info in gis_sources_losses:
                            if source_loss_info['source_id'] == str(source['id']):
                                source_loss = source_loss_info['losses_total']
                                break
                    else:
                        analyse_source = False

            #########################################################
            #########################################################
            #########################################################
            analyse_source = True
            if analyse_source == True:

                #########################################################
                ###################### TO BE REMOVED ####################
                #########################################################
                old_version = True
                if old_version == True:
                    # first iteration - grid losses not considered
                    if gis_sources_losses == []:
                        source_grid_supply_temperature = sink_group_grid_supply_temperature
                        source_grid_return_temperature = sink_group_grid_return_temperature

                    # other iterations - grid losses considered
                    else:
                        # get source max power supplied on last iteration
                        for cap_source in last_iteration_data["n_supply_list"]:
                            if cap_source['id'] == source['id']:
                                power_last_iteration = cap_source['cap']
                                break

                        source_grid_supply_temperature, source_grid_return_temperature = dhn_correct_losses(power_last_iteration, source_loss, sink_group_grid_supply_temperature, sink_group_grid_return_temperature, max_grid_temperature)

                #########################################################
                #########################################################
                #########################################################

                # get conversion technologies for each stream
                for stream_index, stream in enumerate(source['streams']):

                    conversion_technologies = []
                    source_grid_supply_temperature = sink_group_grid_supply_temperature + delta_T_buffer
                    source_grid_return_temperature = sink_group_grid_return_temperature - delta_T_buffer

                    # only convert sources where grid supply temperature is inferior to max_grid_temperature
                    if source_grid_supply_temperature is not None:
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
                                    if stream[ 'supply_temperature'] >= hx_source_supply_temperature + hx_delta_T * hx_number:

                                        #  check if intermediate circuit is needed
                                        if intermediate_circuit == True:
                                            # get intermediate circuit temperatures
                                            hx_intermediate_supply_temperature = source_grid_supply_temperature + hx_delta_T
                                            hx_intermediate_return_temperature = source_grid_return_temperature + hx_delta_T

                                            # add HX intermediate
                                            hx_intermediate_supply_temperature, hx_intermediate_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(hx_intermediate_supply_temperature, hx_intermediate_return_temperature, stream['supply_temperature'], stream['target_temperature'], hx_delta_T)
                                            hx_power = stream_nominal_capacity * (abs(hx_stream_supply_temperature - hx_stream_target_temperature) / abs(stream['supply_temperature'] - stream['target_temperature']))

                                            stream_available_capacity = copy(hx_power)

                                            info_hx_intermediate = Add_HX(kb,
                                                                          hx_stream_supply_temperature,
                                                                          hx_stream_target_temperature,
                                                                          stream['fluid'],
                                                                          hx_intermediate_supply_temperature,
                                                                          hx_intermediate_return_temperature,
                                                                          intermediate_fluid,
                                                                          hx_power,
                                                                          power_fraction)

                                            # add intermediation circulation pumping
                                            info_pump_intermediate = Add_Pump(kb,
                                                                              country,
                                                                              consumer_type,
                                                                              intermediate_fluid,
                                                                              info_hx_intermediate.available_power,
                                                                              power_fraction,
                                                                              hx_intermediate_supply_temperature,
                                                                              hx_intermediate_return_temperature)

                                            # add HX to grid
                                            hx_power = info_hx_intermediate.available_power
                                            info_hx_grid = Add_HX(kb,
                                                                  hx_intermediate_supply_temperature,
                                                                  hx_intermediate_return_temperature,
                                                                  intermediate_fluid,
                                                                  source_grid_supply_temperature,
                                                                  source_grid_return_temperature,
                                                                  grid_fluid,
                                                                  hx_power,
                                                                  power_fraction)

                                            # add circulation pumping to grid
                                            info_pump_grid = Add_Pump(kb,
                                                                      country,
                                                                      consumer_type,
                                                                      grid_fluid,
                                                                      info_hx_grid.available_power,
                                                                      power_fraction,
                                                                      source_grid_supply_temperature,
                                                                      source_grid_return_temperature)

                                            teo_equipment_name = 'mhex'
                                            info = join_hx_and_technology(source['id'],
                                                                          [info_hx_intermediate, info_pump_intermediate,info_hx_grid, info_pump_grid],
                                                                          power_fraction,
                                                                          stream_available_capacity,
                                                                          info_pump_grid.supply_capacity,
                                                                          'sou',
                                                                          teo_equipment_name,
                                                                          stream['id'])

                                            conversion_technologies.append(info)

                                        else:
                                            # add HX to grid
                                            hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(source_grid_supply_temperature, source_grid_return_temperature,stream['supply_temperature'], stream['target_temperature'], hx_delta_T)
                                            hx_power = stream_nominal_capacity / (abs(stream['target_temperature'] - stream['supply_temperature'])) * abs(hx_stream_supply_temperature - hx_stream_target_temperature)

                                            stream_available_capacity = copy(hx_power)

                                            info_hx_grid = Add_HX(kb,
                                                                  hx_stream_supply_temperature,
                                                                  hx_stream_target_temperature,
                                                                  stream['fluid'],
                                                                  source_grid_supply_temperature,
                                                                  source_grid_return_temperature,
                                                                  grid_fluid,
                                                                  hx_power,
                                                                  power_fraction)

                                            # add circulation pumping to grid
                                            info_pump_grid = Add_Pump(kb,
                                                                      country,
                                                                      consumer_type,
                                                                      grid_fluid,
                                                                      info_hx_grid.available_power,
                                                                      power_fraction,
                                                                      hx_grid_supply_temperature,
                                                                      hx_grid_return_temperature)

                                            teo_equipment_name = 'shex'

                                            info = join_hx_and_technology(source['id'],
                                                                          [info_hx_grid, info_pump_grid],
                                                                          power_fraction,
                                                                          stream_available_capacity,
                                                                          info_pump_grid.supply_capacity,
                                                                          'sou',
                                                                          teo_equipment_name,
                                                                          stream['id'])

                                            conversion_technologies.append(info)

                                        # add ORC cascaded
                                        orc_T_cond = source_grid_supply_temperature + hx_delta_T
                                        orc_T_evap = orc_T_cond + orc_evap_cond_delta_T
                                        orc_type, stream_available_capacity, orc_electrical_generation, overall_thermal_capacity, hx_stream_target_temperature, intermediate_circuit, hx_intermediate_supply_temperature, hx_intermediate_return_temperature = design_orc(stream['capacity'], stream['fluid'], stream['supply_temperature'],stream['target_temperature'], hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,aggregate_streams=False)

                                        if intermediate_circuit == True:
                                            hx_number = 2
                                        else:
                                            hx_number = 1

                                        if stream['supply_temperature'] >= (orc_T_evap + hx_delta_T * hx_number):
                                            info_technology = Add_ORC_Cascaded(kb,
                                                                               orc_T_cond,
                                                                               orc_type,
                                                                               overall_thermal_capacity,
                                                                               orc_electrical_generation,
                                                                               power_fraction)

                                            # get intermediate circuit
                                            if intermediate_circuit == True:
                                                # add HX intermediate
                                                hx_stream_supply_temperature = stream['supply_temperature']
                                                hx_power = copy(stream_available_capacity)
                                                info_hx_intermediate = Add_HX(kb,
                                                                              hx_stream_supply_temperature,
                                                                              hx_stream_target_temperature,
                                                                              stream['fluid'],
                                                                              hx_intermediate_supply_temperature,
                                                                              hx_intermediate_return_temperature,
                                                                              intermediate_fluid,
                                                                              hx_power,
                                                                              power_fraction)

                                                # add circulation pumping to intermediate circuit
                                                info_pump_intermediate = Add_Pump(kb,
                                                                                  country,
                                                                                  consumer_type,
                                                                                  orc_intermediate_fluid,
                                                                                  info_hx_intermediate.available_power,
                                                                                  power_fraction,
                                                                                  hx_intermediate_supply_temperature,
                                                                                  hx_intermediate_return_temperature)

                                            info_pump_grid = Add_Pump(kb,
                                                                      country,
                                                                      consumer_type,
                                                                      grid_fluid,
                                                                      info_technology.supply_capacity,
                                                                      power_fraction,
                                                                      source_grid_supply_temperature,
                                                                      source_grid_return_temperature)
                                            teo_equipment_name = 'orc'

                                            if intermediate_circuit == True:
                                                info = join_hx_and_technology(source['id'],
                                                                              [info_hx_intermediate, info_pump_intermediate,
                                                                               info_technology,
                                                                               info_pump_grid],
                                                                              power_fraction,
                                                                              stream_available_capacity,
                                                                              info_pump_grid.supply_capacity,
                                                                              'sou',
                                                                              teo_equipment_name,
                                                                              stream['id'])
                                            else:
                                                info = join_hx_and_technology(source['id'],
                                                                              [info_technology, info_pump_grid],
                                                                              power_fraction,
                                                                              stream_available_capacity,
                                                                              info_pump_grid.supply_capacity,
                                                                              'sou',
                                                                              teo_equipment_name,
                                                                              stream['id'])

                                            conversion_technologies.append(info)


                                    # grid may not supply enough heat to the source; add heating technologies
                                    else:
                                        if stream['supply_temperature'] > source_grid_return_temperature + hx_delta_T:
                                            # get heat extra needed to be supplied
                                            booster_outlet_temperature = source_grid_supply_temperature
                                            booster_inlet_temperature = stream['supply_temperature'] - hx_delta_T
                                            needed_supply_capacity = stream['capacity'] * (booster_outlet_temperature - booster_inlet_temperature) / (stream['supply_temperature'] - stream[ 'target_temperature'])

                                            # add HX to grid
                                            hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature, = source_get_hx_temperatures(booster_inlet_temperature, source_grid_return_temperature,stream['supply_temperature'], stream['target_temperature'], hx_delta_T)

                                            hx_power = stream_nominal_capacity * (abs(hx_stream_supply_temperature - hx_stream_target_temperature)) / abs(stream['supply_temperature'] - stream['target_temperature'])

                                            info_hx_grid = Add_HX(kb,
                                                                  hx_stream_supply_temperature,
                                                                  hx_stream_target_temperature,
                                                                  stream['fluid'],
                                                                  source_grid_supply_temperature,
                                                                  source_grid_return_temperature,
                                                                  grid_fluid,
                                                                  hx_power,
                                                                  power_fraction)

                                            stream_available_capacity = stream_nominal_capacity * ( abs(stream['supply_temperature'] - hx_stream_target_temperature)) / abs( stream['supply_temperature'] - stream['target_temperature'])

                                            # add circulation pumping to grid
                                            info_pump_grid = Add_Pump(kb,
                                                                      country,
                                                                      consumer_type,
                                                                      grid_fluid,
                                                                      info_hx_grid.available_power,
                                                                      power_fraction,
                                                                      booster_inlet_temperature,
                                                                      source_grid_return_temperature)

                                            # add boiler
                                            for fuel in boiler_fuel_type:
                                                info_technology = Add_Boiler(kb,
                                                                             fuel,
                                                                             country,
                                                                             consumer_type,
                                                                             needed_supply_capacity,
                                                                             power_fraction,
                                                                             booster_outlet_temperature,
                                                                             booster_inlet_temperature)

                                                teo_equipment_name = fuels_teo_nomenclature[info_technology.fuel_type] + '_whrb'

                                                info = join_hx_and_technology(source['id'],
                                                                              [info_technology, info_hx_grid,info_pump_grid],
                                                                              power_fraction,
                                                                              stream_available_capacity,
                                                                              info_pump_grid.supply_capacity,
                                                                              'sou',
                                                                              teo_equipment_name,
                                                                              stream['id'])

                                                conversion_technologies.append(info)

                                            # add solar thermal + boiler as backup
                                            info_technology_solar_thermal = Add_Solar_Thermal(kb,
                                                                                              country,
                                                                                              consumer_type,
                                                                                              latitude,
                                                                                              longitude,
                                                                                              needed_supply_capacity,
                                                                                              power_fraction,
                                                                                              booster_outlet_temperature,
                                                                                              booster_inlet_temperature,
                                                                                              hx_delta_T,
                                                                                              hx_efficiency)
                                            for fuel in boiler_fuel_type:
                                                info_technology_boiler = Add_Boiler(kb,
                                                                                    fuel,
                                                                                    country,
                                                                                    consumer_type,
                                                                                    needed_supply_capacity,
                                                                                    power_fraction,
                                                                                    booster_outlet_temperature,
                                                                                    booster_inlet_temperature)

                                                teo_equipment_name = 'st_' + fuels_teo_nomenclature[info_technology_boiler.fuel_type] + '_boiler'

                                                coef_solar_thermal, info_technology_boiler = coef_solar_thermal_backup(stream['hourly_generation'], info_technology_solar_thermal,info_technology_boiler)

                                                info = join_hx_and_technology(source['id'],
                                                                              [info_technology_solar_thermal,info_technology_boiler,info_hx_grid, info_pump_grid],
                                                                              power_fraction,
                                                                              stream_available_capacity,
                                                                              info_pump_grid.supply_capacity,
                                                                              'sou',
                                                                              teo_equipment_name,
                                                                              stream['id'])

                                                if coef_solar_thermal >= minimum_coef_solar_thermal:
                                                    conversion_technologies.append(info)

                                            # add solar thermal + heat pump as backup
                                            teo_equipment_name = 'st_' + 'hp'
                                            info_technology_heat_pump = Add_Heat_Pump(kb,
                                                                                      country,
                                                                                      consumer_type,
                                                                                      power_fraction,
                                                                                      booster_outlet_temperature,
                                                                                      booster_inlet_temperature,
                                                                                      ambient_temperature,
                                                                                      supply_capacity=needed_supply_capacity)

                                            coef_solar_thermal, info_technology_heat_pump = coef_solar_thermal_backup(stream['hourly_generation'], info_technology_solar_thermal,info_technology_heat_pump)

                                            info = join_hx_and_technology(source['id'],
                                                                          [info_technology_solar_thermal, info_technology_heat_pump,info_hx_grid, info_pump_grid],
                                                                          power_fraction,
                                                                          stream_available_capacity,
                                                                          info_pump_grid.supply_capacity,
                                                                          'sou',
                                                                          teo_equipment_name,
                                                                          stream['id'])

                                            if coef_solar_thermal >= minimum_coef_solar_thermal:
                                                conversion_technologies.append(info)

                                            # add heat pump
                                            teo_equipment_name = 'hp'
                                            heat_pump_T_evap = stream['target_temperature'] - hx_delta_T
                                            heat_pump_evap_capacity = stream_nominal_capacity
                                            info_technology = Add_Heat_Pump(kb,
                                                                            country,
                                                                            consumer_type,
                                                                            power_fraction,
                                                                            source_grid_supply_temperature,
                                                                            source_grid_return_temperature,
                                                                            heat_pump_T_evap,
                                                                            evap_capacity=heat_pump_evap_capacity)

                                            # hp - add circulation pumping to grid
                                            info_pump_grid = Add_Pump(kb,
                                                                      country,
                                                                      consumer_type,
                                                                      grid_fluid,
                                                                      info_technology.supply_capacity,
                                                                      power_fraction,
                                                                      source_grid_supply_temperature,
                                                                      source_grid_return_temperature)

                                            info = join_hx_and_technology(source['id'],
                                                                          [info_technology,
                                                                           info_hx_grid,
                                                                           info_pump_grid],
                                                                          power_fraction,
                                                                          stream_available_capacity,
                                                                          info_pump_grid.supply_capacity,
                                                                          'sou',
                                                                          teo_equipment_name,
                                                                          stream['id'])

                                            conversion_technologies.append(info)

                                            # add chp
                                            for fuel in chp_fuel_type:
                                                info_technology = Add_CHP(kb,
                                                                          fuel,
                                                                          country,
                                                                          consumer_type,
                                                                          needed_supply_capacity,
                                                                          power_fraction,
                                                                          booster_outlet_temperature,
                                                                          booster_inlet_temperature)

                                                teo_equipment_name = 'chp_' + fuels_teo_nomenclature[info_technology.fuel_type]

                                                info = join_hx_and_technology(source['id'],
                                                                              [info_technology, info_hx_grid,info_pump_grid],
                                                                              power_fraction,
                                                                              stream_available_capacity,
                                                                              info_pump_grid.supply_capacity,
                                                                              'sou',
                                                                              teo_equipment_name,
                                                                              stream['id'])

                                                conversion_technologies.append(info)

                                        # add heat pump
                                        teo_equipment_name = 'boost_hp'
                                        heat_pump_T_evap = stream['target_temperature'] - hx_delta_T
                                        heat_pump_evap_capacity = stream_available_capacity = stream_nominal_capacity
                                        info_technology = Add_Heat_Pump(kb,
                                                                        country,
                                                                        consumer_type,
                                                                        power_fraction,
                                                                        source_grid_supply_temperature,
                                                                        source_grid_return_temperature,
                                                                        heat_pump_T_evap,
                                                                        evap_capacity=heat_pump_evap_capacity)

                                        # add HX to hp
                                        hx_hp_supply_temperature, hx_hp_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature, = source_get_hx_temperatures(stream['supply_temperature'] - hx_delta_T,stream['target_temperature'] - hx_delta_T, stream['supply_temperature'],stream['target_temperature'], hx_delta_T)
                                        hx_power = stream_nominal_capacity

                                        info_hx_pump = Add_HX(kb,
                                                              hx_stream_supply_temperature,
                                                              hx_stream_target_temperature,
                                                              stream['fluid'],
                                                              hx_hp_supply_temperature,
                                                              hx_hp_return_temperature,
                                                              'water',
                                                              hx_power,
                                                              power_fraction)

                                        # hp - add circulation pumping to grid
                                        info_pump_grid = Add_Pump(kb,
                                                                  country,
                                                                  consumer_type,
                                                                  grid_fluid,
                                                                  info_technology.supply_capacity,
                                                                  power_fraction,
                                                                  source_grid_supply_temperature,
                                                                  source_grid_return_temperature)

                                        info = join_hx_and_technology(source['id'],
                                                                      [info_technology, info_hx_pump, info_pump_grid],
                                                                      power_fraction,
                                                                      stream_available_capacity,
                                                                      info_pump_grid.supply_capacity,
                                                                      'sou',
                                                                      teo_equipment_name,
                                                                      stream['id'])

                                        conversion_technologies.append(info)

                                    teo_capacity_factor = [i / max(hourly_stream_capacity) for i in hourly_stream_capacity]
                                    gis_capacity = conversion_technologies[0]['max_capacity'] * conversion_technologies[0]['conversion_efficiency']

                                    output_converted.append({
                                        'stream_id': stream['id'],
                                        "teo_stream_id": 'str' + str(stream['id']) + 'sou' + str(source['id']),
                                        "input_fuel": None,
                                        "output_fuel": "eh" + 'str' + str(stream['id']) + 'sou' + str(source['id']),
                                        "output": 1,
                                        'gis_capacity': gis_capacity,  # [kW]
                                        'hourly_stream_capacity': hourly_stream_capacity,  # [kWh]
                                        'teo_capacity_factor': teo_capacity_factor,
                                        'max_stream_capacity': max(hourly_stream_capacity),
                                        'conversion_technologies': conversion_technologies,  # [€/kW]
                                    })

                                    for index, i in enumerate(teo_group_of_sources_capacity_factor):
                                        teo_id = 'str' + str(stream['id']) + 'sou' + str(source['id'])
                                        i[teo_id] = teo_capacity_factor[index]

                # get conversion for each source
                if output_converted != []:
                    all_sources_info.append({
                        'source_id': source['id'],
                        'location': [latitude, longitude],
                        'source_grid_supply_temperature': source_grid_supply_temperature,
                        'source_grid_return_temperature': source_grid_return_temperature,
                        'streams_converted': output_converted
                    })

    except:
        raise ModuleRuntimeException(
            code="1",
            type="convert_sources.py",
            msg="Source' streams conversion infeasible. Check sources' streams. \n "
                "If all inputs are correct report to the platform."
        )


    ############################
    if existing_grid_data is not None:
        grid_id = existing_grid_data['id']
        latitude, longitude = existing_grid_data['location']
        levelized_co2_emissions = existing_grid_data['levelized_co2_emissions']
        levelized_om_var = existing_grid_data['levelized_om_var']
        levelized_om_fix = existing_grid_data['levelized_om_fix']

        ex_grid = {
                      "teo_equipment_name": "ex_grid",
                      "output": 1,
                      "input_fuel": None,
                      "output_fuel": "dhnwatersupply",
                      "equipment": [],
                      "max_capacity": 10**8,
                      "turnkey_a": 0,
                      "turnkey_b": 0,
                      "conversion_efficiency": 1,
                      "om_fix": levelized_om_fix,
                      "om_var": levelized_om_var,
                      "emissions": levelized_co2_emissions,
                      "technologies": []
            }
    else:
        ex_grid = []

    ##############################
    # OUTPUT
    n_supply_list = []
    for source in all_sources_info:
        total_cap = 0
        for stream in source['streams_converted']:
            total_cap += float(stream['gis_capacity'])  # [kW]

        if total_cap != 0:
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
        'ex_grid': ex_grid,
        'teo_string': 'dhn',
        "input_fuel": "dhnwatersupply",
        "output_fuel": "dhnwaterdem",
        "output": 1,
        "input": 1,
        'n_supply_list': n_supply_list,
        "teo_capacity_factor_group": teo_group_of_sources_capacity_factor,
        "teo_dhn": teo_dhn
    }


    return all_info
