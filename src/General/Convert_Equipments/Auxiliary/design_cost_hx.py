from ....KB_General.hx_data import HxData
from ....KB_General.equipment_details import EquipmentDetails
from ....General.Auxiliary_General.compute_delta_T_lmtd import compute_delta_T_lmtd_counter
from ....utilities.kb import KB


def design_cost_hx(kb : KB, hot_stream_T_hot, hot_stream_T_cold, hot_stream_fluid, cold_stream_T_hot, cold_stream_T_cold,cold_stream_fluid, hx_power):

    """Design and cost HX according to hot and cold stream characteristics

    Parameters
    ----------
    kb : dict
        Knowledge Base data

    hot_stream_T_hot : float
        Hot stream's hot/higher temperature [ºC]

    hot_stream_T_cold : float
        Hot stream's cold/lower temperature [ºC]

     hot_stream_fluid : str
        Hot stream fluid

    cold_stream_T_hot : float
        Hot stream's hot/higher temperature [ºC]

    cold_stream_T_cold : float
        Cold stream's cold/lower temperature [ºC]

    cold_stream_fluid : str
        Cold stream fluid

    hx_power :  float
        Heat exchanger designed power [kW]


    Returns
    -------
    hx_turnkey
        Heat exchanger turnkey [€]

    hx_om_fix
        Heat exchanger OM Fix [€/year]

    """

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
        hx_turnkey = 100 ** 10  # give large value
        hx_om_fix = 100 ** 10
        raise Exception('design_cost_hx.py error - Delta_LMTD ERROR!')

    return hx_turnkey, hx_om_fix
