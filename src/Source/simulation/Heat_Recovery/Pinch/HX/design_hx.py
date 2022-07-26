from ......General.Convert_Equipments.Auxiliary.design_cost_hx import design_cost_hx
from ......KB_General.hx_data import HxData
from ......KB_General.medium import Medium
from ......utilities.kb import KB


def design_hx(kb : KB ,hot_stream_index, cold_stream_index, hx_hot_stream_T_hot, hx_hot_stream_T_cold, hot_stream_fluid,
              hx_cold_stream_T_hot, hx_cold_stream_T_cold, cold_stream_fluid, hx_power, original_hot_stream_index,
              original_cold_stream_index):

    """Design and cost HX according to streams info

    Parameters
    ----------
    kb : dict
        Knowledge Base data

    hot_stream_index : int

    cold_stream_index : int

    hx_hot_stream_T_hot : float

    hx_hot_stream_T_cold : float

    hot_stream_fluid : str

    hx_cold_stream_T_hot : float

    hx_cold_stream_T_cold : float

    cold_stream_fluid : str

    hx_power : float

    original_hot_stream_index : int

    original_cold_stream_index : int

    Returns
    -------
    new_hx_row : dict
        New designed heat exchanger details
    """

    # info KB
    hx_data = HxData(kb)
    medium = Medium(kb)


    hx_turnkey_cost, hx_om_fix_cost = design_cost_hx(kb, hx_hot_stream_T_hot, hx_hot_stream_T_cold, hot_stream_fluid,
                                                     hx_cold_stream_T_hot, hx_cold_stream_T_cold, cold_stream_fluid,
                                                     hx_power)

    hx_type, hx_u_value = hx_data.get_values(hot_stream_fluid, cold_stream_fluid)

    if hot_stream_index != original_hot_stream_index:
        hot_split = True
    else:
        hot_split = False

    if cold_stream_index != original_cold_stream_index:
        cold_split = True
    else:
        cold_split = False

    hot_stream_cp = medium.cp(hot_stream_fluid, hx_hot_stream_T_hot)
    hot_stream_flowrate = hx_power / (abs(hx_hot_stream_T_hot - hx_hot_stream_T_cold) * hot_stream_cp)
    hot_stream_mcp = hx_power / (abs(hx_hot_stream_T_hot - hx_hot_stream_T_cold) )
    cold_stream_cp = medium.cp(cold_stream_fluid, hx_cold_stream_T_hot)
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
                  'HX_Hot_Stream_T_Hot': hx_hot_stream_T_hot,
                  'HX_Hot_Stream_T_Cold': hx_hot_stream_T_cold,
                  'HX_Cold_Stream_T_Hot': hx_cold_stream_T_hot,
                  'HX_Cold_Stream_T_Cold': hx_cold_stream_T_cold,
                  'HX_Type': hx_type,
                  'HX_Turnkey_Cost': hx_turnkey_cost,
                  'HX_OM_Fix_Cost': hx_om_fix_cost,
                  'HX_Original_Hot_Stream': int(original_hot_stream_index),
                  'HX_Original_Cold_Stream': int(original_cold_stream_index),
                  'Hot_Split': hot_split,
                  'Cold_Split': cold_split
    }


    return new_hx_row