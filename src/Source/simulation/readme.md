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
