from ....Source.simulation.Heat_Recovery.Pinch.convert_pinch import convert_pinch
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....Source.characterization.Generate_Equipment.generate_boiler import Boiler
from ....Source.characterization.Process.process import Process

# IMPORTANT
### OPTION 1 - just pinch analysis (no optimization) - INPUT: isolated streams (example below)
### OPTION 2 - pinch analysis with processes (co2,energy,cost optmization - 3 best solutions of each) - INPUT:processes, equipments
### OPTION 3 - pinch analysis with processes and isolated streams (co2,energy,cost optmization - 3 best solutions of each) - INPUT:processes, equipments and isolated streams
### OPTION 4 - equipment internal optimization (co2,energy,cost - 1 solution of each) - INPUT: only one equipment at a time


class ConvertPinch:
    def __init__(self):


        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 150, 100, 0.5 * 3600 / 2, 0.5* 3600 * 2 * (150 - 100),
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 90, 170, 0.2 * 3600 / 2, 0.2 * 3600 * 2 * (170 - 90),
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 90, 140, 0.4 * 3600 / 2, 0.4 * 3600 * 2 * (140 - 90),
                            [1, 1, 0, 1])]

        # stream_industry(1, 'outflow', 'thermal_oil', 250, 140, 0.1 * 3600, 0.1 * 3600*2*(250-5), [1, 1, 1, 0])]


        # need streams
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 750, 350, 0.045 * 3600 / 2, 0.045 * 3600 * 2 * (750 - 350),
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 550, 250, 0.04 * 3600 / 2, 0.04 * 3600 * 2 * (550 - 250),
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 300, 900, 0.043 * 3600 / 2, 0.043 * 3600 * 2 * (900 - 300),
                            [1, 1, 0, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 200, 550, 0.02 * 3600 / 2, 0.02 * 3600 * 2 * (550 - 200),
                            [1, 1, 1, 0])]



        # need streams
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 150, 100, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (150 - 40),
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 140, 100, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (140 - 100),
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 130, 100, 0.1 * 3600 / 2, 0.1 * 3600 * 2 * (130 - 100),
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 90, 170, 0.2 * 3600 / 2, 0.2 * 3600 * 2 * (170 - 90),
                            [1, 1, 0, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 90, 140, 0.4 * 3600 / 2, 0.4 * 3600 * 2 * (140 - 90),
                            [1, 1, 1, 0])]


        # need streams
        # pag.323
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 327, 150, 0.1098 * 3600 / 2, 34.1,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 495, 307, 0.134 * 3600 / 2, 16.5,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 220, 150, 0.2062 * 3600 / 2, 5.5,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 222, 150, 0.0739 * 3600 / 2, 5.5,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 140, 327, .1094 * 3600 / 2, 7.2,
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 140, 164, 0.698 * 3600 / 2, 19.6,
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 140, 500, 0.2 * 3600 / 2, 104.8,
                            [1, 1, 0, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 140, 169, 0.0618 * 3600 / 2, 104.8,
                            [1, 1, 0, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 480, 500, 1.625 * 3600 / 2, 104.8,
                            [1, 1, 0, 1])
            ]

        # need streams
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 750, 350, 0.045 * 3600 / 2, 0.045 * 3600 * 2 * (750 - 350),
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 550, 250, 0.04 * 3600 / 2, 0.04 * 3600 * 2 * (550 - 250),
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 300, 900, 0.043 * 3600 / 2, 0.043 * 3600 * 2 * (900 - 300),
                            [1, 1, 0, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 200, 550, 0.02 * 3600 / 2, 0.02 * 3600 * 2 * (550 - 200),
                            [1, 1, 1, 0])]

        self.delta_T_min = 50


        # need streams
        # pag.323
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 349, 183, 0.178 * 3600 / 2, 34.1,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 341, 183, 0.1 * 3600 / 2, 16.5,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 268, 183, 0.065 * 3600 / 2, 5.5,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 251, 183, 0.105 * 3600 / 2, 7.2,
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 163, 194, 0.6 * 3600 / 2, 19.6,
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 189, 368, 0.58 * 3600 / 2, 104.8,
                            [1, 1, 0, 1])
            ]


        # need minimum delta T for pinch analysis
        self.delta_T_min = 20




        # need streams
        # pag.323
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 349, 183, 0.178 * 3600 / 2, 34.1,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 341, 183, 0.1 * 3600 / 2, 16.5,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 268, 183, 0.065 * 3600 / 2, 5.5,
                            [1, 1, 1, 1]),
            stream_industry(1, 'outflow', 'thermal_oil', 251, 183, 0.105 * 3600 / 2, 7.2,
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 163, 194, 0.6 * 3600 / 2, 19.6,
                            [1, 1, 1, 1]),
            stream_industry(1, 'inflow', 'thermal_oil', 189, 368, 0.58 * 3600 / 2, 104.8,
                            [1, 1, 0, 1])
        ]

        # need minimum delta T for pinch analysis
        self.pinch_delta_T_min = 20
        self.hx_delta_T = 20


        # need streams
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 250, 40, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (250 - 40),
                            [1, 1, 1, 1]),
            stream_industry(2, 'outflow', 'thermal_oil', 200, 80, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (200 - 80),
                            [1, 1, 1, 1]),
            stream_industry(3, 'outflow', 'thermal_oil', 20, 180, 0.2 * 3600 / 2, 0.1 * 3600 * 2 * (180 - 20),
                            [1, 1, 1, 1]),
            stream_industry(4, 'inflow', 'thermal_oil', 140, 230, 0.3 * 3600 / 2, 0.2 * 3600 * 2 * (230 - 140),
                            [1, 1, 1, 1]), ]

        self.pinch_delta_T_min = 10
        self.hx_delta_T = 10


        # need streams
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 250, 40, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (250 - 40),
                            [1, 1, 1, 1]),
            stream_industry(2, 'outflow', 'thermal_oil', 200, 80, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (200 - 80),
                            [1, 1, 1, 1]),
            stream_industry(3, 'outflow', 'thermal_oil', 20, 180, 0.2 * 3600 / 2, 0.1 * 3600 * 2 * (180 - 20),
                            [1, 1, 1, 1]),
            stream_industry(4, 'inflow', 'thermal_oil', 140, 230, 0.3 * 3600 / 2, 0.2 * 3600 * 2 * (230 - 140),
                            [1, 1, 1, 1]), ]

        self.pinch_delta_T_min = 10


        # need streams
        # https://processdesign.mccormick.northwestern.edu/index.php/Pinch_analysis
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 180, 40, 40 * 3600 / 2, 40 * 3600 * 2 * (180 - 40),
                            [1, 1, 1, 1]),
            stream_industry(2, 'outflow', 'thermal_oil', 150, 60, 30 * 3600 / 2, 30 * 3600 * 2 * (150 - 60),
                            [1, 1, 1, 1]),
            stream_industry(3, 'outflow', 'thermal_oil', 30, 180, 60 * 3600 / 2, 60 * 3600 * 2 * (180 - 30),
                            [1, 1, 1, 1]),
            stream_industry(4, 'inflow', 'thermal_oil', 80, 160, 20 * 3600 / 2, 20 * 3600 * 2 * (160 - 80),
                            [1, 1, 1, 1]), ]

        self.pinch_delta_T_min = 20


        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 250, 40, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (250 - 40),
                            [1, 1, 1, 1]),
            stream_industry(2, 'outflow', 'thermal_oil', 200, 80, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (200 - 80),
                            [1, 1, 1, 1]),
            stream_industry(3, 'outflow', 'thermal_oil', 20, 180, 0.2 * 3600 / 2, 0.1 * 3600 * 2 * (180 - 20),
                            [1, 1, 1, 1]),
            stream_industry(4, 'inflow', 'thermal_oil', 140, 230, 0.3 * 3600 / 2, 0.2 * 3600 * 2 * (230 - 140),
                            [1, 1, 1, 1]), ]

        self.pinch_delta_T_min = 10




        # need streams
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 750, 350, 0.045 * 3600 / 2, 0.045 * 3600 * 2 * (750 - 350),
                            [1]),
            stream_industry(1, 'outflow', 'thermal_oil', 550, 250, 0.04 * 3600 / 2, 0.04 * 3600 * 2 * (550 - 250),
                            [1]),
            stream_industry(1, 'inflow', 'thermal_oil', 300, 900, 0.043 * 3600 / 2, 0.043 * 3600 * 2 * (900 - 300),
                            [1]),
            stream_industry(1, 'inflow', 'thermal_oil', 200, 550, 0.02 * 3600 / 2, 0.02 * 3600 * 2 * (550 - 200),
                            [1])]

        numbers = 1
        for i in self.all_objects:
            i['id'] = numbers
            numbers += 1
        self.pinch_delta_T_min = 50


        # need streams
        # https://processdesign.mccormick.northwestern.edu/index.php/Pinch_analysis
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 180, 40, 40 * 3600 / 2, 40 * 3600 * 2 * (180 - 40),
                            [1,1,0,0,1,1]),
            stream_industry(2, 'outflow', 'thermal_oil', 150, 60, 30 * 3600 / 2, 30 * 3600 * 2 * (150 - 60),
                            [0,1,0,0,0,1]),
            stream_industry(3, 'outflow', 'thermal_oil', 30, 180, 60 * 3600 / 2, 60 * 3600 * 2 * (180 - 30),
                            [1,1,0,1,1,0]),
            stream_industry(4, 'inflow', 'thermal_oil', 80, 160, 20 * 3600 / 2, 20 * 3600 * 2 * (160 - 80),
                            [0,1,0,0,1,1]), ]

        numbers = 1
        for i in self.all_objects:
            i['id'] = numbers
            numbers += 1


        self.pinch_delta_T_min = 20



        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 250, 40, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (250 - 40),
                            [1, 1, 1, 1]),
            stream_industry(2, 'outflow', 'thermal_oil', 200, 80, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (200 - 80),
                            [1, 1, 1, 1]),
            stream_industry(3, 'outflow', 'thermal_oil', 20, 180, 0.2 * 3600 / 2, 0.1 * 3600 * 2 * (180 - 20),
                            [1, 1, 1, 1]),
            stream_industry(4, 'inflow', 'thermal_oil', 140, 230, 0.3 * 3600 / 2, 0.2 * 3600 * 2 * (230 - 140),
                            [1, 1, 1, 1]), ]

        self.pinch_delta_T_min = 10

         # need streams
        # pag.323
        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 349, 183, 0.178 * 3600 / 2, 34.1,
                            [1]),
            stream_industry(1, 'outflow', 'thermal_oil', 341, 183, 0.1 * 3600 / 2, 16.5,
                            [1]),
            stream_industry(1, 'outflow', 'thermal_oil', 268, 183, 0.065 * 3600 / 2, 5.5,
                            [1]),
            stream_industry(1, 'outflow', 'thermal_oil', 251, 183, 0.105 * 3600 / 2, 7.2,
                            [1]),
            stream_industry(1, 'inflow', 'thermal_oil', 163, 194, 0.6 * 3600 / 2, 19.6,
                            [1,]),
            stream_industry(1, 'inflow', 'thermal_oil', 189, 368, 0.58 * 3600 / 2, 104.8,
                            [1, ])
        ]


        numbers = 1
        for i in self.all_objects:
            i['id'] = numbers
            numbers += 1

        # need minimum delta T for pinch analysis
        self.pinch_delta_T_min = 20


        # need streams
        # pag.338
        self.all_objects = [
            stream_industry(2, 'outflow', 'thermal_oil', 327, 50, 0.1098 * 3600 / 2, 34.1,
                            [1]),
            stream_industry(5, 'outflow', 'thermal_oil', 495, 307, 0.134 * 3600 / 2, 16.5,
                            [1]),
            stream_industry(6, 'outflow', 'thermal_oil', 220, 59, 0.2062 * 3600 / 2, 5.5,
                            [1]),
            stream_industry(9, 'outflow', 'thermal_oil', 222, 67, 0.0739 * 3600 / 2, 7.2,
                            [1]),
            stream_industry(1, 'inflow', 'thermal_oil', 102, 327, 0.1094 * 3600 / 2, 104.8,
                            [1]),

            stream_industry(3, 'inflow', 'thermal_oil', 35, 164, 0.0698 * 3600 / 2, 104.8,
                            [1]),

            stream_industry(4, 'inflow', 'thermal_oil', 140, 500, 0.2 * 3600 / 2, 104.8,
                            [1]),

            stream_industry(7, 'inflow', 'thermal_oil', 80, 123, 0.0767 * 3600 / 2, 104.8,
                            [1]),
            stream_industry(8, 'inflow', 'thermal_oil', 59, 169, 0.0618 * 3600 / 2, 104.8,
                            [1]),
            stream_industry(10, 'inflow', 'thermal_oil', 85, 125, 0.1025 * 3600 / 2, 104.8,
                            [1]),
            stream_industry(11, 'inflow', 'thermal_oil', 480, 500, 1.625 * 3600 / 2, 104.8,
                            [1]),

        ]


        self.all_objects = [
            stream_industry(1, 'outflow', 'thermal_oil', 250, 40, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (250 - 40),
                            [1, 1, 1, 1]),
            stream_industry(2, 'outflow', 'thermal_oil', 200, 80, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (200 - 80),
                            [1, 1, 1, 1]),
            stream_industry(3, 'outflow', 'thermal_oil', 20, 180, 0.2 * 3600 / 2, 0.1 * 3600 * 2 * (180 - 20),
                            [1, 1, 1, 1]),
            stream_industry(4, 'inflow', 'thermal_oil', 140, 230, 0.3 * 3600 / 2, 0.2 * 3600 * 2 * (230 - 140),
                            [1, 1, 1, 1]), ]

        self.pinch_delta_T_min = 10

        # need minimum delta T for pinch analysis
        self.pinch_delta_T_min = 10
        numbers= 1
        for i in self.all_objects:
            i['id'] = numbers
            numbers += 1



