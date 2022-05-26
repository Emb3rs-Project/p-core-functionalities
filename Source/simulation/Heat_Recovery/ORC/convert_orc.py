"""
alisboa/jmcunha

##############################
INFO: Convert_Options Raw Data to ORC, for maximum electrical generation.


##############################
INPUT:  consumer_type - 'household' or 'non-household'
        location = [latitude,longitude]
        get_best_number - number of best conversion cases, 3 by default
        streams - array with dicts where
                    {id,
                     object_type,
                     stream_type,
                     fluid, capacity,
                     supply_temperature,
                     target_temperature,
                     hourly_generation,
                     schedule}

        OPTIONAL:
            orc_T_evap [ºC]
            orc_T_cond [ºC]

##############################
OUTPUT: array best_options with dictionaries, e.g. best_options=[option_1,option_2,..]

        Where, for example:

        option_1 = {
        #           'ID' - orc design ID
        #           'streams_id' - vector with streams ID
        #           'electrical_generation_nominal' [kW]
        #           'electrical_generation_yearly' [kWh]
        #           'excess_heat_supply_capacity' [kW]
        #           'conversion_efficiency' []
        #           'turnkey' [€]
        #           'om_fix' - yearly om fix costs [€/year]
        #           'om_var' [€/kWh]
        #           'electrical_generation_yearly_turnkey' [kWh/€]
        #           'co2_savings'  [kg CO2/kWh]
        #           'money_savings' [€/kWh]
        #           'discount_rate' []
        #           'lifetime' [years]
        #  }


"""

import itertools
import pandas as pd
import numpy as np
from .....Source.simulation.Heat_Recovery.ORC.Auxiliary.convert_orc_aux import convert_aux
from .....KB_General.equipment_details import EquipmentDetails
from .....General.Auxiliary_General.get_country import get_country
from .....KB_General.fuel_properties import FuelProperties
from .....KB_General.get_interest_rate import get_interest_rate
from .....utilities.kb import KB
from .....Error_Handling.error_convert_orc import PlatformConvertORC
from .....Error_Handling.runtime_error import ModuleRuntimeException


