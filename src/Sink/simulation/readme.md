# Sink simulation

On the sink simulation submodule, there is 1 main function (convert_sinks), listed below are its inputs and outputs:

## convert_sink function

### INPUT:

group_of_sinks = [sink_1,sink_2,...] each sink with dictionary {sink_id,sink_location,streams}

Where:
1. sink id
1. location = [country, consumer_type,latitude,longitude]
1. consumer_type - 'household' or 'non-household'
1. streams -> vector with dictionaries with {id, object_type, 1. stream_type, fluid, capacity, supply_temperature, target_temperature,hourly_generation}
1. hourly_generation for streams (profile 1 and 0)
1. hourly_generation for building  (kWh profile)

### OUTPUT:

json with multiple dictionaries {'sink_id', 'stream_id', 'hourly_stream_capacity', 'conversion_technologies'}
Where in sinks:

1. sink_id
1. streams

Where in streams:

1. stream_id
1. hourly_stream_capacity [kWh]
1. conversion_technologies - multiple dictionaries with technologies possible to implement
    - 'equipment' - group of equipment installed
    - 'max_capacity'  - conversion maximum designed capacity[kW]
    - 'turnkey_a' - conversion turnkey linear coefficient [€/kW]
    - 'turnkey_b' - conversion turnkey fixed coefficien [€]
    - 'conversion_efficiency' - ratio between grid supply capacity and sink required capacity []
    - 'om_fix' - conversion fixed yearly OM costs / grid supply capacity [€/year.kW]
    - 'om_var' - conversion variable costs (accounting fuel costs) [€/kWh]
    - 'emissions' - conversion direct or indirect CO2 emissions [kg.CO2/kWh]
    - tecnhologies' - technologies info in details,
