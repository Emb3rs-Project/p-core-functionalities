from ....General.Auxiliary_General.linearize_values import linearize_values


def aggregate_technologies_info(object_id, technologies, power_fraction, max_power_available, max_power_convertible,
                                object_type, teo_equipment_name, stream_id):

    """ Aggregate conversion technologies and compute data for TEO

    Parameters
    ----------
    object_id : str
        Source/sink ID or 'grid_specfic'

    technologies : list with dicts
        Technologies data

    power_fraction : float
        Design equipment for max and fraction power; value between 0 and 1 []


    max_power_available : float
        Stream max power available before conversion [kW]

    max_power_convertible : float
        Stream power given to the the DHN after conversion  [kW]

    object_type : str
        'sink' or 'source'

    teo_equipment_name : str
        Specific TEO nomenclature for the technology name

    stream_id : int, str
        Stream ID


    Returns
    -------
    data_teo : dict
        technologies data for the TEO module, with the following keys:

        - teo_equipment_name : str
            Specific nomenclature for the TEO

        - output : str
            Specific nomenclature for the TEO

        - input_fuel : str
            Specific nomenclature for the TEO

        - output_fuel : str
            Specific nomenclature for the TEO

        - equipment : list
            All conversion equipments; list with technologies names; e.g. ['hx_plate', 'heat_pump','hx_plate']

        - max_capacity : float
            Stream power (sources- excess heat; sinks - grid heat)  [kW]

        - turnkey_a : float
            Aggregated turnkey [€/kW]

        - turnkey_b : float
            Aggregated om_var [€]

        - conversion_efficiency :
            Aggregated conversion_efficiency []

        - electrical_conversion_efficiency : float
            ONLY FOR ORC - electrical conversion efficiency []

        - om_fix : float
            Aggregated om_fix [€/year.kW]

        - om_var : float
            Aggregated om_var [€/kWh]

        - emissions : float
            Aggregated emissions [kg.CO2/kWh]

        - technologies : list with dicts
            Each equipment info in detail (check General/Convert_Equipments/Convert_Options)


    """

    turnkey_max_power = 0
    turnkey_power_fraction = 0
    om_fix = 0
    om_var = 0
    emissions = 0
    max_supply_capacity = 0
    all_equipment = []
    technologies_dict = []

    if object_type == 'sink':
        if object_id == 'grid_specific':
            input_fuel = None
        else:
            if teo_equipment_name.find('hp') == 0 or teo_equipment_name.find('absorption_chiller') == 0:
                input_fuel = 'dhnwaterdemand'  # + electricity
            else:
                input_fuel = 'dhnwaterdemand'

        if object_id == 'grid_specific':
            output_fuel = 'dhnwatersupply'
        else:
            output_fuel = 'sink' + str(object_id) + 'str' + str(stream_id) + 'dem'

    else:
        if teo_equipment_name.find('hp') == 0:
            input_fuel = "eh" + 'str' + str(stream_id) + 'sou' + str(object_id)  # + electricity
        else:
            input_fuel = "eh" + 'str' + str(stream_id) + 'sou' + str(object_id)

        if teo_equipment_name.find('orc') == 0 or teo_equipment_name.find('chp') == 0:
            output_fuel = 'dhnwatersupply'  # + electricity
        else:
            output_fuel = 'dhnwatersupply'


    for technology in technologies:

        technologies_dict.append(technology.__dict__)

        all_equipment.append(technology.data_teo['equipment'])

        if technology.data_teo['equipment'] == 'fresnel' or technology.data_teo['equipment'] == 'evacuated_tube' or technology.data_teo['equipment'] == 'flat_plate':
            max_supply_capacity_val = technology.data_teo['max_average_supply_capacity']
        else:
            max_supply_capacity_val = technology.data_teo['max_input_capacity']

        turnkey_max_power += max_supply_capacity_val * technology.data_teo['turnkey_a'] + technology.data_teo['turnkey_b']
        turnkey_power_fraction += max_supply_capacity_val * power_fraction * technology.data_teo['turnkey_a'] + technology.data_teo['turnkey_b']

        om_fix += technology.data_teo['om_fix'] * max_supply_capacity_val
        om_var += technology.data_teo['om_var'] * max_supply_capacity_val
        emissions += technology.data_teo['emissions'] * max_supply_capacity_val


    power_fraction_supply_capacity = max_power_available * power_fraction
    conversion_efficiency = max_power_convertible/max_power_available
    turnkey_a, turnkey_b = linearize_values(turnkey_max_power, turnkey_power_fraction, max_power_available, power_fraction_supply_capacity)




    # TEO CHANGES FOR THE NAMES
    if object_type == 'sink':
        if object_id == 'grid_specific':
            teo_equipment_name = 'grid_specific' + '_' + str(teo_equipment_name)
        else:
            teo_equipment_name = str(object_type) + '_' + str(object_id) + '_' + 'str' + str(stream_id) + '_' + str(teo_equipment_name)
    else:
        teo_equipment_name = str(object_type) + '_' + str(object_id) + '_' + 'str' + str(stream_id) + '_' + str(teo_equipment_name)


    teo_equipment_name = teo_equipment_name.replace('_','')
    teo_equipment_name = teo_equipment_name.replace('-','')




    if object_id == 'grid_specific':
        gs_cost = 10 ** 6
        data_teo = {
            'teo_equipment_name': teo_equipment_name,
            'output': 1,
            'input_fuel': input_fuel,
            'output_fuel': output_fuel,
            'equipment': all_equipment,
            'max_capacity': round(max_power_available, 3),  # [kW]
            'turnkey_a': round(turnkey_a, 3),  # [€/kW]
            'turnkey_b': round(turnkey_b, 3),  # [€]
            'conversion_efficiency': round(conversion_efficiency, 3),  # []
            'om_fix': round(om_fix / max_power_available, 3) * gs_cost,  # [€/year.kW]
            'om_var': round(om_var / max_power_available, 3) * gs_cost,  # [€/kWh]
            'emissions': round(emissions / max_power_available, 3),  # [kg.CO2/kWh]
            'technologies': technologies_dict,
        }

    else:
        if 'orc' in teo_equipment_name:
            for technology in technologies:
                if technology.data_teo['equipment'] == 'orc':
                    electrical_conversion_efficiency = technology.data_teo['electrical_conversion_efficiency']

            data_teo = {
                'teo_equipment_name': teo_equipment_name,
                'output': 1,
                'input_fuel': input_fuel,
                'output_fuel': output_fuel,
                'equipment': all_equipment,
                'max_capacity': round(max_power_available, 3),  # [kW]
                'turnkey_a': round(turnkey_a, 3),  # [€/kW]
                'turnkey_b': round(turnkey_b, 3),  # [€]
                'conversion_efficiency': round(conversion_efficiency, 3),  # []
                'electrical_conversion_efficiency': round(electrical_conversion_efficiency, 3),
                'om_fix': round(om_fix / max_power_available, 3),  # [€/year.kW]
                'om_var': round(om_var / max_power_available, 3),  # [€/kWh]
                'emissions': round(emissions / max_power_available, 3),  # [kg.CO2/kWh]
                'technologies': technologies_dict,
            }
        else:
            data_teo = {
                'teo_equipment_name': teo_equipment_name,
                'output': 1,
                'input_fuel': input_fuel,
                'output_fuel': output_fuel,
                'equipment': all_equipment,
                'max_capacity': round(max_power_available, 3),  # [kW]
                'turnkey_a': round(turnkey_a, 3),  # [€/kW]
                'turnkey_b': round(turnkey_b, 3),  # [€]
                'conversion_efficiency': round(conversion_efficiency, 3),  # []
                'om_fix': round(om_fix / max_power_available, 3),  # [€/year.kW]
                'om_var': round(om_var / max_power_available, 3),  # [€/kWh]
                'emissions': round(emissions / max_power_available, 3),  # [kg.CO2/kWh]
                'technologies': technologies_dict,
            }

    return data_teo

