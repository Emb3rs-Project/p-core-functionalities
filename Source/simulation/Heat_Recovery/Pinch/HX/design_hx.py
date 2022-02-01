"""
alisboa/jmcunha

##############################
INFO:  Design and cost HX according to streams info


##############################
INPUT:
        # hot_stream_index,
        # cold_stream_index
        # hx_hot_stream_T_hot  [ºC]
        # hx_hot_stream_T_cold  [ºC]
        # hot_stream_fluid
        # hx_cold_stream_T_hot  [ºC]
        # hx_cold_stream_T_cold  [ºC]
        # cold_stream_fluid
        # hx_power  [kW]
        # original_hot_stream_index
        # original_cold_stream_index


##############################
RETURN: a new_hx_row to add to the df_hx,

        Where,
            # new_hx_row = {
            #               'HX_Power', - hx power [kW]
            #               'HX_Hot_Stream', - stream ID, may be equal to Original_Hot_Stream or different if split occurred
            #               'HX_Cold_Stream', - stream ID
            #               'HX_Hot_Stream_flowrate',
            #               'HX_Cold_Stream_flowrate',
            #               'HX_Hot_Stream_T_Hot',  [ºC]
            #               'HX_Hot_Stream_T_Cold',  [ºC]
            #               'HX_Type', - type of hx, e.g. hx_plate, hx_shell_and_tubes, hx_kettle_boiler
            #               'HX_Turnkey_Cost',  [€]
            #               'HX_OM_Fix_Cost',  [€/year]
            #               'HX_Original_Hot_Stream', - original stream ID
            #               'HX_Original_Cold_Stream', - original stream ID
            #               'Hot_Split', - if split stream or not; True or False
            #               'Cold_Split',
            #               }

"""

from ......General.Convert_Equipments.Auxiliary.design_cost_hx import design_cost_hx
from ......KB_General.hx_type_and_u import hx_type_and_u
from ......KB_General.fluid_material import fluid_material_cp


def design_hx(hot_stream_index, cold_stream_index, hx_hot_stream_T_hot, hx_hot_stream_T_cold, hot_stream_fluid,
              hx_cold_stream_T_hot, hx_cold_stream_T_cold, cold_stream_fluid, hx_power, original_hot_stream_index,
              original_cold_stream_index):



    hx_turnkey_cost, hx_om_fix_cost = design_cost_hx(hx_hot_stream_T_hot, hx_hot_stream_T_cold, hot_stream_fluid,
                                                     hx_cold_stream_T_hot, hx_cold_stream_T_cold, cold_stream_fluid,
                                                     hx_power)

    hx_type, hx_u_value = hx_type_and_u(hot_stream_fluid, cold_stream_fluid)

    if hot_stream_index != original_hot_stream_index:
        hot_split = True
    else:
        hot_split = False

    if cold_stream_index != original_cold_stream_index:
        cold_split = True
    else:
        cold_split = False

    hot_stream_cp = fluid_material_cp(hot_stream_fluid, hx_hot_stream_T_hot)
    hot_stream_flowrate = hx_power / (abs(hx_hot_stream_T_hot - hx_hot_stream_T_cold) * hot_stream_cp)
    hot_stream_mcp = hx_power / (abs(hx_hot_stream_T_hot - hx_hot_stream_T_cold) )
    cold_stream_cp = fluid_material_cp(cold_stream_fluid, hx_cold_stream_T_hot)
    cold_stream_flowrate = hx_power / (abs(hx_cold_stream_T_hot - hx_cold_stream_T_cold) * cold_stream_cp)
    cold_stream_mcp = hx_power / (abs(hx_cold_stream_T_hot - hx_cold_stream_T_cold))

    new_hx_row = {
                  'HX_Power': round(hx_power + .0, 1),
                  'HX_Hot_Stream': hot_stream_index,
                  'HX_Cold_Stream': cold_stream_index,
                  'HX_Hot_Stream_mcp': hot_stream_mcp,
                  'HX_Cold_Stream_mcp': cold_stream_mcp,
                  'HX_Hot_Stream_flowrate': hot_stream_flowrate,
                  'HX_Cold_Stream_flowrate': cold_stream_flowrate,
                  'HX_Hot_Stream_T_Hot': round(hx_hot_stream_T_hot + .0, 1),
                  'HX_Hot_Stream_T_Cold': round(hx_hot_stream_T_cold + .0, 1),
                  'HX_Cold_Stream_T_Hot': round(hx_cold_stream_T_hot + .0, 1),
                  'HX_Cold_Stream_T_Cold': round(hx_cold_stream_T_cold + .0, 1),
                  'HX_Type': hx_type,
                  'HX_Turnkey_Cost': round(hx_turnkey_cost + .0, 1),
                  'HX_OM_Fix_Cost': round(hx_om_fix_cost + .0, 1),
                  'HX_Original_Hot_Stream': int(original_hot_stream_index),
                  'HX_Original_Cold_Stream': int(original_cold_stream_index),
                  'Hot_Split': hot_split,
                  'Cold_Split': cold_split
    }


    return new_hx_row