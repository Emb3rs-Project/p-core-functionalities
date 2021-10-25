The Core Functionalities module will allow a full characterization of the main objects of the EMB3Rs platform and prepare the data for the simulation process by the analysis modules.

For sources, the CF module is divided into 2 submodules: characterization and simulation.
The CF source characterization submodule receives the input data from the user and calculates available excess heat. It has 6 main functions (outflow_simplified, generate_process, generate_boiler, generate_burner generate_cooling_equipment and generate_chp), and 5 auxiliary functions (schedule_hour; T_flue_gas; combustion_mass_flows; compute_flow_rate and stream). These are the main functionalities to analyse user data input for sources.

Whenever a user performs a simulation on the platform, the CF source simulation submodule will retrieve the required data from the platform and calculate the end use. The submodule has 2 main functions (convert_sources and generate_heat_recovery), and 17 auxiliary functions (as presented in figure 2.1.2 in yellow). The convert_source funcion will get the group of sources to be converted from the platform, their main attributes are:
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

OUTPUT: vector with multiple dictionaries ('source_id', 'stream_id', 'hourly_stream_capacity', 'conversion_technologies',..)
      Where:
        -  source_id
        -  source_grid_supply_temperature
        -  source_grid_return_temperature
        - streams_converted

            Where in streams_converted:
            - stream_id
            - hourly_stream_capacity [kWh]
            - conversion_technologies - multiple dictionaries with technologies possible to implement
              Important:
                conversion_technologies =
                 - 'equipment'
                 - 'max_capacity'  [kW]
                 - 'turnkey_a' [€/kW]
                 - 'turnkey_b' [€]
                 - 'conversion_efficiency'  []
                 - 'om_fix'   [€/year.kW]
                 - 'om_var'  [€/kWh]
                 - 'emissions'  [kg.CO2/kWh]



