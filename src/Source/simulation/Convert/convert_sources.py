from copy import copy
from ....General.Convert_Equipments.Auxiliary.source_get_hx_temperatures import source_get_hx_temperatures
from ....General.Convert_Equipments.Convert_Options.add_boiler import Add_Boiler
from ....General.Convert_Equipments.Convert_Options.add_hx import Add_HX
from ....General.Convert_Equipments.Convert_Options.add_solar_thermal import Add_Solar_Thermal
from ....General.Convert_Equipments.Convert_Options.add_heat_pump import Add_Heat_Pump
from ....General.Convert_Equipments.Convert_Options.add_chp import Add_CHP
from ....General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from ....General.Convert_Equipments.Convert_Options.add_orc_cascaded import Add_ORC_Cascaded
from ....General.Convert_Equipments.Auxiliary.aggregate_technologies_info import aggregate_technologies_info
from ....Source.simulation.Auxiliary.design_orc import design_orc
from ....General.Convert_Equipments.Auxiliary.coef_solar_thermal_backup import coef_solar_thermal_backup
from ....Error_Handling.error_convert_sources import MainErrorConvertSources
from ....Error_Handling.runtime_error import ModuleRuntimeException

def convert_sources(in_var, kb):
    """Sources conversion to the grid - design of technologies.

    For each source are designed the conversion technologies needed. The design may be done for each stream individually
    or it can be made to the aggregated of streams (the user must provide his preference). After the designing, it is
    known the power available from each source.
    When performing the conversion, three design options may occur:
            1. If the stream supply temperature > grid supply temperature -> HX designed
            2. If the stream supply temperature > ORC evaporator -> ORC cascaded designed
            3. If the stream supply temperature < grid supply temperature -> heating technologies are designed

    Parameters
    ----------
    in_var : dict
        platform and CF module data, with the following keys:

            - platform: dict
                Platform data, with the following keys:

                    - existing_grid_data: list with dict [OPTIONAL]
                        Existent grid connection point data, with the following keys:

                            - id: int
                                Existent source or grid connection point ID

                            - location: list
                                Location [º]; [latitude,longitude]

                            - levelized_co2_emissions: float
                                Grid levelized CO2 emissions [c]

                            - levelized_om_var: float
                                Grid levelized OM var [€/kWh]

                            - levelized_om_fix: float
                                Grid levelized OM fix  [€/kWh]

                    - group_of_sources: list with dict
                        Sources to be analyzed. Each source with the following keys:

                            - id: int:
                                Source ID

                            - location: list
                                Location [º]; [latitude,longitude]

                            - fuels_data: dict
                                Fuels price and CO2 emission, with the following keys:

                                    - natural_gas: dict
                                        with the following keys:

                                        - co2_emissions: float:
                                            Fuel CO2 emission [kg CO2/kWh]

                                        - price: float:
                                            Fuel price [€/kWh]

                                    - fuel_oil : dict
                                        Similar to "natural_gas"

                                    - electricity : dict
                                        Similar to "natural_gas"

                                    - biomass : dict
                                        Similar to "natural_gas"

                            - streams: list with dict
                                Source's streams to be analyzed. Each stream with the following keys:

                                    - stream_id: int
                                        Stream ID []

                                    - object_type: str
                                        DEFAULT=stream []

                                    - stream_type: str
                                        Stream designation []; inflow, outflow, excess_heat

                                    - fluid: str
                                        Stream's fluid []

                                    - capacity: float
                                        Stream's capacity [kW]

                                    - supply_temperature: float
                                        Stream's supply/initial temperature [ºC]

                                    - target_temperature: float
                                        Stream's target/final temperature [ºC]

                                    - hourly_generation: list
                                        Stream's hourly capacity [kWh]

                - cf_module: dict
                    CF module data, with the following keys:

                        - sink_group_grid_supply_temperature: float
                            Grid supply temperature (user input or defined by the "convert_sinks") [ºC]

                        - sink_group_grid_return_temperature: float
                            Grid return temperature (user input or defined by the "convert_sinks") [ºC]

    kb :dict
        Knowledge Base data

    Returns
    -------
    all_info: dict:
        Sources conversion data, with the following keys:

            - all_sources_info: list
                Sources dicts to be analyzed. Each source with the following keys:

                    - source_id: int:
                        Source ID

                    - location: list:
                        Location [º]; [latitude,longitude]

                    - source_grid_supply_temperature: float
                        Source-grid supply temperature [ºC]

                    - source_grid_return_temperature: float
                        Source-grid return temperature [ºC]

                    - streams_converted : list
                        Streams conversion data dicts, with the following keys:

                            - stream_id: int
                                Stream ID

                            - teo_stream_id: str
                                TEO specific data; stream ID with source ID []

                            - input_fuel: str
                                TEO specific data; TEO input fuel name []

                            - output_fuel: str
                                TEO specific data; TEO output fuel name  []

                            - output: int
                                TEO specific data; DEFAULT=1 []

                            - gis_capacity: float
                                GIS specific data; stream converted/provided capacity to the grid

                            - hourly_stream_capacity: list
                                Hourly stream capacity [kWh]

                            - teo_capacity_factor: list
                                TEO specific data

                            - max_stream_capacity: float
                                Max stream capacity [kW]

                            - conversion_technologies: list
                                Conversion solution data dicts (technologies implemented), with the following keys:

                                    - teo_equipment_name: str
                                        TEO specific data; TEO equipment name []

                                    - output: int
                                        TEO specific data; DEFAULT=1 []

                                    - input_fuel: str
                                        TEO specific data; TEO input fuel name []

                                    - output_fuel: str
                                        TEO specific data; TEO output fuel name  []

                                    - equipment: list
                                        Conversion solution equipment names []

                                    - max_capacity: float
                                        Stream capacity maximum capacity convertible  [kW]

                                    - turnkey_a: float
                                        Conversion solution turnkey a (ax+b)  [€/kW]

                                    - turnkey_b: float
                                        Conversion solution turnkey b (ax+b) [€]

                                    - conversion_efficiency: float
                                        Conversion solution efficiency stream-to-grid []

                                    - om_fix: float
                                        Conversion solution OM fix [€/year.kW]

                                    - om_var: float
                                        Conversion solution OM var [€/kWh]

                                    - emissions: float
                                        Conversion solution CO2 emissions [kg.CO2/kWh]

                                    - technologies: list
                                        Each technologies info in detail dicts (check each technology routine for more details)

            - ex_grid: dict, list
                TEO specific data; existent grid data

                    - teo_equipment_name: str
                        DEFAULT="ex_grid"

                    - output: int
                        DEFAULT=1

                    - input_fuel: None
                        DEFAULT=None

                    - output_fuel: str
                        DEFAULT="dhnwatersupply"

                    - equipment: list
                        DEFAULT=[]

                    - max_capacity: float
                        DEFAULT=10**8

                    - turnkey_a: float
                        DEFAULT=0

                    - turnkey_b: float
                        DEFAULT=0

                    - conversion_efficiency: float
                        DEFAULT=1

                    - om_fix: int
                        Levelized OM Var [€/year]

                    - om_var: int
                        Levelized OM Var [€/kWh]

                    - emissions: float
                        Levelized CO2 emissions [kgCO2/kWh]

                    - technologies: list
                        DEFAULT=[]

            - teo_string: str
                TEO specific data. DEFAULT="dhn"

            - input_fuel: str
                TEO specific data. DEFAULT="dhnwatersupply"

            - output_fuel: str
                TEO specific data. DEFAULT="dhnwaterdem"

            - output: int
                TEO specific data. DEFAULT=1

            - input: int
                TEO specific data. DEFAULT=1

            - n_supply_list: list
                GIS specific data. Sources location and capacity provided to the grid

            - teo_capacity_factor_group: int
                TEO specific data

            - teo_dhn: dict
                TEO specific data. Parameters TEO

    """

    ############################################################################################################
    # INPUT
    # error handling
    MainErrorConvertSources(**in_var)

    group_of_sources = in_var['platform']['group_of_sources']
    sink_group_grid_supply_temperature = in_var['cf_module']['sink_group_grid_supply_temperature']
    sink_group_grid_return_temperature = in_var['cf_module']['sink_group_grid_return_temperature']

    try:
        existing_grid_data = in_var['platform']['existing_grid_data']
    except:
        existing_grid_data = None


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
    fuels_teo_nomenclature = {'natural_gas': 'ng', 'fuel_oil': 'oil', 'biomass': 'bio', 'electricity': 'el'}

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
            fuels_data = source['fuels_data']

            # get conversion technologies for each stream
            for stream_index, stream in enumerate(source['streams']):
                conversion_technologies = []
                source_grid_supply_temperature = sink_group_grid_supply_temperature + delta_T_buffer
                source_grid_return_temperature = sink_group_grid_return_temperature - delta_T_buffer

                # only convert sources where grid supply temperature is inferior to max_grid_temperature
                if source_grid_supply_temperature <= max_grid_temperature:

                    if stream['stream_type'] == 'excess_heat' or stream['stream_type'] == 'outflow':
                        hourly_stream_capacity = stream['hourly_generation']
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
                            if stream['supply_temperature'] >= hx_source_supply_temperature + hx_delta_T * hx_number:

                                #  check if intermediate circuit is needed
                                if intermediate_circuit == True:
                                    # get intermediate circuit temperatures
                                    hx_intermediate_supply_temperature = source_grid_supply_temperature + hx_delta_T
                                    hx_intermediate_return_temperature = source_grid_return_temperature + hx_delta_T

                                    # add HX intermediate
                                    hx_intermediate_supply_temperature, hx_intermediate_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(
                                        hx_intermediate_supply_temperature, hx_intermediate_return_temperature,
                                        stream['supply_temperature'], stream['target_temperature'], hx_delta_T)
                                    hx_power = stream_nominal_capacity * (
                                            abs(hx_stream_supply_temperature - hx_stream_target_temperature) / abs(
                                        stream['supply_temperature'] - stream['target_temperature']))

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
                                                                      fuels_data,
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
                                                              fuels_data,
                                                              grid_fluid,
                                                              info_hx_grid.available_power,
                                                              power_fraction,
                                                              source_grid_supply_temperature,
                                                              source_grid_return_temperature)

                                    teo_equipment_name = 'mhex'
                                    info = aggregate_technologies_info(source['id'],
                                                                       [info_hx_intermediate,
                                                                        info_pump_intermediate, info_hx_grid,
                                                                        info_pump_grid],
                                                                       power_fraction,
                                                                       stream_available_capacity,
                                                                       info_pump_grid.supply_capacity,
                                                                       'sou',
                                                                       teo_equipment_name,
                                                                       stream['id'])

                                    conversion_technologies.append(info)

                                else:
                                    # add HX to grid
                                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(
                                        source_grid_supply_temperature, source_grid_return_temperature,
                                        stream['supply_temperature'], stream['target_temperature'], hx_delta_T)
                                    hx_power = stream_nominal_capacity / (
                                        abs(stream['target_temperature'] - stream['supply_temperature'])) * abs(
                                        hx_stream_supply_temperature - hx_stream_target_temperature)

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
                                                              fuels_data,
                                                              grid_fluid,
                                                              info_hx_grid.available_power,
                                                              power_fraction,
                                                              hx_grid_supply_temperature,
                                                              hx_grid_return_temperature)

                                    teo_equipment_name = 'shex'

                                    info = aggregate_technologies_info(source['id'],
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
                                orc_type, stream_available_capacity, orc_electrical_generation, overall_thermal_capacity, hx_stream_target_temperature, intermediate_circuit, hx_intermediate_supply_temperature, hx_intermediate_return_temperature = design_orc(
                                    stream['capacity'], stream['fluid'], stream['supply_temperature'],
                                    stream['target_temperature'], hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,
                                    aggregate_streams=False)

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
                                                                          fuels_data,
                                                                          orc_intermediate_fluid,
                                                                          info_hx_intermediate.available_power,
                                                                          power_fraction,
                                                                          hx_intermediate_supply_temperature,
                                                                          hx_intermediate_return_temperature)

                                    info_pump_grid = Add_Pump(kb,
                                                              fuels_data,
                                                              grid_fluid,
                                                              info_technology.supply_capacity,
                                                              power_fraction,
                                                              source_grid_supply_temperature,
                                                              source_grid_return_temperature)
                                    teo_equipment_name = 'orc'

                                    if intermediate_circuit == True:
                                        info = aggregate_technologies_info(source['id'],
                                                                           [info_hx_intermediate,
                                                                            info_pump_intermediate,
                                                                            info_technology,
                                                                            info_pump_grid],
                                                                           power_fraction,
                                                                           stream_available_capacity,
                                                                           info_pump_grid.supply_capacity,
                                                                           'sou',
                                                                           teo_equipment_name,
                                                                           stream['id'])
                                    else:
                                        info = aggregate_technologies_info(source['id'],
                                                                           [info_technology, info_pump_grid],
                                                                           power_fraction,
                                                                           stream_available_capacity,
                                                                           info_pump_grid.supply_capacity,
                                                                           'sou',
                                                                           teo_equipment_name,
                                                                           stream['id'])

                                    conversion_technologies.append(info)

                            # heating technologies needed; source cannot meet DHN temperature
                            else:
                                if stream['supply_temperature'] > source_grid_return_temperature + hx_delta_T:
                                    # get heat extra needed to be supplied
                                    booster_outlet_temperature = source_grid_supply_temperature
                                    booster_inlet_temperature = stream['supply_temperature'] - hx_delta_T
                                    needed_supply_capacity = stream['capacity'] * (booster_outlet_temperature - booster_inlet_temperature) / ( stream['supply_temperature'] - stream[ 'target_temperature'])

                                    # get data HX Source-Grid
                                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature, = source_get_hx_temperatures(
                                        booster_inlet_temperature, source_grid_return_temperature,
                                        stream['supply_temperature'], stream['target_temperature'], hx_delta_T)

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

                                    stream_available_capacity = stream_nominal_capacity * (
                                        abs(stream['supply_temperature'] - hx_stream_target_temperature)) / abs(
                                        stream['supply_temperature'] - stream['target_temperature'])

                                    # add circulation pumping to grid
                                    info_pump_grid = Add_Pump(kb,
                                                              fuels_data,
                                                              grid_fluid,
                                                              info_hx_grid.available_power,
                                                              power_fraction,
                                                              booster_inlet_temperature,
                                                              source_grid_return_temperature)

                                    # DESIGN BOOSTING TECHNOLOGIES
                                    # 1) add Boiler
                                    for fuel in boiler_fuel_type:
                                        info_technology = Add_Boiler(kb,
                                                                     fuels_data,
                                                                     fuel,
                                                                     needed_supply_capacity,
                                                                     power_fraction,
                                                                     booster_outlet_temperature,
                                                                     booster_inlet_temperature)

                                        teo_equipment_name = fuels_teo_nomenclature[info_technology.fuel_type] + '_whrb'

                                        info = aggregate_technologies_info(source['id'],
                                                                           [info_technology, info_hx_grid,
                                                                            info_pump_grid],
                                                                           power_fraction,
                                                                           stream_available_capacity,
                                                                           info_pump_grid.supply_capacity + needed_supply_capacity,
                                                                           'sou',
                                                                           teo_equipment_name,
                                                                           stream['id'])

                                        conversion_technologies.append(info)

                                    # 2) add Solar Thermal + Boiler as backup
                                    info_technology_solar_thermal = Add_Solar_Thermal(kb,
                                                                                      fuels_data,
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
                                                                            fuels_data,
                                                                            fuel,
                                                                            needed_supply_capacity,
                                                                            power_fraction,
                                                                            booster_outlet_temperature,
                                                                            booster_inlet_temperature)

                                        teo_equipment_name = 'st_' + fuels_teo_nomenclature[
                                            info_technology_boiler.fuel_type] + '_boiler'

                                        coef_solar_thermal, info_technology_boiler = coef_solar_thermal_backup(
                                            stream['hourly_generation'], info_technology_solar_thermal,
                                            info_technology_boiler)

                                        info = aggregate_technologies_info(source['id'],
                                                                           [info_technology_solar_thermal,
                                                                            info_technology_boiler, info_hx_grid,
                                                                            info_pump_grid],
                                                                           power_fraction,
                                                                           stream_available_capacity,
                                                                           info_pump_grid.supply_capacity + needed_supply_capacity,
                                                                           'sou',
                                                                           teo_equipment_name,
                                                                           stream['id'])

                                        if coef_solar_thermal >= minimum_coef_solar_thermal:
                                            conversion_technologies.append(info)

                                    # 3) add solar thermal + heat pump as backup
                                    teo_equipment_name = 'st_' + 'hp'
                                    info_technology_heat_pump = Add_Heat_Pump(kb,
                                                                              fuels_data,
                                                                              power_fraction,
                                                                              booster_outlet_temperature,
                                                                              booster_inlet_temperature,
                                                                              ambient_temperature,
                                                                              supply_capacity=needed_supply_capacity)

                                    coef_solar_thermal, info_technology_heat_pump = coef_solar_thermal_backup(
                                        stream['hourly_generation'], info_technology_solar_thermal,
                                        info_technology_heat_pump)

                                    info = aggregate_technologies_info(source['id'],
                                                                       [info_technology_solar_thermal,
                                                                        info_technology_heat_pump, info_hx_grid,
                                                                        info_pump_grid],
                                                                       power_fraction,
                                                                       stream_available_capacity,
                                                                       info_pump_grid.supply_capacity + needed_supply_capacity,
                                                                       'sou',
                                                                       teo_equipment_name,
                                                                       stream['id'])

                                    if coef_solar_thermal >= minimum_coef_solar_thermal:
                                        conversion_technologies.append(info)

                                    #4) add chp
                                    for fuel in chp_fuel_type:
                                        info_technology = Add_CHP(kb,
                                                                  fuels_data,
                                                                  fuel,
                                                                  needed_supply_capacity,
                                                                  power_fraction,
                                                                  booster_outlet_temperature,
                                                                  booster_inlet_temperature)

                                        teo_equipment_name = 'chp_' + fuels_teo_nomenclature[
                                            info_technology.fuel_type]

                                        info = aggregate_technologies_info(source['id'],
                                                                           [info_technology, info_hx_grid,
                                                                            info_pump_grid],
                                                                           power_fraction,
                                                                           stream_available_capacity,
                                                                           info_pump_grid.supply_capacity + needed_supply_capacity,
                                                                           'sou',
                                                                           teo_equipment_name,
                                                                           stream['id'])

                                        conversion_technologies.append(info)

                                # add Heat Pump (with intermediate HX between stream and HP)
                                teo_equipment_name = 'hp'
                                heat_pump_T_evap = stream['target_temperature'] - hx_delta_T
                                heat_pump_evap_capacity = stream_nominal_capacity
                                info_technology = Add_Heat_Pump(kb,
                                                                fuels_data,
                                                                power_fraction,
                                                                source_grid_supply_temperature,
                                                                source_grid_return_temperature,
                                                                heat_pump_T_evap,
                                                                evap_capacity=heat_pump_evap_capacity)

                                # add HX to hp
                                hx_hp_supply_temperature = stream['supply_temperature'] - hx_delta_T
                                hx_hp_return_temperature = stream['target_temperature'] - hx_delta_T
                                hx_stream_supply_temperature = stream['supply_temperature']
                                hx_stream_target_temperature= stream['target_temperature']

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
                                                          fuels_data,
                                                          grid_fluid,
                                                          info_technology.supply_capacity,
                                                          power_fraction,
                                                          source_grid_supply_temperature,
                                                          source_grid_return_temperature)

                                info = aggregate_technologies_info(source['id'],
                                                                   [info_hx_pump, info_technology,  info_pump_grid],
                                                                   power_fraction,
                                                                   stream_nominal_capacity,
                                                                   info_pump_grid.supply_capacity,
                                                                   'sou',
                                                                   teo_equipment_name,
                                                                   stream['id'])

                                conversion_technologies.append(info)

                            teo_capacity_factor = [i / max(hourly_stream_capacity) for i in hourly_stream_capacity]
                            gis_capacity = conversion_technologies[0]['max_capacity'] * conversion_technologies[0][
                                'conversion_efficiency']

                            output_converted.append({
                                "stream_id": stream['id'],
                                "teo_stream_id": 'str' + str(stream['id']) + 'sou' + str(source['id']),
                                "input_fuel": None,
                                "output_fuel": "eh" + 'str' + str(stream['id']) + 'sou' + str(source['id']),
                                "output": 1,
                                "gis_capacity": gis_capacity,  # [kW]
                                "hourly_stream_capacity": hourly_stream_capacity,  # [kWh]
                                "teo_capacity_factor": teo_capacity_factor,
                                "max_stream_capacity": max(hourly_stream_capacity),
                                "conversion_technologies": conversion_technologies,  # [€/kW]
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
        "all_sources_info": all_sources_info,
        "ex_grid": ex_grid,
        "teo_string": 'dhn',
        "input_fuel": "dhnwatersupply",
        "output_fuel": "dhnwaterdem",
        "output": 1,
        "input": 1,
        "n_supply_list": n_supply_list,
        "teo_capacity_factor_group": teo_group_of_sources_capacity_factor,
        "teo_dhn": teo_dhn
    }


    return all_info
