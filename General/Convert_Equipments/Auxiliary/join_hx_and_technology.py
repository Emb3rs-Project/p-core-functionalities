"""
##############################
INFO: Aggregate conversion technologies and compute data for TEO


##############################
INPUT:  technologies - vector with technologies objects
        power_fraction - minimum power fraction technologies are designed for  []
        max_power_stream - maximum power stream can provide (sources - heat from excess heat stream; sinks - heat from grid stream) [kW]
        max_power_grid - maximum power supplied with conversion (sources - heat to grid; sinks - heat to sinks' needs) [kW]


##############################
OUTPUT: dictionary with:

            # equipment - all conversion equipments; array with technologies names; e.g. ['hx_plate', 'heat_pump','hx_plate']
            # max_capacity - stream power (sources- excess heat; sinks - grid heat)  [kW]
            # turnkey_a - aggregated turnkey [€/kW]
            # turnkey_b - aggregated om_var[€]
            # conversion_efficiency - aggregated conversion_efficiency []
            # om_fix - aggregated om_fix  [€/year.kW]
            # om_var - aggregated om_var  [€/kWh]
            # emissions - aggregated emissions  [kg.CO2/kWh]
            # technologies - each equipment info in detail


"""


from ....General.Auxiliary_General.linearize_values import linearize_values


def join_hx_and_technology(technologies,power_fraction,max_power_stream,max_power_grid,object_type):

    turnkey_max_power = 0
    turnkey_power_fraction = 0
    om_fix = 0
    om_var = 0
    emissions = 0
    max_supply_capacity = 0
    conversion_efficiency_technology_name = []

    technologies_dict = []


    for technology in technologies:

        technologies_dict.append(technology.__dict__)

        conversion_efficiency_technology_name.append(technology.data_teo['equipment'])

        if technology.data_teo['equipment'] == 'fresnel' or technology.data_teo['equipment'] == 'evacuated_tube' or technology.data_teo['equipment'] == 'flat_plate':
            max_supply_capacity_val = technology.data_teo['max_average_supply_capacity']
        else:
            max_supply_capacity_val = technology.data_teo['max_input_capacity']

        max_supply_capacity += max_supply_capacity_val
        turnkey_max_power += max_supply_capacity_val * technology.data_teo['turnkey_a'] + technology.data_teo['turnkey_b']
        turnkey_power_fraction += max_supply_capacity_val* power_fraction * technology.data_teo['turnkey_a'] + technology.data_teo['turnkey_b']

        om_fix += technology.data_teo['om_fix'] * max_supply_capacity_val
        om_var += technology.data_teo['om_var'] * max_supply_capacity_val
        emissions += technology.data_teo['emissions'] * max_supply_capacity_val

    power_fraction_supply_capacity = max_power_stream * power_fraction
    conversion_efficiency = max_power_grid/max_power_stream
    turnkey_a, turnkey_b = linearize_values(turnkey_max_power, turnkey_power_fraction, max_power_stream, power_fraction_supply_capacity)

    data_teo = {
        'equipment': conversion_efficiency_technology_name,
        'max_capacity': max_power_stream,  # [kW]
        'turnkey_a': turnkey_a,  # [€/kW]
        'turnkey_b': turnkey_b,  # [€]
        'conversion_efficiency': conversion_efficiency,  # []
        'om_fix': om_fix / max_power_stream,  # [€/year.kW]
        'om_var': om_var / max_power_stream,  # [€/kWh]
        'emissions': emissions / max_power_stream,  # [kg.CO2/kWh]
        'technologies': technologies_dict,

    }

    return data_teo

