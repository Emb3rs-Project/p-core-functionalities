The Core Functionalities module will allow a full characterization of the main objects of the EMB3Rs platform and prepare the data for the simulation process by the analysis modules.

For sources, the CF module is divided into 2 submodules: characterization and simulation.
The CF source characterization submodule receives the input data from the user and calculates available excess heat. It has 6 main functions (outflow_simplified, generate_process, generate_boiler, generate_burner generate_cooling_equipment and generate_chp), and 5 auxiliary functions (schedule_hour; T_flue_gas; combustion_mass_flows; compute_flow_rate and stream). These are the main functionalities to analyse user data input for sources.

Whenever a user performs a simulation on the platform, the CF source simulation submodule will retrieve the required data from the platform and calculate the end use. The submodule has 2 main functions (convert_sources and generate_heat_recovery), and 17 auxiliary functions. 

The convert_source funcion will get the group of sources to be converted from the platform.

INPUT: group_of_sources = [source_1,source_2,...] each source with dictionary {source_id,source_location,consumer_type,source_streams}
- source_id
- source_location = (country,latitude,longitude)
- consumer_type - 'household' or 'non-household'
- Source streams - vector with dictionaries with:
  - stream_id
  - object_type
  - stream_type
  - fluid
  - capacity
  - supply_temperature
  - target_temperature
  - hourly_generation

OUTPUT: json with multiple dictionaries ('source_id', 'stream_id', 'hourly_stream_capacity', 'conversion_technologies',..)
Where:
- source_id
- source_grid_supply_temperature
- source_grid_return_temperature
- streams_converted

Where in streams_converted:
- stream_id
- hourly_stream_capacity [kWh/h]
- conversion_technologies - multiple dictionaries with technologies possible to implement
  - 'equipment'
  - 'max_capacity'  [kW]
  - 'turnkey_a' [€/kW]
  - 'turnkey_b' [€]
  - 'conversion_efficiency'  []
  - 'om_fix'   [€/year.kW]
  - 'om_var'  [€/kWh]
  - 'emissions'  [kg.CO2/kWh]

For sinks, the CF module is also divided into 2 submodules, charaterization and simulation.

To characterize sinks, the CF has 3 main functions and 16 auxiliary functions. There is the industry function for simplified users that wish to manually add a heat/cold demand.
The building and greenhouse functions is for users that intend to add a climate dependent heating/cooling demand. The functions will then generate an hourly heating/cooling demand profile for a full year based on climate data and indoor temperature requirements.

On the simulation subgroup, there is 1 main function (convert_sinks), listed below are its inputs and outputs:
 
INPUT: group_of_sinks = [sink_1,sink_2,...] each sink with dictionary {sink_id,sink_location,streams}
Where:
  - sink id
  - location = [country, consumer_type,latitude,longitude]
  - consumer_type - 'household' or 'non-household'
  - streams -> vector with dictionaries with {id, object_type, stream_type, fluid, capacity, supply_temperature, target_temperature,hourly_generation}
  - hourly_generation for streams (profile 1 and 0), hourly_generation for building  (kWh profile)

OUTPUT: json with multiple dictionaries {'sink_id', 'stream_id', 'hourly_stream_capacity', 'conversion_technologies'}
Where in sinks:
- sink_id
- streams

Where in streams:
- stream_id
- hourly_stream_capacity [kWh]
- conversion_technologies - multiple dictionaries with technologies possible to implement
  - 'equipment'
  - 'max_capacity'  [kW]
  - 'turnkey_a' [€/kW]
  - 'turnkey_b' [€]
  - 'conversion_efficiency'  []
  - 'om_fix'   [€/year.kW]
  - 'om_var'  [€/kWh]
  - 'emissions'  [kg.CO2/kWh]

