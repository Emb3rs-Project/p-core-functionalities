import numpy as np
import copy
from ...General.Convert_Equipments.Auxiliary.sink_get_hx_temperatures import sink_get_hx_temperatures
from ...General.Convert_Equipments.Convert_Options.add_boiler import Add_Boiler
from ...General.Convert_Equipments.Convert_Options.add_hx import Add_HX
from ...General.Convert_Equipments.Convert_Options.add_solar_thermal import Add_Solar_Thermal
from ...General.Convert_Equipments.Convert_Options.add_heat_pump import Add_Heat_Pump
from ...General.Convert_Equipments.Convert_Options.add_thermal_chiller import Add_Thermal_Chiller
from ...General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from ...General.Convert_Equipments.Auxiliary.aggregate_technologies_info import aggregate_technologies_info
from ...General.Convert_Equipments.Convert_Options.add_electric_chiller import Add_Electric_Chiller
from ...General.Convert_Equipments.Auxiliary.coef_solar_thermal_backup import coef_solar_thermal_backup
from ...Error_Handling.error_convert_sinks import PlatformConvertSinks
from ...Error_Handling.runtime_error import ModuleRuntimeException

def convert_sinks(in_var, kb):
    """Design of Grid - Sinks conversion technologies.

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

    Parameters
    ----------
    in_var :  All necessary data to perform the grid to sinks conversion with the following key:

        platform: dict
            Data obtained from the platform

                - grid_supply_temperature : float, optional
                    Grid supply temperature provided by the user [ºC]

                - grid_return_temperature : float, optional
                    Grid return temperature provided by the user [ºC]

                - group_of_sinks : list with dict
                    List with all sinks to be analyzed; each with the following keys:

                        - id : int
                            Sink ID []

                        - location : list
                            [latitude, longitude] [º]

                        - fuels_data: dict:
                            Fuels price and CO2 emission, with the following keys:

                                - natural_gas: dict
                                    Natural gas data

                                        - co2_emissions: float:
                                            Fuel CO2 emission [kg CO2/kWh

                                        - price: float:
                                            Fuel price [€/kWh

                                - fuel_oil
                                    Same keys as "natural_gas"

                                - electricity
                                    Same keys as "natural_gas"

                                - biomass
                                    Same keys as "natural_gas"

                        - streams : list with dict
                            Streams to be analyzed. Each stream with the following keys:

                                - id : int
                                    Stream ID []

                                - name : str
                                    Stream name []

                                - object_type : str
                                    DEFAULT = "stream" []

                                - object_linked_id
                                    None: DEFAULT=NONE, since no equipment/process is associated

                                - stream_type : str
                                    Stream designation []; inflow, outflow, excess_heat

                                - supply_temperature : float
                                    Stream's supply/initial temperature [ºC]

                                - target_temperature : float
                                    Stream's target/final temperature [ºC]

                                - fluid : str
                                    Stream fluid name

                                - flowrate : float
                                    Stream mass flowrate[kg/h]

                                - schedule : list
                                    Hourly values between 0 and 1, according to the capacity ration on that hour

                                - hourly_generation: list
                                    Stream's hourly capacity [kWh]

                                - capacity : float
                                    Stream's capacity [kW]

                                - fuel : str
                                    Associated equipment fuel name []

                                - eff_equipment : float
                                    Associated equipment efficiency []

    kb : dict
        Knowledge Base data

    Returns
    -------
    all_info : dict
        All conversion data

            - all_sinks_info : list
                Each sink conversion data

                    -sink_group_grid_supply_temperature : float
                       Grid supply temperature [ºC]

                    - sink_group_grid_return_temperature : float
                       Grid return temperature [ºC]

                    - grid_specific : list
                        List with Grid Specific technologies, each technology with the following keys:

                            - teo_equipment_name : str
                                Specific nomenclature for the TEO

                            - output : str
                                Specific nomenclature for the TEO

                            - input_fuel : str
                                Specific nomenclature for the TEO

                            - output_fuel : str
                                Specific nomenclature for the TEO

                            - equipment : list
                                All conversion equipments; list with technologies names; e.g. ['hx_plate', 'heat_pump','hx_plate']

                            - max_capacity : float
                                Stream power (sources- excess heat; sinks - grid heat)  [kW]

                            - turnkey_a : float
                                Aggregated turnkey a [€/kW]

                            - turnkey_b : float
                                Aggregated turnkey b [€]

                            - conversion_efficiency :
                                Aggregated conversion_efficiency []

                            - electrical_conversion_efficiency : float
                                ONLY FOR ORC - electrical conversion efficiency []

                            - om_fix : float
                                Aggregated om_fix [€/year.kW]

                            - om_var : float
                                Aggregated om_var [€/kWh]

                            - emissions : float
                                Aggregated emissions [kg.CO2/kWh]

                            - technologies : list with dicts
                                Each equipment info in detail (check General/Convert_Equipments/Convert_Options)

                    - sinks : list with dict
                        List with each sink data, with the following keys:

                            - sink_id : str
                                Sink ID

                            - location : list
                                [latitude, longitude] [º]

                            - streams : list with dict
                                Each stream of the sink, with the following keys:

                                    - stream_id : str
                                        Stream ID

                                    - demand_fuel : str
                                        TEO specific data

                                    - gis_capacity : float
                                        Sink nominal capacity [kWh]

                                    - hourly_stream_capacity : list
                                        Stream hourly capacity [kWh]

                                    - teo_demand_factor : list
                                        Stream's hourly capacity divided by yearly capacity [kWh]

                                    - teo_yearly_demand : float
                                        Stream yearly demand [kWh]

                                    - conversion_technologies : list
                                        List with multiple dictionaries with the solution of technologies possible to
                                        implement; same keys as the "grid_specific" technologies

            - n_demand_list : list with dicts
                Sinks data for GIS, with the following keys:

                - id : str
                    Object ID

                - coords : list
                    [latitude, longitude] [º]

                - cap : float
                    Object nominal capacity [kW]

            - n_grid_specific : list with dicts
                Grid specific data for GIS, with the following keys:

                    - id : int
                        Object ID

                    - coords : list
                        Same keys as "n_demand_list"

                    - cap : float
                        Same keys as "n_demand_list"

            - n_thermal_storage : list with dicts
                Thermal storage data for GIS; Same keys as "n_grid_specific"

            - teo_demand_factor_group : list
                Every hour of the year with dicts in each hour with TEO Sink ID and corresponding
                hourly_capacity/yearly_capacity; e.g. [{"sink1":0.5,"sink2":0,...},{{"sink1":0.6,"sink2":0,...},...]

    """
    ##################################################################################################################
    # INPUT
    platform_data = PlatformConvertSinks(**in_var['platform'])

    grid_supply_temperature = platform_data.grid_supply_temperature
    grid_return_temperature = platform_data.grid_return_temperature

    group_of_sinks = platform_data.group_of_sinks  # e.g. building, greenhouse, streams
    group_of_sinks = [vars(sink) for sink in group_of_sinks]

    for sink in group_of_sinks:
        sink["fuels_data"] = vars(sink["fuels_data"])
        for fuel in sink["fuels_data"].keys():
            sink["fuels_data"][fuel] = vars(sink["fuels_data"][fuel])

    for sink in group_of_sinks:
        sink['streams'] = [vars(stream) for stream in sink['streams']]

    ##################################################################################################################
    # Initialize array
    output_sink = []
    vector_sink_max_target_temperature = []
    vector_sink_max_supply_temperature = []
    grid_specific_heating = []
    boiler_fuel_type = ['electricity','natural_gas', 'fuel_oil', 'biomass']  # types of fuel
    fuels_teo_nomenclature = {'natural_gas': 'ng', 'fuel_oil': 'oil', 'biomass': 'bio', 'electricity': 'el'}

    ##################################################################################################################
    # Defined vars
    ambient_temperature = 15
    minimum_coef_solar_thermal = 0.5  # solar thermal has to provide at least 50% of streams demand to be considered for TEO

    # Grid Characteristics
    grid_fluid = 'water'
    hot_grid_delta_T = 30  # defined minimum grid delta_T
    max_grid_temperature = 110

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

    for sink_index, sink in enumerate(group_of_sinks):
        for stream_index, stream in enumerate(sink['streams']):
            hourly_stream_capacity = stream['hourly_generation']
            break
        break

    teo_group_of_sinks_demand_factor = list({} for i in range(len(hourly_stream_capacity)))

    ############################################################
    # get grid temperature according to max sink target temperature
    if grid_supply_temperature is None and grid_supply_temperature is None:
        for sink in group_of_sinks:
            for stream in sink['streams']:
                if stream['stream_type'] == 'inflow':
                    vector_sink_max_target_temperature.append(stream['target_temperature'])
                    vector_sink_max_supply_temperature.append(stream['supply_temperature'])

                grid_supply_temperature = max(vector_sink_max_target_temperature) + hx_delta_T
                grid_return_temperature = max(vector_sink_max_supply_temperature) + hx_delta_T

                # check if grid delta_T is respected
                if grid_supply_temperature - grid_return_temperature < hot_grid_delta_T:
                    grid_supply_temperature = grid_return_temperature + hot_grid_delta_T

                if grid_supply_temperature > max_grid_temperature:
                    grid_supply_temperature = max_grid_temperature
                    grid_return_temperature = max_grid_temperature - hot_grid_delta_T


    ######################################
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

    # assume average value of fuel cost/co2 emissions of the sinks for the grid specific
    grid_specific_fuels_data = copy.deepcopy((group_of_sinks[0]['fuels_data']))

    for fuels_keys in grid_specific_fuels_data.keys():
        for fuel_key in grid_specific_fuels_data[fuels_keys].keys():
            grid_specific_fuels_data[fuels_keys][fuel_key] = 0


    fuels_keys = group_of_sinks[0]['fuels_data'].keys() # fuels names
    for sink in group_of_sinks:
        for fuel_key in fuels_keys:
            grid_specific_fuels_data[fuel_key]["price"] += sink['fuels_data'][fuel_key]["price"] * (1/len(group_of_sinks))
            grid_specific_fuels_data[fuel_key]["co2_emissions"] += sink['fuels_data'][fuel_key]["co2_emissions"] * (1/len(group_of_sinks))


    if group_of_sinks_grid_specific_power_heating > 0:
        try:
            # add boiler
            for fuel in boiler_fuel_type:
                info_technology_group = Add_Boiler(kb,
                                                   grid_specific_fuels_data,
                                                   fuel,
                                                   group_of_sinks_grid_specific_power_heating,
                                                   power_fraction,
                                                   grid_supply_temperature,
                                                   grid_return_temperature)

                teo_equipment_name = fuels_teo_nomenclature[info_technology_group.fuel_type] + '_boiler'
                info = aggregate_technologies_info('grid_specific',
                                              [info_technology_group],
                                              power_fraction,
                                              info_technology_group.data_teo['max_input_capacity'],
                                              group_of_sinks_grid_specific_power_heating,
                                              'sink',
                                              teo_equipment_name,
                                              'grid_specific')

                grid_specific_heating.append(info)

            # add heat pump
            info_technology_group_hp = Add_Heat_Pump(kb,
                                                     grid_specific_fuels_data,
                                                     power_fraction,
                                                     grid_supply_temperature,
                                                     grid_return_temperature,
                                                     ambient_temperature,
                                                     supply_capacity=group_of_sinks_grid_specific_power_heating)

            teo_equipment_name = 'hp'
            info = aggregate_technologies_info('grid_specific',
                                          [info_technology_group_hp],
                                          power_fraction,
                                          info_technology_group_hp.data_teo['max_input_capacity'],
                                          group_of_sinks_grid_specific_power_heating,
                                          'sink',
                                          teo_equipment_name,
                                          'grid_specific')

            grid_specific_heating.append(info)

            # add solar thermal + hp
            info_technology_group_solar_thermal = Add_Solar_Thermal(kb,
                                                                    grid_specific_fuels_data,
                                                                    group_latitude,
                                                                    group_longitude,
                                                                    group_of_sinks_grid_specific_power_heating,
                                                                    power_fraction,
                                                                    grid_supply_temperature,
                                                                    grid_return_temperature,
                                                                    hx_delta_T,
                                                                    hx_efficiency)

            teo_equipment_name = 'st_' + 'hp'
            coef_solar_thermal, info_technology_group_hp = coef_solar_thermal_backup(group_of_sinks_grid_specific_hourly_capacity, info_technology_group_solar_thermal, info_technology_group_hp)

            info = aggregate_technologies_info('grid_specific',
                                          [info_technology_group_solar_thermal,
                                           info_technology_group_hp],
                                          power_fraction,
                                          group_of_sinks_grid_specific_power_heating,
                                          group_of_sinks_grid_specific_power_heating,
                                          'sink',
                                          teo_equipment_name,
                                          'grid_specific')  # overall conversion efficiency will be 1

            if coef_solar_thermal >= minimum_coef_solar_thermal:
                info['hourly_supply_capacity_normalize'] = info_technology_group_solar_thermal.data_teo['hourly_supply_capacity_normalize']
                grid_specific_heating.append(info)

        except:
            raise ModuleRuntimeException(
                code="1",
                type="convert_sinks.py",
                msg="Designing heating grid specific technologies is infeasible. Report to the platform."
            )

    ######################################
    # convert each stream
    try:
       for sink in group_of_sinks:
        output_converted = []
        latitude, longitude = sink['location']
        fuels_data = sink['fuels_data']

        # get conversion technologies for each stream
        for stream in sink['streams']:
            conversion_technologies = []
            hourly_stream_capacity = stream['hourly_generation']  # [kWh]
            stream_nominal_capacity = max(hourly_stream_capacity)  # [kW]

            if stream['stream_type'] == 'inflow':

                # get heating technologies
                if stream['target_temperature'] > stream['supply_temperature']:

                    # vapour is needed - only heat pump is designed
                    if stream['target_temperature'] > 100 - hx_delta_T:
                        teo_equipment_name = 'hp'

                        info_technology = Add_Heat_Pump(kb,
                                                        fuels_data,
                                                        power_fraction,
                                                        stream['target_temperature'],
                                                        stream['supply_temperature'],
                                                        grid_return_temperature,
                                                        supply_capacity=stream_nominal_capacity)

                        power_from_grid = info_technology.evap_capacity

                        info_pump_grid = Add_Pump(kb,
                                                  fuels_data,
                                                  grid_fluid,
                                                  power_from_grid,
                                                  power_fraction,
                                                  grid_supply_temperature,
                                                  grid_return_temperature)

                        info = aggregate_technologies_info(sink['id'],
                                                      [info_pump_grid, info_technology],
                                                      power_fraction,
                                                      info_pump_grid.supply_capacity,
                                                      stream_nominal_capacity,
                                                      'sink',
                                                      teo_equipment_name,
                                                      stream['id'])

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

                        info_hx_grid = Add_HX(kb,
                                              hx_grid_supply_temperature,
                                              hx_grid_return_temperature,
                                              grid_fluid,
                                              hx_sink_target_temperature,
                                              hx_sink_supply_temperature,
                                              stream['fluid'],
                                              hx_power,
                                              power_fraction)

                        # add circulation pumping to grid
                        info_pump_grid = Add_Pump(kb,
                                                  fuels_data,
                                                  grid_fluid,
                                                  hx_power,
                                                  power_fraction,
                                                  hx_grid_supply_temperature,
                                                  hx_grid_return_temperature)

                        # grid may not supply enough heat to the sink
                        needed_supply_capacity = stream_nominal_capacity - hx_power_supply  # [kW]

                        # only HX needed
                        if stream['target_temperature'] == hx_sink_target_temperature:
                            teo_equipment_name = 'shex'

                            info = aggregate_technologies_info(sink['id'],
                                                          [info_hx_grid, info_pump_grid],
                                                          power_fraction,
                                                          info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity,
                                                          'sink',
                                                          teo_equipment_name,
                                                          stream['id'])

                            conversion_technologies.append(info)

                        # add boosting technologies
                        elif stream['target_temperature'] > hx_sink_target_temperature:
                            # 1) add boiler
                            for fuel in boiler_fuel_type:
                                info_technology = Add_Boiler(kb,
                                                             fuels_data,
                                                             fuel,
                                                             needed_supply_capacity,
                                                             power_fraction,
                                                             stream['target_temperature'],
                                                             hx_sink_target_temperature)

                                teo_equipment_name = fuels_teo_nomenclature[info_technology.fuel_type] + '_boiler'

                                info = aggregate_technologies_info(sink['id'],
                                                              [info_hx_grid, info_pump_grid, info_technology],
                                                              power_fraction,
                                                              info_pump_grid.supply_capacity,
                                                              stream_nominal_capacity,
                                                              'sink',
                                                              teo_equipment_name,
                                                              stream['id'])

                                conversion_technologies.append(info)

                            # 2) add solar thermal + boiler as backup
                            info_technology_solar_thermal = Add_Solar_Thermal(kb,
                                                                              fuels_data,
                                                                              latitude,
                                                                              longitude,
                                                                              needed_supply_capacity,
                                                                              power_fraction,
                                                                              stream['target_temperature'],
                                                                              hx_sink_target_temperature,
                                                                              hx_delta_T,
                                                                              hx_efficiency)

                            info_technology_boiler = Add_Boiler(kb,
                                                                fuels_data,
                                                                'natural_gas',
                                                                needed_supply_capacity,
                                                                power_fraction,
                                                                stream['target_temperature'],
                                                                hx_sink_target_temperature)

                            teo_equipment_name = 'st_' + fuels_teo_nomenclature[
                                info_technology_boiler.fuel_type] + '_boiler'

                            coef_solar_thermal, info_technology_boiler = coef_solar_thermal_backup(
                                stream['hourly_generation'], info_technology_solar_thermal, info_technology_boiler)

                            info = aggregate_technologies_info(sink['id'],
                                                          [info_hx_grid, info_pump_grid,
                                                           info_technology_solar_thermal, info_technology_boiler],
                                                          power_fraction,
                                                          info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity,
                                                          'sink',
                                                          teo_equipment_name,
                                                          stream['id'])

                            conversion_technologies.append(info)

                            # 3) add solar thermal + heat pump as backup
                            info_technology_heat_pump = Add_Heat_Pump(kb,
                                                                      fuels_data,
                                                                      power_fraction,
                                                                      stream['target_temperature'],
                                                                      hx_sink_target_temperature,
                                                                      ambient_temperature,
                                                                      supply_capacity=needed_supply_capacity)

                            teo_equipment_name = 'st_' + 'hp'

                            coef_solar_thermal, info_technology_heat_pump = coef_solar_thermal_backup(
                                stream['hourly_generation'],
                                info_technology_solar_thermal,
                                info_technology_heat_pump)

                            info = aggregate_technologies_info(sink['id'],
                                                          [info_hx_grid, info_pump_grid,
                                                           info_technology_solar_thermal,
                                                           info_technology_heat_pump],
                                                          power_fraction,
                                                          info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity,
                                                          'sink',
                                                          teo_equipment_name,
                                                          stream['id'])

                            # add solar thermal profile
                            if coef_solar_thermal >= minimum_coef_solar_thermal:
                                info['hourly_supply_capacity_normalize'] = info_technology_solar_thermal.data_teo[
                                    'hourly_supply_capacity_normalize']

                                conversion_technologies.append(info)

                            # 4) add Heat Pump
                            info_technology = Add_Heat_Pump(kb,
                                                            fuels_data,
                                                            power_fraction,
                                                            stream["target_temperature"],
                                                            stream["supply_temperature"],
                                                            grid_return_temperature,
                                                            supply_capacity=stream_nominal_capacity)
                            teo_equipment_name = 'hp'

                            # heat pump circulation pumping to grid
                            info_pump_grid = Add_Pump(kb,
                                                      fuels_data,
                                                      grid_fluid,
                                                      info_technology.evap_capacity,
                                                      power_fraction,
                                                      hx_grid_supply_temperature,
                                                      hx_grid_return_temperature)

                            info = aggregate_technologies_info(sink['id'],
                                                          [info_pump_grid, info_technology],
                                                          power_fraction,
                                                          info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity,
                                                          'sink',
                                                          teo_equipment_name,
                                                          stream['id'])

                            conversion_technologies.append(info)


                # get cooling technologies
                else:
                    if grid_supply_temperature < thermal_chiller_generator_T_hot:
                        after_hx_global_conversion_efficiency = boiler_efficiency * thermal_chiller_efficiency
                    else:
                        after_hx_global_conversion_efficiency = thermal_chiller_efficiency

                    # add electric chiller IF stream target temperature inferior to absorption chiller supply temperature
                    if stream['target_temperature'] < thermal_chiller_supply_temperature:
                        electric_chiller_supply_capacity = stream_nominal_capacity * (
                                thermal_chiller_supply_temperature - stream['target_temperature']) / (
                                                                   stream['supply_temperature'] - stream[
                                                               'target_temperature'])

                        thermal_chiller_supply_capacity = stream_nominal_capacity - electric_chiller_supply_capacity

                        info_electric_chiller = Add_Electric_Chiller(kb,
                                                                     fuels_data,
                                                                     electric_chiller_supply_capacity,
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

                    info_hx_grid = Add_HX(kb,
                                          hx_grid_supply_temperature,
                                          hx_grid_return_temperature,
                                          grid_fluid,
                                          hx_sink_target_temperature,
                                          hx_sink_supply_temperature,
                                          stream['fluid'],
                                          hx_power,
                                          power_fraction)

                    # add circulation pumping to grid
                    info_pump_grid = Add_Pump(kb,
                                              fuels_data,
                                              grid_fluid,
                                              hx_power_supply,
                                              power_fraction,
                                              hx_sink_target_temperature,
                                              hx_sink_supply_temperature)

                    # grid may not supply enough heat to the sink
                    needed_supply_capacity = stream_nominal_capacity / after_hx_global_conversion_efficiency - hx_power_supply  # [kW]

                    # add absorption chiller
                    info_technology = Add_Thermal_Chiller(kb,
                                                          fuels_data,
                                                          thermal_chiller_supply_capacity,
                                                          power_fraction)

                    # absorption chiller evaporation temperature not reached by the grid - put booster technology before
                    if hx_sink_target_temperature < thermal_chiller_generator_T_hot:
                        # add boiler
                        for fuel in boiler_fuel_type:
                            info_boiler = Add_Boiler(kb,
                                                     fuels_data,
                                                     fuel,
                                                     needed_supply_capacity,
                                                     power_fraction,
                                                     thermal_chiller_generator_T_hot,
                                                     hx_sink_target_temperature)

                            if info_electric_chiller == []:
                                teo_equipment_name = 'ac_' + fuels_teo_nomenclature[
                                    info_boiler.fuel_type] + '_boiler'
                                info = aggregate_technologies_info(sink['id'],
                                                              [info_hx_grid, info_pump_grid, info_boiler,
                                                               info_technology],
                                                              power_fraction,
                                                              info_pump_grid.supply_capacity,
                                                              stream_nominal_capacity,
                                                              'sink',
                                                              teo_equipment_name,
                                                              stream['id'])
                            else:
                                teo_equipment_name = 'ac_ec_' + fuels_teo_nomenclature[
                                    info_boiler.fuel_type] + '_boiler'

                                info = aggregate_technologies_info(sink['id'],
                                                              [info_hx_grid, info_pump_grid, info_boiler,
                                                               info_technology, info_electric_chiller],
                                                              power_fraction,
                                                              info_pump_grid.supply_capacity,
                                                              stream_nominal_capacity,
                                                              'sink',
                                                              teo_equipment_name,
                                                              stream['id'])

                            conversion_technologies.append(info)

                        # add heat pump
                        info_heat_pump = Add_Heat_Pump(kb,
                                                       fuels_data,
                                                       needed_supply_capacity,
                                                       power_fraction,
                                                       thermal_chiller_generator_T_hot,
                                                       hx_sink_target_temperature,
                                                       ambient_temperature)

                        if info_electric_chiller == []:
                            teo_equipment_name = 'ac_' + 'hp'
                            info = aggregate_technologies_info(sink['id'],
                                                          [info_hx_grid, info_pump_grid, info_heat_pump,
                                                           info_technology],
                                                          power_fraction,
                                                          info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity,
                                                          'sink',
                                                          teo_equipment_name,
                                                          stream['id'])
                        else:
                            teo_equipment_name = 'ac_ec_' + 'hp'
                            info = aggregate_technologies_info(sink['id'],
                                                          [info_hx_grid, info_pump_grid, info_heat_pump,
                                                           info_technology, info_electric_chiller],
                                                          power_fraction,
                                                          info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity,
                                                          'sink',
                                                          teo_equipment_name,
                                                          stream['id'])

                        conversion_technologies.append(info)

                    else:
                        if info_electric_chiller == []:
                            teo_equipment_name = 'ac'

                            info = aggregate_technologies_info(sink['id'],
                                                          [info_hx_grid, info_pump_grid, info_technology],
                                                          power_fraction,
                                                          info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity,
                                                          'sink',
                                                          teo_equipment_name,
                                                          stream['id'])
                        else:
                            teo_equipment_name = 'ac_ec'
                            info = aggregate_technologies_info(sink['id'],
                                                          [info_hx_grid, info_pump_grid, info_electric_chiller,
                                                           info_technology],
                                                          power_fraction,
                                                          info_pump_grid.supply_capacity,
                                                          stream_nominal_capacity,
                                                          'sink',
                                                          teo_equipment_name,
                                                          stream['id'])

                        conversion_technologies.append(info)

            yearly_demand = sum(hourly_stream_capacity)
            teo_demand_factor = [float(i / yearly_demand) for i in hourly_stream_capacity]


            gis_capacity = conversion_technologies[0]['max_capacity']
            teo_id = 'sink' + str(sink['id']) + 'str' + str(stream['id']) + 'dem' # 'sink' + str(sink['id']) + 'stream' + str(stream['id'])

            output_converted.append({
                'stream_id': stream['id'],
                'demand_fuel': teo_id,
                'gis_capacity': gis_capacity,  # [kW]
                'hourly_stream_capacity': hourly_stream_capacity,  # [kWh]
                'teo_demand_factor': teo_demand_factor,
                'teo_yearly_demand': yearly_demand,
                'conversion_technologies': conversion_technologies,  # [€/kW]
            })

            for index, i in enumerate(teo_group_of_sinks_demand_factor):
                i[teo_id] = teo_demand_factor[index]

        output_sink.append({
            'sink_id': sink['id'],
            'location': [latitude, longitude],
            'streams': output_converted
        })

    except:
        raise ModuleRuntimeException(
            code="2",
            type="convert_sinks.py",
            msg="Sinks' streams conversion infeasible. Check sinks' streams."
        )

    ##############################
    # OUTPUT
    all_sinks_info = {
        'sink_group_grid_supply_temperature': grid_supply_temperature,
        'sink_group_grid_return_temperature': grid_return_temperature,
        'grid_specific': grid_specific_heating,
        'sinks': output_sink
    }

    # GIS INFO
    n_demand_list = []
    for sink in all_sinks_info['sinks']:
        total_cap = 0
        for stream in sink['streams']:
            total_cap = total_cap + stream['gis_capacity']

        gis_dict = {
            'id': sink['sink_id'],
            'coords': sink['location'],
            'cap': total_cap  # [kW]
        }

        n_demand_list.append(gis_dict)

    n_grid_specific = [{
        'id': 0,
        'coords': [group_latitude, group_longitude],
        'cap': group_of_sinks_grid_specific_power_heating  # [kW]
    }]

    n_thermal_storage = [{
        'id': -1,
        'coords': [group_latitude, group_longitude],
        'cap': 1  # [kW]
    },
        {
            'id': -2,
            'coords': [group_latitude, group_longitude],
            'cap': 1  # [kW]
        }
    ]



    all_info = {
        "all_sinks_info": all_sinks_info,
        "n_grid_specific": n_grid_specific,
        "n_demand_list": n_demand_list,
        "n_thermal_storage": n_thermal_storage,
        "teo_demand_factor_group": teo_group_of_sinks_demand_factor
    }

    return all_info
