import numpy as np

def compute_delta_T_lmtd_paralel(T_source_in,T_source_out,T_sink_in,T_sink_out):

    delta_T_in = T_source_in - T_sink_in
    delta_T_out = T_source_out - T_sink_out
    delta_T_lmtd = (delta_T_in - delta_T_out) / np.log(delta_T_in / delta_T_out)

    return delta_T_lmtd

def compute_delta_T_lmtd_counter(T_source_hot,T_source_cold,T_sink_hot,T_sink_cold):

    delta_T_in = abs(T_source_hot - T_sink_hot)
    delta_T_out = abs(T_source_cold - T_sink_cold)

    if delta_T_in == delta_T_out:
        delta_T_lmtd = delta_T_in
    else:
        delta_T_lmtd = (delta_T_in - delta_T_out) / np.log(delta_T_in / delta_T_out)



    return delta_T_lmtd