def convert_orc(in_var, kb: KB):

    #################################################################
    # INPUT
    platform_data = PlatformConvertORC(**in_var['platform'])

    streams = platform_data.streams
    streams = [vars(stream) for stream in streams]
    consumer_type = platform_data.consumer_type
    location = platform_data.location
    get_best_number = platform_data.get_best_number
    orc_years_working = platform_data.orc_years_working


    orc_T_evap = platform_data.orc_T_evap
    orc_T_cond = platform_data.orc_T_cond

    #################################################################
    # KB
    fuel_properties = FuelProperties(kb)
    equipment_details = EquipmentDetails(kb)

    # Initialize Arrays
    convert_info = []
    stream_combination_not_feasible = []

    # ORC characteristics
    minimum_orc_power = 100  # [kW] - minimum power ORC designed
    hx_delta_T = 5
    hx_efficiency = 0.95
    power_fraction = 0.05
    carnot_correction_factor = 0.44
    eff_carnot = (1 - (orc_T_cond + 273.15) / (orc_T_evap + 273.15)) * carnot_correction_factor
    min_orc_supply_temperature = orc_T_evap + hx_delta_T

    # Intermediate Circuit Characteristics
    intermediate_fluid = 'water'

    #################################################################
    # COMPUTE
    # get country
    latitude, longitude = location
    country = get_country(latitude, longitude)

    # get interest rate and fuel price
    interest_rate = get_interest_rate(country, kb)
    electricity_data = fuel_properties.get_values(country, 'electricity', consumer_type)


    # check if streams temperature enough to be converted
    df_streams = pd.DataFrame.from_dict(streams)
    df_streams = df_streams.drop(df_streams[df_streams['supply_temperature'] < min_orc_supply_temperature].index)
    df_streams = df_streams.drop(df_streams[df_streams['capacity'] < minimum_orc_power].index)

    try:
        if df_streams.empty == False:
            df_streams['sum_hourly_generation'] = df_streams.apply(lambda x: sum(x['hourly_generation']), axis=1)
            df_streams_best_five = df_streams.sort_values('hourly_generation', ascending=False).head(n=get_best_number)
            streams_best_five_index = df_streams_best_five.index.tolist()

            # do all possible combinations between the streams
            combinations = []
            for L in range(0, len(streams_best_five_index) + 1):
                for subset in itertools.combinations(streams_best_five_index, L):
                    if list(subset) != []:
                        combinations.append(list(subset))

            # compute stream conversion info when aggregated and not aggregated
            streams_info = {}
            for stream_index in streams_best_five_index:
                stream = streams[stream_index]

                # Individual Stream
                aggregate_streams = False
                stream_thermal_capacity_max_power,orc_type,orc_electrical_generation,intermediate_turnkey_max_power,intermediate_om_fix_max_power,intermediate_om_var_max_power = convert_aux(kb,stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,power_fraction,intermediate_fluid, country,consumer_type,aggregate_streams)
                info_individual = {'orc_type':orc_type, 'stream_thermal_capacity_max_power':stream_thermal_capacity_max_power, 'orc_electrical_generation':orc_electrical_generation, 'intermediate_turnkey_max_power':intermediate_turnkey_max_power, 'intermediate_om_fix_max_power': intermediate_om_fix_max_power, 'intermediate_om_var_max_power': intermediate_om_var_max_power}

                # Aggregated
                aggregate_streams = True
                stream_thermal_capacity_max_power,orc_type,orc_electrical_generation,intermediate_turnkey_max_power,intermediate_om_fix_max_power,intermediate_om_var_max_power = convert_aux(kb,stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,power_fraction,intermediate_fluid, country,consumer_type,aggregate_streams)
                info_aggregate = {'orc_type':orc_type, 'stream_thermal_capacity_max_power':stream_thermal_capacity_max_power, 'orc_electrical_generation':orc_electrical_generation, 'intermediate_turnkey_max_power':intermediate_turnkey_max_power, 'intermediate_om_fix_max_power': intermediate_om_fix_max_power, 'intermediate_om_var_max_power': intermediate_om_var_max_power}

                streams_info[str(stream_index)] = {
                                                    'info_individual': info_individual,
                                                    'info_aggregate': info_aggregate
                                                   }

            new_id = 1

            # convert streams - all combinations possible
            for combination in combinations:
                electrical_generation_yearly = 0
                om_fix_intermediate = 0
                turnkey_intermediate = 0
                om_var_intermediate = 0
                stream_thermal_capacity_total = 0
                combo = []
                combination_streams_id = []
                vec_electrical_generation_nominal_total = []

                try:
                    for stream_index in combination:

                        if len(combination) > 1:  # aggregated
                            electrical_generation_nominal = streams_info[str(stream_index)]['info_aggregate']['orc_electrical_generation']
                            stream_thermal_capacity_total += streams_info[str(stream_index)]['info_aggregate']['stream_thermal_capacity_max_power']
                            om_fix_intermediate += streams_info[str(stream_index)]['info_aggregate']['intermediate_om_fix_max_power']
                            turnkey_intermediate += streams_info[str(stream_index)]['info_aggregate']['intermediate_turnkey_max_power']
                            om_var_intermediate += streams_info[str(stream_index)]['info_aggregate']['intermediate_om_var_max_power']
                            combo.append(streams[stream_index]['id'])

                        else:  # not aggregated
                            electrical_generation_nominal = streams_info[str(stream_index)]['info_individual']['orc_electrical_generation']
                            stream_thermal_capacity_total += streams_info[str(stream_index)]['info_individual']['stream_thermal_capacity_max_power']
                            om_fix_intermediate = streams_info[str(stream_index)]['info_individual']['intermediate_om_fix_max_power']
                            turnkey_intermediate = streams_info[str(stream_index)]['info_individual']['intermediate_turnkey_max_power']
                            om_var_intermediate = streams_info[str(stream_index)]['info_individual']['intermediate_om_var_max_power']

                        # yearly and nominal electric generation
                        if vec_electrical_generation_nominal_total == []:
                            vec_electrical_generation_nominal_total = [electrical_generation_nominal * i for i in streams[stream_index]['schedule']]
                        else:
                            vec_electrical_generation_nominal_total += electrical_generation_nominal * np.array(streams[stream_index]['schedule'])

                        electrical_generation_yearly += electrical_generation_nominal * sum(streams[stream_index]['schedule'])

                    # design ORC for this nominal electrical generation
                    electrical_generation_nominal_total = max(vec_electrical_generation_nominal_total)

                    if len(combination) > 1:
                        combination_streams_id.append(combo)
                        global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details.get_values('orc',electrical_generation_nominal_total)

                    else:
                        combination_streams_id.append([streams[stream_index]['id']])
                        global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details.get_values(streams_info[str(stream_index)]['info_individual']['orc_type'],electrical_generation_nominal_total)

                    # total costs
                    om_var_total = om_var_intermediate
                    om_fix_total = om_fix_orc + om_fix_intermediate
                    total_turnkey = turnkey_orc + turnkey_intermediate

                    # all convert options
                    if electrical_generation_nominal_total != 0:
                        convert_info.append({
                            'ID': new_id,
                            'streams_id': combination_streams_id[0],
                            'electrical_generation_nominal': electrical_generation_nominal_total,  # [kW]
                            'electrical_generation_yearly': electrical_generation_yearly,  # electric generation per year [kWh]
                            'excess_heat_supply_capacity': stream_thermal_capacity_total,  # [kW]
                            'conversion_efficiency': eff_carnot,  # [%]
                            'turnkey': total_turnkey,  # [€]
                            'om_fix': om_fix_total,  # yearly om fix costs [€/year]
                            'om_var': om_var_total/electrical_generation_yearly,  # [€/kWh]
                            'electrical_generation_yearly_turnkey': total_turnkey / electrical_generation_yearly,
                            'co2_savings': electricity_data['co2_emissions'],  # [kg CO2/kWh]
                            'money_savings': electricity_data['price'],  # [€/kWh]
                            "orc_T_evap": orc_T_evap,
                            "orc_T_cond": orc_T_cond
                            })

                        new_id += 1

                except:
                    stream_combination_not_feasible.append(str(combination))

            df_data = pd.DataFrame()
            for dict in convert_info:
                df_data = df_data.append(dict,ignore_index=True)

            # update columns for Business Module
            df_data['discount_rate'] = interest_rate
            df_data['lifetime'] = orc_years_working

            # get best
            if df_data.empty == False:
                best_options = df_data.sort_values('electrical_generation_yearly_turnkey', ascending=True).head(n=get_best_number).to_dict(orient='records')
            else:
                best_options = []
                raise ModuleRuntimeException(
                    code="1",
                    type="convert_orc.py",
                    msg="There are no feasible ORC designs ofr the streams provided."
                )
        else:
            best_options = []
            raise ModuleRuntimeException(
                code="1",
                type="convert_orc.py",
                msg="There are no feasible ORC designs ofr the streams provided."
            )

    except:
        raise ModuleRuntimeException(
            code="1",
            type="convert_orc.py",
            msg="ORC design to source' streams infeasible. Check sources' streams. \n "
                "If all inputs are correct report to the platform."
        )

    ##############################
    # OUTPUT
    output_orc = {
        'best_options': best_options,
        'df_streams_analyzed': df_streams.to_dict(orient='records'),
        "co2_emission_data":electricity_data['co2_emissions'],
        "elec_cost_data":electricity_data['price'],
    }

    return output_orc


