from ....Source.simulation.Heat_Recovery.PINCH.convert_pinch import convert_pinch
from ....General.Auxiliary_General.stream_industry import stream_industry


# IMPORTANT
### OPTION 1 - just pinch analysis (no optimization) - INPUT: isolated streams (example below)
### OPTION 2 - pinch analysis with processes (co2,energy,cost optmization - 3 best solutions of each) - INPUT:processes, equipments
### OPTION 3 - pinch analysis with processes and isolated streams (co2,energy,cost optmization - 3 best solutions of each) - INPUT:processes, equipments and isolated streams
### OPTION 4 - equipment internal optimization (co2,energy,cost - 1 solution of each) - INPUT: only one equipment at a time


class ConvertPinch:
    def __init__(self):

        # need streams
        self.all_objects = [stream_industry(1, 'outflow', 'thermal_oil', 250, 40, 0.15 * 3600, 1, [1, 1, 1, 1]),
                 stream_industry(1, 'outflow', 'thermal_oil', 200, 80, 0.25 * 3600, 1, [1, 1, 1, 1]),
                 stream_industry(1, 'outflow', 'thermal_oil', 20, 180, 0.2 * 3600, 1, [1, 1, 1, 1]),
                 stream_industry(1, 'outflow', 'thermal_oil', 140, 230, 0.3 * 3600, 1, [1, 1, 1, 1])]

        # need minimum delta T for pinch analysis
        self.delta_T_min = 10




def testConvertPinch():
    data = ConvertPinch()
    test = convert_pinch(data)

    for hx in test['co2_optimization']['pinch_hx_data']:
        print(hx)

    """
     for hx in test['co2_optimization']['pinch_hx_data']:
            print(hx)

    Expected:
    {'Power': 25000.0, 'Hot_Stream': 2, 'Cold_Stream': 4, 'Type': 'hx_plate', 'HX_Turnkey_Cost': 15842.539435317562, 'OM_Fix_Cost': 9.092037053554732, 'Hot_Stream_T_Hot': 200, 'Hot_Stream_T_Cold': 150.0, 'Original_Hot_Stream': 2, 'Original_Cold_Stream': 4, 'Storage': 0, 'Storage_Satisfies': 100, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 15842.539435317562, 'Recovered_Energy': 100000.0}
    {'Power': 16000.0, 'Hot_Stream': 1, 'Cold_Stream': 3, 'Type': 'hx_plate', 'HX_Turnkey_Cost': 12812.546573843323, 'OM_Fix_Cost': 5.08378716232322, 'Hot_Stream_T_Hot': 203.33333333333334, 'Hot_Stream_T_Cold': 150.0, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 3, 'Storage': 0, 'Storage_Satisfies': 100, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 12812.546573843323, 'Recovered_Energy': 64000.0}
    {'Power': 13999.999999999996, 'Hot_Stream': 1, 'Cold_Stream': 4, 'Type': 'hx_plate', 'HX_Turnkey_Cost': 9506.536738371518, 'OM_Fix_Cost': 2.1926625256283763, 'Hot_Stream_T_Hot': 250, 'Hot_Stream_T_Cold': 203.33333333333334, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 4, 'Storage': 0, 'Storage_Satisfies': 100, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 9506.536738371518, 'Recovered_Energy': 55999.999999999985}
    {'Power': 35000.0, 'Hot_Stream': 2, 'Cold_Stream': 3, 'Type': 'hx_plate', 'HX_Turnkey_Cost': 16479.44590246096, 'OM_Fix_Cost': 10.1160091167848, 'Hot_Stream_T_Hot': 150.0, 'Hot_Stream_T_Cold': 80, 'Original_Hot_Stream': 2, 'Original_Cold_Stream': 3, 'Storage': 0, 'Storage_Satisfies': 100, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 16479.44590246096, 'Recovered_Energy': 140000.0}
    {'Power': 12990.299999999996, 'Hot_Stream': 1, 'Cold_Stream': 3, 'Type': 'hx_plate', 'HX_Turnkey_Cost': 6493.545595856755, 'OM_Fix_Cost': 0.7061386246495113, 'Hot_Stream_T_Hot': 150.0, 'Hot_Stream_T_Cold': 106.69900000000001, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 3, 'Storage': 0, 'Storage_Satisfies': 100, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 6493.545595856755, 'Recovered_Energy': 51961.19999999998}

     """