def testConvertPinch():

    import time
    t0 = time.time()

    data = ConvertPinch()
    test = convert_pinch(data)

    t1 = time.time()
    total = t1 - t0
    print('#################################################################################')
    print('#################################################################################')

    print('#################################################################################')

    print('time simulation [s]:', total)

    if test != []:
        for key in test.keys():
            print('------------------------------------------------------------------------------------------------------------')
            print(key)
            for i in test[key]:
                print(i)
    else:
        print('no HX')

    """
    Expected:
    
    ------------------------------------------------------------------------------------------------------------
    co2_optimization
    ------------------------------------------------------------------------------------------------------------
    energy_recovered_optimization
    {'total_turnkey': 9237.691072465488, 'total_co2_savings': 0.0, 'total_energy_recovered': 64.39999999999999, 'equipment_detailed_savings': [], 'pinch_hx_data': [{'Power': 8.6, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 3, 'Hot_Stream_T_Hot': 750.0, 'Hot_Stream_T_Cold': 550.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1597.5, 'HX_OM_Fix_Cost': 159.7, 'Storage': 0.16826086956521735, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 1299.9554025018795, 'Total_Turnkey_Cost': 2897.4554025018797, 'Recovered_Energy': 25.799999999999997}, {'Power': 0.4, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 4, 'Hot_Stream_T_Hot': 750.0, 'Hot_Stream_T_Cold': 550.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1313.3, 'HX_OM_Fix_Cost': 131.3, 'Storage': 0.00391304347826087, 'Storage_Satisfies': 50.0, 'Storage_Turnkey_Cost': 134.71477032252943, 'Total_Turnkey_Cost': 1448.0147703225293, 'Recovered_Energy': 0.8}, {'Power': 8.6, 'Original_Hot_Stream': 3, 'Original_Cold_Stream': 1, 'Hot_Stream_T_Hot': 500.0, 'Hot_Stream_T_Cold': 300.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1585.8, 'HX_OM_Fix_Cost': 158.6, 'Storage': 0.16826086956521735, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 1299.9554025018795, 'Total_Turnkey_Cost': 2885.7554025018794, 'Recovered_Energy': 25.799999999999997}, {'Power': 6.0, 'Original_Hot_Stream': 4, 'Original_Cold_Stream': 2, 'Hot_Stream_T_Hot': 500.0, 'Hot_Stream_T_Cold': 200.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1466.8, 'HX_OM_Fix_Cost': 146.7, 'Storage': 0.0391304347826087, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 539.6654971391985, 'Total_Turnkey_Cost': 2006.4654971391983, 'Recovered_Energy': 12.0}]}
    {'total_turnkey': 8866.064394961497, 'total_co2_savings': 0.0, 'total_energy_recovered': 63.8, 'equipment_detailed_savings': [], 'pinch_hx_data': [{'Power': 1.0, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 4, 'Hot_Stream_T_Hot': 750.0, 'Hot_Stream_T_Cold': 550.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1350.1, 'HX_OM_Fix_Cost': 135.0, 'Storage': 0.009782608695652175, 'Storage_Satisfies': 50.0, 'Storage_Turnkey_Cost': 234.02186068097257, 'Total_Turnkey_Cost': 1584.1218606809725, 'Recovered_Energy': 2.0}, {'Power': 8.0, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 3, 'Hot_Stream_T_Hot': 750.0, 'Hot_Stream_T_Cold': 550.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1570.2, 'HX_OM_Fix_Cost': 157.0, 'Storage': 0.0782608695652174, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 819.5216346394461, 'Total_Turnkey_Cost': 2389.721634639446, 'Recovered_Energy': 24.0}, {'Power': 8.6, 'Original_Hot_Stream': 3, 'Original_Cold_Stream': 1, 'Hot_Stream_T_Hot': 500.0, 'Hot_Stream_T_Cold': 300.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1585.8, 'HX_OM_Fix_Cost': 158.6, 'Storage': 0.16826086956521735, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 1299.9554025018795, 'Total_Turnkey_Cost': 2885.7554025018794, 'Recovered_Energy': 25.799999999999997}, {'Power': 6.0, 'Original_Hot_Stream': 4, 'Original_Cold_Stream': 2, 'Hot_Stream_T_Hot': 500.0, 'Hot_Stream_T_Cold': 200.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1466.8, 'HX_OM_Fix_Cost': 146.7, 'Storage': 0.0391304347826087, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 539.6654971391985, 'Total_Turnkey_Cost': 2006.4654971391983, 'Recovered_Energy': 12.0}]}
    {'total_turnkey': 3521.4654971391983, 'total_co2_savings': 0.0, 'total_energy_recovered': 28.0, 'equipment_detailed_savings': [], 'pinch_hx_data': [{'Power': 8.0, 'Original_Hot_Stream': 2, 'Original_Cold_Stream': 3, 'Hot_Stream_T_Hot': 550.0, 'Hot_Stream_T_Cold': 350.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1570.2, 'HX_OM_Fix_Cost': 157.0, 'Storage': 0.0, 'Storage_Satisfies': 100, 'Storage_Turnkey_Cost': 0.0, 'Total_Turnkey_Cost': 1570.2, 'Recovered_Energy': 24.0}, {'Power': 2.0, 'Original_Hot_Stream': 4, 'Original_Cold_Stream': 2, 'Hot_Stream_T_Hot': 300.0, 'Hot_Stream_T_Cold': 200.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1411.6, 'HX_OM_Fix_Cost': 141.2, 'Storage': 0.0391304347826087, 'Storage_Satisfies': 100, 'Storage_Turnkey_Cost': 539.6654971391985, 'Total_Turnkey_Cost': 1951.2654971391985, 'Recovered_Energy': 4.0}]}
    ------------------------------------------------------------------------------------------------------------
    energy_investment_optimization
    {'total_turnkey': 5438.230994278398, 'total_co2_savings': 0.0, 'total_energy_recovered': 24.0, 'equipment_detailed_savings': [], 'pinch_hx_data': [{'Power': 4.0, 'Original_Hot_Stream': 2, 'Original_Cold_Stream': 4, 'Hot_Stream_T_Hot': 550.0, 'Hot_Stream_T_Cold': 350.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1502.9, 'HX_OM_Fix_Cost': 150.3, 'Storage': 0.0391304347826087, 'Storage_Satisfies': 50.0, 'Storage_Turnkey_Cost': 539.6654971391985, 'Total_Turnkey_Cost': 2042.5654971391987, 'Recovered_Energy': 8.0}, {'Power': 4.0, 'Original_Hot_Stream': 2, 'Original_Cold_Stream': 3, 'Hot_Stream_T_Hot': 550.0, 'Hot_Stream_T_Cold': 350.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1444.4, 'HX_OM_Fix_Cost': 144.4, 'Storage': 0.0, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 0.0, 'Total_Turnkey_Cost': 1444.4, 'Recovered_Energy': 12.0}, {'Power': 2.0, 'Original_Hot_Stream': 4, 'Original_Cold_Stream': 2, 'Hot_Stream_T_Hot': 300.0, 'Hot_Stream_T_Cold': 200.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1411.6, 'HX_OM_Fix_Cost': 141.2, 'Storage': 0.0391304347826087, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 539.6654971391985, 'Total_Turnkey_Cost': 1951.2654971391985, 'Recovered_Energy': 4.0}]}
    {'total_turnkey': 9237.691072465488, 'total_co2_savings': 0.0, 'total_energy_recovered': 64.39999999999999, 'equipment_detailed_savings': [], 'pinch_hx_data': [{'Power': 8.6, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 3, 'Hot_Stream_T_Hot': 750.0, 'Hot_Stream_T_Cold': 550.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1597.5, 'HX_OM_Fix_Cost': 159.7, 'Storage': 0.16826086956521735, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 1299.9554025018795, 'Total_Turnkey_Cost': 2897.4554025018797, 'Recovered_Energy': 25.799999999999997}, {'Power': 0.4, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 4, 'Hot_Stream_T_Hot': 750.0, 'Hot_Stream_T_Cold': 550.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1313.3, 'HX_OM_Fix_Cost': 131.3, 'Storage': 0.00391304347826087, 'Storage_Satisfies': 50.0, 'Storage_Turnkey_Cost': 134.71477032252943, 'Total_Turnkey_Cost': 1448.0147703225293, 'Recovered_Energy': 0.8}, {'Power': 8.6, 'Original_Hot_Stream': 3, 'Original_Cold_Stream': 1, 'Hot_Stream_T_Hot': 500.0, 'Hot_Stream_T_Cold': 300.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1585.8, 'HX_OM_Fix_Cost': 158.6, 'Storage': 0.16826086956521735, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 1299.9554025018795, 'Total_Turnkey_Cost': 2885.7554025018794, 'Recovered_Energy': 25.799999999999997}, {'Power': 6.0, 'Original_Hot_Stream': 4, 'Original_Cold_Stream': 2, 'Hot_Stream_T_Hot': 500.0, 'Hot_Stream_T_Cold': 200.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1466.8, 'HX_OM_Fix_Cost': 146.7, 'Storage': 0.0391304347826087, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 539.6654971391985, 'Total_Turnkey_Cost': 2006.4654971391983, 'Recovered_Energy': 12.0}]}
    {'total_turnkey': 8866.064394961497, 'total_co2_savings': 0.0, 'total_energy_recovered': 63.8, 'equipment_detailed_savings': [], 'pinch_hx_data': [{'Power': 1.0, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 4, 'Hot_Stream_T_Hot': 750.0, 'Hot_Stream_T_Cold': 550.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1350.1, 'HX_OM_Fix_Cost': 135.0, 'Storage': 0.009782608695652175, 'Storage_Satisfies': 50.0, 'Storage_Turnkey_Cost': 234.02186068097257, 'Total_Turnkey_Cost': 1584.1218606809725, 'Recovered_Energy': 2.0}, {'Power': 8.0, 'Original_Hot_Stream': 1, 'Original_Cold_Stream': 3, 'Hot_Stream_T_Hot': 750.0, 'Hot_Stream_T_Cold': 550.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1570.2, 'HX_OM_Fix_Cost': 157.0, 'Storage': 0.0782608695652174, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 819.5216346394461, 'Total_Turnkey_Cost': 2389.721634639446, 'Recovered_Energy': 24.0}, {'Power': 8.6, 'Original_Hot_Stream': 3, 'Original_Cold_Stream': 1, 'Hot_Stream_T_Hot': 500.0, 'Hot_Stream_T_Cold': 300.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1585.8, 'HX_OM_Fix_Cost': 158.6, 'Storage': 0.16826086956521735, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 1299.9554025018795, 'Total_Turnkey_Cost': 2885.7554025018794, 'Recovered_Energy': 25.799999999999997}, {'Power': 6.0, 'Original_Hot_Stream': 4, 'Original_Cold_Stream': 2, 'Hot_Stream_T_Hot': 500.0, 'Hot_Stream_T_Cold': 200.0, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1466.8, 'HX_OM_Fix_Cost': 146.7, 'Storage': 0.0391304347826087, 'Storage_Satisfies': 100.0, 'Storage_Turnkey_Cost': 539.6654971391985, 'Total_Turnkey_Cost': 2006.4654971391983, 'Recovered_Energy': 12.0}]}

     """

