# Source characterization submodule

The CF source characterization submodule receives the input data from the user and calculates available excess heat. It has 6 main functions (simple_user, generate_process, generate_boiler, generate_burner generate_cooling_equipment and generate_chp), and 5 auxiliary functions (schedule_hour; T_flue_gas; combustion_mass_flows; compute_flow_rate and stream). These are the main functionalities to analyse user data input for sources.

## generate_boiler function

This function is used when a user adds a boiler.

### INPUT
1. supply_capacity_nominal = Boiler heat supply capacity [kW]
1. equipment_sub_type = Boiler type (hot_water_boiler/ steam_boiler/ condensing_boiler)
1. open_closed_loop = open_closed_loop  # Open heating circuit? (1-Yes, 0-No)
1. supply_temperature = Boiler supply temperature - ºC (KB has default value)
1. fuel_type = Boiler fuel type (KB has default value)
1. global_conversion_efficiency = Boiler efficiency (KB has default value)
1. equipment schedule:
    - saturday_on = saturday operation (1-Yes, 0- No)
    - sunday_on = sunday operation (1-Yes, 0- No)
    - shutdown_periods = yearly shutdown periods (e.g: [[59,74],[152,172],[362,365]])
    - daily_periods = daily_periods (e.g: [[8,12],[15,19]])


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
    - daily_periods = daily_periods (e.g: [[8,12],[15,19]])


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


## generate_chp function

This function generates streams from a user-defined combined heat and power equipment (a gas engine or a gas turbine).

### INPUT
1. supply_capacity_nominal = CHP heat supply capacity [kW]
1. equipment_sub_type = CHP type (gas engine or gas turbine)
1. open_closed_loop = open_closed_loop  # Open heating circuit? (1-Yes, 0-No)
1. supply_temperature = CHP supply temperature - ºC (KB has default value)
1. fuel_type = CHP fuel type (KB has default value)
1. global_conversion_efficiency = CHP efficiency (KB has default value)
1. thermal_conversion_efficiency = CHP thermal efficiency (KB has default value)
1. electrical_conversion_efficiency = CHP electrical efficiency (KB has default value)
1. equipment schedule:
    - saturday_on = saturday operation (1-Yes, 0- No)
    - sunday_on = sunday operation (1-Yes, 0- No)
    - shutdown_periods = yearly shutdown periods (e.g: [[59,74],[152,172],[362,365]])
    - daily_periods = daily_periods (e.g: [[8,12],[15,19]])


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

## generate_cooling_equipment
This function generates streams from a user-defined cooling equipment (a co2_chiller/ cooling_tower/ thermal_chiller/ air_cooled_chiller/ water_cooled_chiller).

### INPUT
1. supply_capacity_nominal = cooling equipment heat supply capacity [kW]
1. equipment_sub_type = cooling equipment type (co2_chiller/ cooling_tower/ thermal_chiller/ air_cooled_chiller/ water_cooled_chiller)
1. supply_temperature = cooling equipment supply temperature - ºC (KB has default value)
1. global_conversion_efficiency = cooling equipment COP (KB has default value)
1. equipment schedule:
    - saturday_on = saturday operation (1-Yes, 0- No)
    - sunday_on = sunday operation (1-Yes, 0- No)
    - shutdown_periods = yearly shutdown periods (e.g: [[59,74],[152,172],[362,365]])
    - daily_periods = daily_periods (e.g: [[8,12],[15,19]])

### OUTPUT

It outputs a json file containing the following information on the 2 streams generated. Excess heat stream is only generated for CO2 chillers.

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

## generate_process

This function will generate the streams related to a process, according to the user specifications.

### INPUT
1. equipment = equipment that supplies heat/cold to the process [kW]
1. operation_temperature = process operation temperature (ºC)
1. startup_op = process startup (1-yes, 0-no)
    - startup_fluid (list)
    - startup_T_initial (ºC)
    - startup_mass (kg)
    - startup_fluid_cp (kJ/kg.K - default values from KB)
1. maintenance_op = process maintenance (1-yes, 0-no)
    - maintenance_capacity (kW)
1. n_inflows = process number of inflows (0 - 10)
    - inflow_fluid (list)
    - inflow_supply_temperature (ºC)
    - inflow_target_temperature (ºC)
    - inflow_flowrate (kg/h)
    - inflow_fluid_cp (kJ/kg.K - default values from KB)
1. n_outflows = process number of outflows (0 - 10)
    - outflow_fluid (list)
    - outflow_supply_temperature (ºC)
    - outflow_target_temperature (ºC)
    - outflow_flowrate (kg/h)
    - outflow_fluid_cp (kJ/kg.K - default values from KB)
1. process schedule:
    - saturday_on = saturday operation (1-Yes, 0- No)
    - sunday_on = sunday operation (1-Yes, 0- No)
    - shutdown_periods = yearly shutdown periods (e.g: [[59,74],[152,172],[362,365]])
    - daily_periods = daily_periods (e.g: [[8,12],[15,19]])
    - schedule_type = process type (0-continuous, 1-batch)
    - cycle_time_percentage = time percentage for startup and ouflows (0-1)


### OUTPUT

It outputs a json file containing the following information on the n streams generated (startup, maintenance, inflows, outflows), having for each stream
- supply_fluid (water by default)
- return_temperature (ºC),
- supply_temperature (ºC),
- supply_flowrate (kg/h),
- supply_capacity (kW),
- hourly_generation (kWh/h),
