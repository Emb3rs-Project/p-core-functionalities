import itertools
import pandas as pd
import numpy as np
from .....Source.simulation.Heat_Recovery.ORC.Auxiliary.get_data_of_converting_each_stream_to_orc import get_data_of_converting_each_stream_to_orc
from .....KB_General.equipment_details import EquipmentDetails
from .....utilities.kb import KB
from .....Error_Handling.error_convert_orc import PlatformConvertORC
from .....Error_Handling.runtime_error import ModuleRuntimeException
from .....Reports.orc_report import orc_report


def convert_orc(in_var, kb: KB):

    """
    The main routine for designing ORCs for the streams given

    :param in_var:
            - streams:``list with dicts``: each stream data, with the following keys:
                    - id: ``int``: stream ID []
                    - name: ``str``: stream name []
                    - object_type: ``str``: DEFAULT=stream []
                    - stream_type: ``str``: stream designation []; e.g. inflow, outflow, excess_heat
                    - supply_temperature: ``float``: stream's supply/initial temperature [ºC]
                    - target_temperature: ``float``: stream's target/final temperature [ºC]
                    - fluid: ``str``: stream's fluid []
                    - flowrate: ``float``: stream's mass flowrate [kg/h]
                    - schedule: ``list``: stream's hourly schedule
                    - hourly_generation: ``list``: stream's hourly capacity
                    - capacity: ``float``: stream's capacity [kW]

            - consumer_type: ``str``: type of consumer tariff []; 'household' or 'non-household'
            - get_best_number: ``int``: [OPTIONAL]  number of best conversion cases; DEFAULT=3
            - orc_years_working: ``int``: [OPTIONAL]  ORC working years [years]; DEFAULT=25
            - orc_T_evap: ``float``: [OPTIONAL] ORC evaporator temperature [ºC]; DEFAULT=110
            - orc_T_cond: ``float``: [OPTIONAL] ORC evaporator temperature [ºC]; DEFAULT=35

    :param kb: Knowledge Base data

    :return:
        - report: ``str``: HTML report
        - best_options: ``list with dicts``: each designed solution data, with the following keys:
                - ID: ``int``: ORC design ID []
                - streams_id: ``list``:  streams ID considered for the solution []
                - electrical_generation_nominal: ``float``: ORC nominal electrical generation [kW]
                - electrical_generation_yearly: ``float``: ORC yearly electrical generation [kWh]
                - excess_heat_supply_capacity: ``float``: streams thermal capacity available [kW]
                - conversion_efficiency: ``float``: ORC heat to electricity conversion efficiency []
                - turnkey: ``float``: ORC investment cost [€]
                - om_fix: ``float``: ORC yearly OM fix costs [€/year]
                - om_var: ``float``: ORC yearly OM var costs [€/kWh]
                - electrical_generation_yearly_turnkey: ``float``: ORC yearly electrical generation over turnkey [kWh/€]
                - co2_savings: ``float``: ORC yearly CO2 savings (all electricity is considered to be consumed)  [kg CO2/kWh]
                - money_savings: ``float``: ORC yearly monetary savings (all electricity is considered to be consumed [€/kWh]
                - discount_rate: ``float``: discount rate []
                - lifetime: ``float``: ORC working years [years]


    """

    #################################################################
    # INPUT
    platform_data = PlatformConvertORC(**in_var['platform'])

    streams = platform_data.streams
    streams = [vars(stream) for stream in streams]
    get_best_number = platform_data.get_best_number
    orc_years_working = platform_data.orc_years_working
    orc_T_evap = platform_data.orc_T_evap
    orc_T_cond = platform_data.orc_T_cond
    fuels_data = platform_data.fuels_data
    interest_rate = platform_data.interest_rate

    fuels_data = vars(fuels_data)
    for fuel in fuels_data.keys():
        fuels_data[fuel] = vars(fuels_data[fuel])

    #################################################################
    #GET DATA
    # Initialize Arrays
    convert_info = []
    stream_combination_not_feasible = []
    aggregate_options = [True, False]

    # KB
    equipment_details = EquipmentDetails(kb)

    # ORC characteristics
    minimum_orc_power = 100  # [kW] - minimum power ORC designed
    hx_delta_T = 5
    hx_efficiency = 0.95
    power_fraction = 0.05
    carnot_correction_factor = 0.44
    eff_carnot_corrected = (1 - (orc_T_cond + 273.15) / (orc_T_evap + 273.15)) * carnot_correction_factor
    min_orc_supply_temperature = orc_T_evap + hx_delta_T
    intermediate_fluid = 'water'


    # get interest rate and fuel price
    electricity_data = fuels_data['electricity']
    electricity_price = electricity_data["price"]
    electricity_co2_emissions = electricity_data["co2_emissions"]


    # check if streams temperature enough to be converted
    df_streams = pd.DataFrame.from_dict(streams)
    df_streams = df_streams.drop(df_streams[df_streams['supply_temperature'] < min_orc_supply_temperature].index)
    df_streams = df_streams.drop(df_streams[df_streams['capacity'] < minimum_orc_power].index)

    #################################################################
    # COMPUTE
    try:
        all_streams_index = df_streams.index.tolist()

        # do all possible combinations between the streams
        combinations = []
        for L in range(0, len(all_streams_index) + 1):
            for subset in itertools.combinations(all_streams_index, L):
                if list(subset) != []:
                    combinations.append(list(subset))

        # compute stream conversion info when aggregated and not aggregated
        streams_info = {}
        for stream_index in all_streams_index:
            stream = streams[stream_index]
            streams_info[str(stream_index)] = {'info_individual': {}, 'info_aggregate': {}}

            for aggregate_option in aggregate_options:

                stream_thermal_capacity_max_power, orc_type, orc_electrical_generation, intermediate_turnkey_max_power, intermediate_om_fix_max_power, intermediate_om_var_max_power = get_data_of_converting_each_stream_to_orc(
                    kb, stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency, power_fraction, intermediate_fluid,
                    fuels_data, aggregate_option)

                info = {
                    'orc_type': orc_type,
                    'stream_thermal_capacity_max_power': stream_thermal_capacity_max_power,
                    'orc_electrical_generation': orc_electrical_generation,
                    'intermediate_turnkey_max_power': intermediate_turnkey_max_power,
                    'intermediate_om_fix_max_power': intermediate_om_fix_max_power,
                    'intermediate_om_var_max_power': intermediate_om_var_max_power}

                if aggregate_option == True:
                    streams_info[str(stream_index)]['info_individual'] = info
                else:
                    streams_info[str(stream_index)]['info_aggregate'] = info

        # convert streams - all combinations possible
        new_id = 1
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
                        info_type = "info_aggregate"
                        combo.append(streams[stream_index]['id'])
                    else:  # not aggregated
                        info_type = "info_individual"

                    electrical_generation_nominal = streams_info[str(stream_index)][info_type]['orc_electrical_generation']
                    stream_thermal_capacity_total += streams_info[str(stream_index)][info_type]['stream_thermal_capacity_max_power']
                    om_fix_intermediate = streams_info[str(stream_index)][info_type]['intermediate_om_fix_max_power']
                    turnkey_intermediate = streams_info[str(stream_index)][info_type]['intermediate_turnkey_max_power']
                    om_var_intermediate = streams_info[str(stream_index)][info_type]['intermediate_om_var_max_power']

                    # yearly and nominal electric generation
                    if vec_electrical_generation_nominal_total == []:
                        vec_electrical_generation_nominal_total = [electrical_generation_nominal * i for i in
                                                                   streams[stream_index]['schedule']]
                    else:
                        vec_electrical_generation_nominal_total += electrical_generation_nominal * np.array(
                            streams[stream_index]['schedule'])

                    electrical_generation_yearly += electrical_generation_nominal * sum(
                        streams[stream_index]['schedule'])

                # design ORC for this nominal electrical generation
                electrical_generation_nominal_total = max(vec_electrical_generation_nominal_total)

                if len(combination) > 1:
                    combination_streams_id.append(combo)
                    global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details.get_values(
                        'orc', electrical_generation_nominal_total)

                else:
                    combination_streams_id.append([streams[stream_index]['id']])
                    global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details.get_values(
                        streams_info[str(stream_index)]['info_individual']['orc_type'],
                        electrical_generation_nominal_total)

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
                        'electrical_generation_yearly': electrical_generation_yearly,# electric generation per year [kWh]
                        'excess_heat_supply_capacity': stream_thermal_capacity_total,  # [kW]
                        'conversion_efficiency': eff_carnot_corrected,  # [%]
                        'capex': total_turnkey,  # [€]
                        'om_fix': om_fix_total,  # yearly om fix costs [€/year]
                        'om_var': om_var_total / electrical_generation_yearly,  # [€/kWh]
                        'electrical_generation_yearly_turnkey': total_turnkey / electrical_generation_yearly,
                        'co2_savings': electricity_co2_emissions,  # [kg CO2/kWh]
                        'money_savings': electricity_price,  # [€/kWh]
                        "orc_T_evap": orc_T_evap,
                        "orc_T_cond": orc_T_cond
                    })

                    new_id += 1

            except:
                stream_combination_not_feasible.append(str(combination))

        df_data = pd.DataFrame()
        for dict in convert_info:
            df_data = pd.concat([df_data, pd.DataFrame([dict])], ignore_index=True)


        # get best solutions
        if df_data.empty == False:
            # update columns for Business Module
            df_data['discount_rate'] = interest_rate
            df_data['lifetime'] = orc_years_working

            best_options = df_data.sort_values('electrical_generation_yearly_turnkey', ascending=True).head(
                n=get_best_number)
        else:
            raise ModuleRuntimeException(
                code="2",
                type="convert_orc.py",
                msg="There are no feasible ORC designs off the streams provided."
            )

    except:
        raise ModuleRuntimeException(
            code="1",
            type="convert_orc.py",
            msg="ORC design to source' streams infeasible. Check sources' streams.  "
                "If all inputs are correct report to the platform."
        )

    # Get Report HTML
    data_report = {
        "best_options": best_options,
        "df_streams": df_streams,
        "co2_emission_data": electricity_co2_emissions,
        "elec_cost_data": electricity_price,
    }

    report_html = orc_report(data_report)

    ##############################
    # OUTPUT
    output = {
        'best_options': best_options.to_dict(orient='records'),
        'report': report_html
    }

    return output
