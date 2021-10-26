
from General.Auxiliary_General.linearize_values import linearize_values


def join_hx_and_technology(technologies,power_fraction,max_power_stream,max_power_grid,object_type):

    turnkey_max_power = 0
    turnkey_power_fraction = 0
    conversion_efficiency = 1
    om_fix = 0
    om_var = 0
    emissions = 0
    max_supply_capacity = 0
    conversion_efficiency_technology_name = ''


    for technology in technologies:
        conversion_efficiency_technology_name += '+' + technology['equipment']

        if technology['equipment'] == 'fresnel' or technology['equipment'] == 'evacuated_tube' or technology['equipment'] == 'flat_plate':
            max_supply_capacity_val = technology['max_average_supply_capacity']
        else:
            max_supply_capacity_val = technology['max_supply_capacity']

        max_supply_capacity += max_supply_capacity_val
        turnkey_max_power += max_supply_capacity_val * technology['turnkey_a'] + technology['turnkey_b']
        turnkey_power_fraction +=  max_supply_capacity_val*power_fraction * technology['turnkey_a'] + technology['turnkey_b']

        om_fix += technology['om_fix'] * max_supply_capacity_val
        om_var += technology['om_var'] * max_supply_capacity_val

    for technology in technologies:
        if technology['equipment'] == 'fresnel' or technology['equipment'] == 'evacuated_tube' or technology['equipment'] == 'flat_plate':
            max_supply_capacity_val = technology['max_average_supply_capacity']
        else:
            max_supply_capacity_val = technology['max_supply_capacity']

        emissions += technology['emissions'] * (max_supply_capacity_val)

    emissions = emissions / max_power_stream
    power_fraction_supply_capacity = max_power_stream*power_fraction
    conversion_efficiency = max_power_grid/max_power_stream

    turnkey_a,turnkey_b = linearize_values(turnkey_max_power, turnkey_power_fraction, max_power_stream, power_fraction_supply_capacity)

    conversion_efficiency_technology_name = conversion_efficiency_technology_name[1:]

    #if object_type == 'sink':
   #     max_power_stream /= conversion_efficiency
   # else:
   #     max_power_stream /= conversion_efficiency


    data_teo = {
        'equipment': conversion_efficiency_technology_name,
        'max_capacity': max_power_stream,  # [kW]
        'turnkey_a': turnkey_a,  # [€/kW]
        'turnkey_b': turnkey_b,  # [€]
        'conversion_efficiency': conversion_efficiency,  # []
        'om_fix': om_fix / max_power_stream,# [€/year.kW]
        'om_var': om_var / max_power_stream,# [€/kWh]
        'emissions': emissions,  # [kg.CO2/kWh]
        'tecnhologies': technologies,

    }

    return data_teo

