"""
@author: jmcunha/alisboa

Info: Thermal Chiller design

Return: [chiller_evap_T_cold,chiller_evap_T_hot,intermediate_circuit,hx_intermediate_chiller]
"""

def design_chiller(source_T_hot, delta_T):


    if 125 <= source_T_hot:
        chiller_evap_T_cold = 70
        chiller_evap_T_hot = 90
        intermediate_circuit = True
        hx_intermediate_chiller = True

    elif 90 <= source_T_hot < 100:
        chiller_evap_T_cold = 70
        chiller_evap_T_hot = 90
        intermediate_circuit = False
        hx_intermediate_chiller = False


    return chiller_evap_T_cold,chiller_evap_T_hot,intermediate_circuit,hx_intermediate_chiller