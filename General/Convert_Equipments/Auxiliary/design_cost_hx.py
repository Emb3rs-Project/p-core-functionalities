"""
@author: jmcunha/alisboa

Info: Design HX

Input: Hot Side and Cold Side Temperatures and fluids, as well as HX Power

Return: [hx_turnkey_cost,hx_om_fix_cost]
"""

from KB_General.hx_type_and_u import hx_type_and_u
from KB_General.equipment_details import equipment_details
from General.Auxiliary_General.compute_delta_T_lmtd import compute_delta_T_lmtd_counter

def design_cost_hx (hot_stream_T_hot,hot_stream_T_cold,hot_stream_fluid,cold_stream_T_hot,cold_stream_T_cold,cold_stream_fluid,hx_power):

    # HX info
    hx_type, hx_u_value = hx_type_and_u(hot_stream_fluid, cold_stream_fluid)
    delta_T_lmtd = compute_delta_T_lmtd_counter(hot_stream_T_hot, hot_stream_T_cold, cold_stream_T_hot, cold_stream_T_cold)

    # HX turnkey/om_fix cost
    if hx_type == 'hx_gas_cooler':
        hx_char = abs(hx_power)  # Gas cooler - Power
    else:
        hx_char = abs(hx_power) / (hx_u_value/1000 * delta_T_lmtd)  # Plate/Shell&tubes - Area

    global_conversion_efficiency,hx_om_fix,hx_turnkey = equipment_details(hx_type,hx_char)


    return hx_turnkey,hx_om_fix