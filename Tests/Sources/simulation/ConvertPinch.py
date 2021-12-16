from ....Source.simulation.Heat_Recovery.Pinch.convert_pinch import convert_pinch
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....Source.characterization.Generate_Equipment.generate_boiler import Boiler
from ....Source.characterization.Process.process import Process

# IMPORTANT
### OPTION 1 - just pinch analysis (energy optimization) - INPUT: isolated streams (example below)
### OPTION 2 - pinch analysis with processes (co2,energy,cost optmization - 3 best solutions of each) - INPUT:processes, equipments
### OPTION 3 - pinch analysis with processes and isolated streams (co2,energy,cost optmization - 3 best solutions of each) - INPUT:processes, equipments and isolated streams
### OPTION 4 - equipment internal optimization (co2,energy,cost - 1 solution of each) - INPUT: only one equipment at a time


class Option_1:
    def __init__(self):

        test = 6
        if test == 1:
            ### OPTION 1  ###################################################
            # OPTION 1 - TEST 1
            self.input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 150, 100, 0.5 * 3600 / 2, 0.5* 3600 * 2 * (150 - 100), [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 90, 170, 0.2 * 3600 / 2, 0.2 * 3600 * 2 * (170 - 90), [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 90, 140, 0.4 * 3600 / 2, 0.4 * 3600 * 2 * (140 - 90), [1, 1, 0, 1])]
            self.pinch_delta_T_min = 20

        elif test == 2:
            # OPTION 1 - TEST 2
            self.input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 750, 350, 0.045 * 3600 / 2, 0.045 * 3600 * 2 * (750 - 350),  [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 550, 250, 0.04 * 3600 / 2, 0.04 * 3600 * 2 * (550 - 250), [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 300, 900, 0.043 * 3600 / 2, 0.043 * 3600 * 2 * (900 - 300), [1, 1, 0, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 200, 550, 0.02 * 3600 / 2, 0.02 * 3600 * 2 * (550 - 200), [1, 1, 1, 0])]
            self.pinch_delta_T_min = 50

        elif test == 3:
            # OPTION 1 - TEST 3
            self.input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 150, 100, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (150 - 40), [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 140, 100, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (140 - 100), [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 130, 100, 0.1 * 3600 / 2, 0.1 * 3600 * 2 * (130 - 100),  [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 90, 170, 0.2 * 3600 / 2, 0.2 * 3600 * 2 * (170 - 90), [1, 1, 0, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 90, 140, 0.4 * 3600 / 2, 0.4 * 3600 * 2 * (140 - 90), [1, 1, 1, 0])]
            self.pinch_delta_T_min = 20

        elif test == 4:
            # OPTION 1 - TEST 4
            # pag.323
            self.input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 327, 150, 0.1098 * 3600 / 2, 34.1,  [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 495, 307, 0.134 * 3600 / 2, 16.5, [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 220, 150, 0.2062 * 3600 / 2, 5.5,   [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 222, 150, 0.0739 * 3600 / 2, 5.5, [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 140, 327, .1094 * 3600 / 2, 7.2, [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 140, 164, 0.698 * 3600 / 2, 19.6,  [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 140, 500, 0.2 * 3600 / 2, 104.8,  [1, 1, 0, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 140, 169, 0.0618 * 3600 / 2, 104.8,  [1, 1, 0, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 480, 500, 1.625 * 3600 / 2, 104.8, [1, 1, 0, 1])
                ]
            self.pinch_delta_T_min = 20

        elif test == 5:
            # OPTION 1 - TEST 5
            self.input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 349, 183, 0.178 * 3600 / 2, 34.1, [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 341, 183, 0.1 * 3600 / 2, 16.5,   [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 268, 183, 0.065 * 3600 / 2, 5.5,  [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 251, 183, 0.105 * 3600 / 2, 7.2, [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 163, 194, 0.6 * 3600 / 2, 19.6,  [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 189, 368, 0.58 * 3600 / 2, 104.8, [1, 1, 0, 1])
                ]
            self.pinch_delta_T_min = 20

        elif test == 6:
            # OPTION 1 - TEST 6
            self.input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 250, 40, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (250 - 40), [1, 1, 1, 1]),
                stream_industry(2, 'outflow', 'thermal_oil', 200, 80, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (200 - 80), [1, 1, 1, 1]),
                stream_industry(3, 'outflow', 'thermal_oil', 20, 180, 0.2 * 3600 / 2, 0.1 * 3600 * 2 * (180 - 20),[1, 1, 1, 1]),
                stream_industry(4, 'inflow', 'thermal_oil', 140, 230, 0.3 * 3600 / 2, 0.2 * 3600 * 2 * (230 - 140), [1, 1, 1, 1]), ]

            self.pinch_delta_T_min = 10

        elif test == 7:
            # OPTION 1 - TEST 7
            # https://processdesign.mccormick.northwestern.edu/index.php/Pinch_analysis
            self.input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 180, 40, 40 * 3600 / 2, 40 * 3600 * 2 * (180 - 40),[1, 1, 1, 1]),
                stream_industry(2, 'outflow', 'thermal_oil', 150, 60, 30 * 3600 / 2, 30 * 3600 * 2 * (150 - 60),[1, 1, 1, 1]),
                stream_industry(3, 'outflow', 'thermal_oil', 30, 180, 60 * 3600 / 2, 60 * 3600 * 2 * (180 - 30),[1, 1, 1, 1]),
                stream_industry(4, 'inflow', 'thermal_oil', 80, 160, 20 * 3600 / 2, 20 * 3600 * 2 * (160 - 80),[1, 1, 1, 1]), ]

            self.pinch_delta_T_min = 20

        elif test == 8:
            # OPTION 1 - TEST 8
            # pag.338
            self.input_objects = [
                stream_industry(2, 'outflow', 'thermal_oil', 327, 50, 0.1098 * 3600 / 2, 34.1, [1]),
                stream_industry(5, 'outflow', 'thermal_oil', 495, 307, 0.134 * 3600 / 2, 16.5, [1]),
                stream_industry(6, 'outflow', 'thermal_oil', 220, 59, 0.2062 * 3600 / 2, 5.5, [1]),
                stream_industry(9, 'outflow', 'thermal_oil', 222, 67, 0.0739 * 3600 / 2, 7.2, [1]),
                stream_industry(1, 'inflow', 'thermal_oil', 102, 327, 0.1094 * 3600 / 2, 104.8, [1]),
                stream_industry(3, 'inflow', 'thermal_oil', 35, 164, 0.0698 * 3600 / 2, 104.8, [1]),
                stream_industry(4, 'inflow', 'thermal_oil', 140, 500, 0.2 * 3600 / 2, 104.8, [1]),
                stream_industry(7, 'inflow', 'thermal_oil', 80, 123, 0.0767 * 3600 / 2, 104.8, [1]),
                stream_industry(8, 'inflow', 'thermal_oil', 59, 169, 0.0618 * 3600 / 2, 104.8, [1]),
                stream_industry(10, 'inflow', 'thermal_oil', 85, 125, 0.1025 * 3600 / 2, 104.8, [1]),
                stream_industry(11, 'inflow', 'thermal_oil', 480, 500, 1.625 * 3600 / 2, 104.8, [1]),
            ]
            self.pinch_delta_T_min = 20

        # give IDs
        numbers = 1
        for i in self.input_objects:
            i['id'] = numbers
            numbers += 1

        self.country = 'Portugal'


######################################################################################################
class Process_data():
    def __init__(self):

        self.id = 55
        self.equipment = 101
        self.saturday_on = 1
        self.sunday_on = 1
        self.shutdown_periods = []
        self.daily_periods = [[0, 2], [8, 12], [15, 20]]
        self.operation_temperature = 150
        self.schedule_type = 0
        self.cycle_time_percentage = 0.1

        # startup_stream
        startup_stream_1 = {
            'mass':100,
            'fluid_cp':4.2,
            'fluid':'water',
            'supply_temperature':20
            }

        maintenance_stream_1 = {
            'capacity':100
            }

        inflow_stream_1 = {
            'flowrate':100,
            'fluid':'thermal_oil',
            'fluid_cp':2,
            'supply_temperature':10
            }

        inflow_stream_2 = {
            'flowrate':100,
            'fluid':'thermal_oil',
            'fluid_cp':2,
            'supply_temperature':10
            }

        outflow_stream_1 = {
            'flowrate':100,
            'fluid_cp':2,
            'fluid':'thermal_oil',
            'target_temperature':45
            }

        self.startup_data = [startup_stream_1]
        self.maintenance_data = [maintenance_stream_1]
        self.inflow_data = [inflow_stream_1, inflow_stream_2]
        self.outflow_data = [outflow_stream_1]


class GenerateBoiler():

    def __init__(self):

        self.id = 101

        # Schedule
        self.saturday_on = 0
        self.sunday_on = 0
        self.shutdown_periods = []
        self.daily_periods = [[0, 24]]

        # Generate_Equipment Characteristics FROM USER
        self.supply_temperature = 180
        self.open_closed_loop = 0  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = 'natural_gas'  # Fuel type  (Natural gas, Fuel oil, Biomass)

        # Generate_Equipment Characteristics FROM KB_General/USER
        self.return_temperature = 50

        ###################################
        self.supply_capacity = 7500
        self.processes = []

        ###################
        # Optional/Expert User inputs -  should be shown on the platform as default values
        self.equipment_sub_type = 'steam_boiler'
        self.supply_fluid = 'steam'
        self.global_conversion_efficiency = 0.95


class Input_Data_Remaining_Options():

    def __init__(self,all_objects):

        self.all_objects = all_objects
        self.pinch_delta_T_min = 10
        self.country = 'Portugal'


########################################################################################
########################################################################################
########################################################################################

def testConvertPinch():

    import time
    t0 = time.time()

    option = 1
    # OPTION 1 - test isolated streams
    if option == 1:
        data = Option_1()
        test = convert_pinch(data)

    # OPTION 2 - test processes, equipments
    elif option ==2:
        # create process
        process_data = Process_data()
        process = Process(process_data)
        # create equipment
        equipment_data = GenerateBoiler()
        equipment = Boiler(equipment_data)

        input_data = Input_Data_Remaining_Options([process.__dict__, equipment.__dict__])
        test = convert_pinch(input_data)

    # OPTION 3 - test processes, equipments and isolated streams
    elif option == 3:
        # create process
        process_data = Process_data()
        process = Process(process_data)
        # create equipment
        equipment_data = GenerateBoiler()
        equipment = Boiler(equipment_data)
        # create isolated stream
        isolated_stream = stream_industry(11, 'inflow', 'thermal_oil', 480, 500, 1.625 * 3600 / 2, 104.8, [1,0,1,0,0,1,1]),

        input_data = Input_Data_Remaining_Options([process.__dict__, equipment.__dict__, isolated_stream])
        test = convert_pinch(input_data)

    # OPTION 4 - test equipment (one at a time)
    elif option == 4:
        # create equipment
        equipment_data = GenerateBoiler()
        equipment = Boiler(equipment_data)

        input_data = Input_Data_Remaining_Options([equipment.__dict__])
        test = convert_pinch(input_data)


    t1 = time.time()
    total = t1 - t0

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

