# Source characterization submodule

The CF source characterization submodule receives the input data from the user and calculates available excess heat. It has 6 main functions (simple_user, generate_process, generate_boiler, generate_burner generate_cooling_equipment and generate_chp), and 5 auxiliary functions (schedule_hour; T_flue_gas; combustion_mass_flows; compute_flow_rate and stream). These are the main functionalities to analyse user data input for sources.

## generate_boiler function

This function is used when a user adds a boiler.

### INPUT
1. supply_capacity_nominal = Boiler heat supply capacity [kW]
1. equipment_sub_type = Boiler type (hot_water_boiler/ steam_boiler/ condensing_boiler)
1. open_closed_loop = in_var.open_closed_loop  # Open heating circuit? (1-Yes, 0-No)
1. supply_temperature = Boiler supply temperature - ºC (KB has default value)
1. fuel_type = Boiler fuel type (KB has default value)
1. global_conversion_efficiency = Boiler efficiency (KB has default value)
1. equipment schedule:
    - saturday_on = saturday operation (1-Yes, 0- No)
    - sunday_on = sunday operation (1-Yes, 0- No)
    - shutdown_periods = yearly shutdown periods (e.g: [[59,74],[152,172],[362,365]])
    - daily_periods = in_var.daily_periods (e.g: [[8,12],[15,19]])


### OUTPUT

It outputs a json file containing the following information on the 3 streams generated:

1. Air Inflow
    - supply_fluid (air)
    - inflow_T_initial,
    - inflow_T_outlet,
    - inflow_flowrate,
    - supply_capacity,
    - schedule
1. Supply Heat
    - supply_fluid (water by default)
    - return_temperature,
    - supply_temperature,
    - supply_flowrate,
    - supply_capacity,
    - schedule
1. Excess Heat
    - excess_heat_fluid (fluegas)
    - excess_heat_supply_temperature,
    - excess_heat_return_temperature,
    - excess_heat_flowrate,
    - excess_heat_supply_capacity,
    - schedule

## generate_burner function

This function generates streams from a user-defined burner equipment.

### INPUT
1. supply_capacity_nominal = Burner heat supply capacity [kW]
1. equipment_sub_type = Burner type (Burner only option)
1. supply_temperature = Burner supply temperature - ºC (KB has default value)
1. fuel_type = Burner fuel type (KB has default value)
1. global_conversion_efficiency = Burner efficiency (KB has default value)
1. equipment schedule:
    - saturday_on = saturday operation (1-Yes, 0- No)
    - sunday_on = sunday operation (1-Yes, 0- No)
    - shutdown_periods = yearly shutdown periods (e.g: [[59,74],[152,172],[362,365]])
    - daily_periods = in_var.daily_periods (e.g: [[8,12],[15,19]])


### OUTPUT

It outputs a json file containing the following information on the 3 streams generated:

1. Air Inflow
    - supply_fluid (air)
    - inflow_T_initial,
    - inflow_T_outlet,
    - inflow_flowrate,
    - supply_capacity,
    - schedule
1. Supply Heat
    - supply_fluid (water by default)
    - return_temperature,
    - supply_temperature,
    - supply_flowrate,
    - supply_capacity,
    - schedule
1. Excess Heat
    - excess_heat_fluid (fluegas)
    - excess_heat_supply_temperature,
    - excess_heat_return_temperature,
    - excess_heat_flowrate,
    - excess_heat_supply_capacity,
    - schedule
