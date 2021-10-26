# Characterization of user-defined sinks (industrial)

There is one function to characterize industrial sinks or user-defined streams, the industry function.

## Industry function

The function reads user input data and computes the related stream in json format.

### INPUT
1. sink_id = sink_id
1. stream_type = 'inflow'
1. supply_temperature = stream supply temperature (ºC)
1. target_temperature = stream target temperature (ºC)
1. fluid = stream fluid (list)
1. flowrate = stream flowrate (kg/h)
1. schedule
    - saturday_on = if it operates saturday (0/1)
    - sunday_on = if it operates sunday (0/1)
    - shutdown_periods = yearly shutdown periods (d)
    - daily_periods = daily operating periods (h)

### OUTPUT
1. sink_id
1. stream_type
1. fluid
1. supply_temperature (ºC)
1. target_temperature (ºC)
1. flowrate (kg/h)
1. capacity (kW)
1. hourly_generation - yearly operating profile (kWh/h)

