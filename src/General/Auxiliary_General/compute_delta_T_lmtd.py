import numpy as np

def compute_delta_T_lmtd_counter(T_source_hot,T_source_cold,T_sink_hot,T_sink_cold):
    """Compute delta_T_lmtd for counter flow heat exchangers

    Parameters
    ----------
    T_source_hot : float
        Stream hot/higher temperature [ºC]
    T_source_cold : float
        Stream cold/lower temperature [ºC]
    T_sink_hot : float
        Stream hot/higher temperature [ºC]
    T_sink_cold : float
        Stream cold/lower temperature [ºC]

    Returns
    -------
    delta_T_lmtd : float
        Heat exchanger LMTD

    """

    delta_T_in = abs(T_source_hot - T_sink_hot)
    delta_T_out = abs(T_source_cold - T_sink_cold)

    if delta_T_in == delta_T_out:
        delta_T_lmtd = delta_T_in
    else:
        delta_T_lmtd = (delta_T_in - delta_T_out) / np.log(delta_T_in / delta_T_out)


    return delta_T_lmtd