"""
alisboa/jmcunha


##############################
INFO: design and cost HX according to hot and cold stream characteristics


##############################
INPUT:
        # hot_stream_T_hot  [ºC]
        # hot_stream_T_cold  [ºC]
        # hot_stream_fluid - fluid type
        # cold_stream_T_hot  [ºC]
        # cold_stream_T_cold  [ºC]
        # cold_stream_fluid - fluid type
        # hx_power  [kW]


##############################
RETURN:
        # hx_turnkey  [€]
        # hx_om_fix  [€/year]


"""

from ....KB_General.hx_data import HxData
from ....KB_General.equipment_details import EquipmentDetails
from ....General.Auxiliary_General.compute_delta_T_lmtd import compute_delta_T_lmtd_counter
from ....utilities.kb import KB


def design_cost_hx(kb : KB, hot_stream_T_hot, hot_stream_T_cold, hot_stream_fluid, cold_stream_T_hot, cold_stream_T_cold,cold_stream_fluid, hx_power):

    # HX info
    hx_data = HxData(kb)
    equipment_details = EquipmentDetails(kb)


    hx_type, hx_u_value = hx_data.get_values(hot_stream_fluid, cold_stream_fluid)
    delta_T_lmtd = compute_delta_T_lmtd_counter(hot_stream_T_hot, hot_stream_T_cold, cold_stream_T_hot,cold_stream_T_cold)

    # get turnkey and om_fix cost
    if delta_T_lmtd != 0:
        try:
            if hx_type == 'hx_gas_cooler':
                hx_char = abs(hx_power)  # Gas cooler - characteristic value is Power  [kW]
            else:
                hx_char = abs(hx_power) / (
                            hx_u_value / 1000 * delta_T_lmtd)  # Plate/Shell&tubes - characteristic value is Area  [m2]

            global_conversion_efficiency, hx_om_fix, hx_turnkey = equipment_details.get_values(hx_type, hx_char)

        except:
            hx_turnkey = 0
            hx_om_fix = 0
    else:
        print('delta_LMTD ERROR!')
        hx_turnkey = 100 ** 10  # give large value
        hx_om_fix = 100 ** 10

    return hx_turnkey, hx_om_fix
