"""
@author: jmcunha/alisboa

Info: Design and cost HX for Pinch Analysis.

"""

from ......General.Convert_Equipments.Auxiliary.design_cost_hx import design_cost_hx
from ......KB_General.hx_type_and_u import hx_type_and_u

def pinch_design_hx(hot_stream_index,cold_stream_index,hx_hot_stream_T_hot, hx_hot_stream_T_cold, hot_stream_fluid, hx_cold_stream_T_hot, hx_cold_stream_T_cold, cold_stream_fluid, hx_power,original_hot_stream_index,original_cold_stream_index):


    hx_turnkey_cost, hx_om_fix_cost = design_cost_hx(hx_hot_stream_T_hot, hx_hot_stream_T_cold, hot_stream_fluid,hx_cold_stream_T_hot, hx_cold_stream_T_cold, cold_stream_fluid, hx_power)

    hx_type, hx_u_value = hx_type_and_u(hot_stream_fluid, cold_stream_fluid)

    if hot_stream_index != original_hot_stream_index:
        hot_split = True
    else:
        hot_split = False

    if cold_stream_index != original_cold_stream_index:
        cold_split = True
    else:
        cold_split = False

    new_hx_row = {'Power': int(hx_power),
                  'Hot_Stream': hot_stream_index,
                  'Cold_Stream': cold_stream_index,
                  'Hot_Stream_T_Hot': int(hx_hot_stream_T_hot),
                  'Hot_Stream_T_Cold': int(hx_hot_stream_T_cold),
                  'HX_Type': hx_type,
                  'HX_Turnkey_Cost': int(hx_turnkey_cost),
                  'HX_OM_Fix_Cost': int(hx_om_fix_cost),
                  'Original_Hot_Stream': original_hot_stream_index,
                  'Original_Cold_Stream': original_cold_stream_index,
                  'Hot_Split': hot_split,
                  'Cold_Split': cold_split}

    return new_hx_row