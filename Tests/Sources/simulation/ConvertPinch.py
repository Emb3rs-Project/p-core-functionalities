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

        test = 2
        if test == 1:
            ### OPTION 1  ###################################################
            # OPTION 1 - TEST 1
            self.all_input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 150, 100, 0.5 * 3600 / 2, 0.5* 3600 * 2 * (150 - 100), [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 90, 170, 0.2 * 3600 / 2, 0.2 * 3600 * 2 * (170 - 90), [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 90, 140, 0.4 * 3600 / 2, 0.4 * 3600 * 2 * (140 - 90), [1, 1, 0, 1])]
            self.pinch_delta_T_min = 20

        elif test == 2:
            # OPTION 1 - TEST 2
            self.all_input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 750, 350, 0.045 * 3600 / 2, 0.045 * 3600 * 2 * (750 - 350),  [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 550, 250, 0.04 * 3600 / 2, 0.04 * 3600 * 2 * (550 - 250), [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 300, 900, 0.043 * 3600 / 2, 0.043 * 3600 * 2 * (900 - 300), [1, 1, 0, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 200, 550, 0.02 * 3600 / 2, 0.02 * 3600 * 2 * (550 - 200), [1, 1, 1, 0])]
            self.pinch_delta_T_min = 50

        elif test == 3:
            # OPTION 1 - TEST 3
            self.all_input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 150, 100, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (150 - 40), [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 140, 100, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (140 - 100), [1, 1, 1, 1]),
                stream_industry(1, 'outflow', 'thermal_oil', 130, 100, 0.1 * 3600 / 2, 0.1 * 3600 * 2 * (130 - 100),  [1, 1, 1, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 90, 170, 0.2 * 3600 / 2, 0.2 * 3600 * 2 * (170 - 90), [1, 1, 0, 1]),
                stream_industry(1, 'inflow', 'thermal_oil', 90, 140, 0.4 * 3600 / 2, 0.4 * 3600 * 2 * (140 - 90), [1, 1, 1, 0])]
            self.pinch_delta_T_min = 20

        elif test == 4:
            # OPTION 1 - TEST 4
            # pag.323
            self.all_input_objects = [
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
            self.all_input_objects = [
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
            self.all_input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 250, 40, 0.15 * 3600 / 2, 0.15 * 3600 * 2 * (250 - 40), [1, 1, 1, 1]),
                stream_industry(2, 'outflow', 'thermal_oil', 200, 80, 0.25 * 3600 / 2, 0.25 * 3600 * 2 * (200 - 80), [1, 1, 1, 1]),
                stream_industry(3, 'outflow', 'thermal_oil', 20, 180, 0.2 * 3600 / 2, 0.1 * 3600 * 2 * (180 - 20),[1, 1, 1, 1]),
                stream_industry(4, 'inflow', 'thermal_oil', 140, 230, 0.3 * 3600 / 2, 0.2 * 3600 * 2 * (230 - 140), [1, 1, 1, 1]), ]

            self.pinch_delta_T_min = 10

        elif test == 7:
            # OPTION 1 - TEST 7
            # https://processdesign.mccormick.northwestern.edu/index.php/Pinch_analysis
            self.all_input_objects = [
                stream_industry(1, 'outflow', 'thermal_oil', 180, 40, 40 * 3600 / 2, 40 * 3600 * 2 * (180 - 40),[1, 1, 1, 1]),
                stream_industry(2, 'outflow', 'thermal_oil', 150, 60, 30 * 3600 / 2, 30 * 3600 * 2 * (150 - 60),[1, 1, 1, 1]),
                stream_industry(3, 'outflow', 'thermal_oil', 30, 180, 60 * 3600 / 2, 60 * 3600 * 2 * (180 - 30),[1, 1, 1, 1]),
                stream_industry(4, 'inflow', 'thermal_oil', 80, 160, 20 * 3600 / 2, 20 * 3600 * 2 * (160 - 80),[1, 1, 1, 1]), ]

            self.pinch_delta_T_min = 20

        elif test == 8:
            # OPTION 1 - TEST 8
            # pag.338
            self.all_input_objects = [
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
        for i in self.all_input_objects:
            i['id'] = numbers
            numbers += 1

        self.location = [41.13, -8.61]
        self.perform_all_combinations = True


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
            'supply_temperature':15
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
        self.global_conversion_efficiency = 0.93


class Input_Data_Remaining_Options():

    def __init__(self,all_objects):

        self.all_input_objects = all_objects
        self.pinch_delta_T_min = 10
        self.location = [41.13, -8.61]
        self.perform_all_combinations = True


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
        # create isolated stream  - meter aqui simple_user maybes
        isolated_stream = stream_industry(11, 'inflow', 'thermal_oil', 480, 500, 1.625 * 3600 / 2, 104.8, [1,0,1,0,0,1,1])

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
    {'ID': 0, 'streams': array([1, 2, 3, 4], dtype=int64), 'capex': 5963.400000000001, 'om_fix': 596.3, 'hot_utility': 9.2, 'cold_utility': 6.400000000000001, 'lifetime': 20, 'co2_savings': 0.0, 'money_savings': 0.0, 'energy_dispatch': 70.8, 'discount_rate': 0.41, 'equipment_detailed_savings': [], 'pinch_temperature': 525.0, 'pinch_hx_data': [{'HX_Power': 8.6, 'HX_Original_Cold_Stream': 3, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 750.0, 'HX_Hot_Stream_T_Cold': 550.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 3, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1597.5, 'HX_OM_Fix_Cost': 159.7, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 500.0, 'HX_Cold_Stream_T_Hot': 700.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1597.5, 'Recovered_Energy': 25.799999999999997}, {'HX_Power': 0.4, 'HX_Original_Cold_Stream': 4, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 750.0, 'HX_Hot_Stream_T_Cold': 550.0, 'HX_Hot_Stream': '100', 'HX_Cold_Stream': 4, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1313.3, 'HX_OM_Fix_Cost': 131.3, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 500.0, 'HX_Cold_Stream_T_Hot': 520.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1313.3, 'Recovered_Energy': 1.2000000000000002}, {'HX_Power': 8.6, 'HX_Original_Cold_Stream': 3, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 550.0, 'HX_Hot_Stream_T_Cold': 358.9, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 3, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1585.8, 'HX_OM_Fix_Cost': 158.6, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 300.0, 'HX_Cold_Stream_T_Hot': 500.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1585.8, 'Recovered_Energy': 25.799999999999997}, {'HX_Power': 6.0, 'HX_Original_Cold_Stream': 4, 'HX_Original_Hot_Stream': 2, 'HX_Hot_Stream_T_Hot': 550.0, 'HX_Hot_Stream_T_Cold': 400.0, 'HX_Hot_Stream': 2, 'HX_Cold_Stream': 4, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1466.8, 'HX_OM_Fix_Cost': 146.7, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 200.0, 'HX_Cold_Stream_T_Hot': 500.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1466.8, 'Recovered_Energy': 18.0}], 'theo_minimum_hot_utility': 6.3999999999999995, 'theo_minimum_cold_utility': 9.2}
    {'ID': 1, 'streams': array([1, 2, 3, 4], dtype=int64), 'capex': 5972.900000000001, 'om_fix': 597.3, 'hot_utility': 9.2, 'cold_utility': 6.400000000000001, 'lifetime': 20, 'co2_savings': 0.0, 'money_savings': 0.0, 'energy_dispatch': 70.8, 'discount_rate': 0.41, 'equipment_detailed_savings': [], 'pinch_temperature': 525.0, 'pinch_hx_data': [{'HX_Power': 1.0, 'HX_Original_Cold_Stream': 4, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 750.0, 'HX_Hot_Stream_T_Cold': 550.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 4, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1350.1, 'HX_OM_Fix_Cost': 135.0, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 500.0, 'HX_Cold_Stream_T_Hot': 550.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1350.1, 'Recovered_Energy': 3.0}, {'HX_Power': 8.0, 'HX_Original_Cold_Stream': 3, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 750.0, 'HX_Hot_Stream_T_Cold': 550.0, 'HX_Hot_Stream': '100', 'HX_Cold_Stream': 3, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1570.2, 'HX_OM_Fix_Cost': 157.0, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 500.0, 'HX_Cold_Stream_T_Hot': 686.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1570.2, 'Recovered_Energy': 24.0}, {'HX_Power': 8.6, 'HX_Original_Cold_Stream': 3, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 550.0, 'HX_Hot_Stream_T_Cold': 358.9, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 3, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1585.8, 'HX_OM_Fix_Cost': 158.6, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 300.0, 'HX_Cold_Stream_T_Hot': 500.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1585.8, 'Recovered_Energy': 25.799999999999997}, {'HX_Power': 6.0, 'HX_Original_Cold_Stream': 4, 'HX_Original_Hot_Stream': 2, 'HX_Hot_Stream_T_Hot': 550.0, 'HX_Hot_Stream_T_Cold': 400.0, 'HX_Hot_Stream': 2, 'HX_Cold_Stream': 4, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1466.8, 'HX_OM_Fix_Cost': 146.7, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 200.0, 'HX_Cold_Stream_T_Hot': 500.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1466.8, 'Recovered_Energy': 18.0}], 'theo_minimum_hot_utility': 6.3999999999999995, 'theo_minimum_cold_utility': 9.2}
    {'ID': 10, 'streams': array([1, 3, 4], dtype=int64), 'capex': 2984.9, 'om_fix': 298.5, 'hot_utility': 14.801236999999988, 'cold_utility': 14.799999999999999, 'lifetime': 20, 'co2_savings': 0.0, 'money_savings': 0.0, 'energy_dispatch': 54.0, 'discount_rate': 0.41, 'equipment_detailed_savings': [], 'pinch_temperature': 225.0, 'pinch_hx_data': [{'HX_Power': 3.6, 'HX_Original_Cold_Stream': 4, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 430.0, 'HX_Hot_Stream_T_Cold': 350.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 4, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1437.9, 'HX_OM_Fix_Cost': 143.8, 'Storage': 0, 'Cold_Split': 0.0, 'HX_Cold_Stream_T_Cold': 200.0, 'HX_Cold_Stream_T_Hot': 379.9, 'Hot_Split': 0.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1437.9, 'Recovered_Energy': 10.8}, {'HX_Power': 14.4, 'HX_Original_Cold_Stream': 3, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 750.0, 'HX_Hot_Stream_T_Cold': 430.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 3, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1547.0, 'HX_OM_Fix_Cost': 154.7, 'Storage': 0, 'Cold_Split': False, 'HX_Cold_Stream_T_Cold': 300.0, 'HX_Cold_Stream_T_Hot': 634.9, 'Hot_Split': False, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1547.0, 'Recovered_Energy': 43.2}], 'theo_minimum_hot_utility': 0.0, 'theo_minimum_cold_utility': 14.799999999999999}
    ------------------------------------------------------------------------------------------------------------
    energy_investment_optimization
    {'ID': 2, 'streams': array([1, 3], dtype=int64), 'capex': 1683.5, 'om_fix': 168.3, 'hot_utility': 0.8000000000000007, 'cold_utility': 0.7999999999999997, 'lifetime': 20, 'co2_savings': 0.0, 'money_savings': 0.0, 'energy_dispatch': 51.599999999999994, 'discount_rate': 0.41, 'equipment_detailed_savings': [], 'pinch_temperature': 725.0, 'pinch_hx_data': [{'HX_Power': 17.2, 'HX_Original_Cold_Stream': 3, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 750.0, 'HX_Hot_Stream_T_Cold': 367.8, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 3, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1683.5, 'HX_OM_Fix_Cost': 168.3, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 300.0, 'HX_Cold_Stream_T_Hot': 700.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1683.5, 'Recovered_Energy': 51.599999999999994}], 'theo_minimum_hot_utility': 0.8000000000000007, 'theo_minimum_cold_utility': 8.6}
    {'ID': 6, 'streams': array([1, 2, 3], dtype=int64), 'capex': 1712.1, 'om_fix': 171.2, 'hot_utility': 12.799999999999999, 'cold_utility': 12.8, 'lifetime': 20, 'co2_savings': 0.0, 'money_savings': 0.0, 'energy_dispatch': 51.599999999999994, 'discount_rate': 0.41, 'equipment_detailed_savings': [], 'pinch_temperature': 725.0, 'pinch_hx_data': [{'HX_Power': 17.2, 'HX_Original_Cold_Stream': 3, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 750.0, 'HX_Hot_Stream_T_Cold': 350.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 3, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1712.1, 'HX_OM_Fix_Cost': 171.2, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 300.0, 'HX_Cold_Stream_T_Hot': 700.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1712.1, 'Recovered_Energy': 51.599999999999994}], 'theo_minimum_hot_utility': 12.799999999999999, 'theo_minimum_cold_utility': 8.6}
    {'ID': 10, 'streams': array([1, 3, 4], dtype=int64), 'capex': 2984.9, 'om_fix': 298.5, 'hot_utility': 14.801236999999988, 'cold_utility': 14.799999999999999, 'lifetime': 20, 'co2_savings': 0.0, 'money_savings': 0.0, 'energy_dispatch': 54.0, 'discount_rate': 0.41, 'equipment_detailed_savings': [], 'pinch_temperature': 225.0, 'pinch_hx_data': [{'HX_Power': 3.6, 'HX_Original_Cold_Stream': 4, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 430.0, 'HX_Hot_Stream_T_Cold': 350.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 4, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1437.9, 'HX_OM_Fix_Cost': 143.8, 'Storage': 0, 'Cold_Split': 0.0, 'HX_Cold_Stream_T_Cold': 200.0, 'HX_Cold_Stream_T_Hot': 379.9, 'Hot_Split': 0.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1437.9, 'Recovered_Energy': 10.8}, {'HX_Power': 14.4, 'HX_Original_Cold_Stream': 3, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 750.0, 'HX_Hot_Stream_T_Cold': 430.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 3, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1547.0, 'HX_OM_Fix_Cost': 154.7, 'Storage': 0, 'Cold_Split': False, 'HX_Cold_Stream_T_Cold': 300.0, 'HX_Cold_Stream_T_Hot': 634.9, 'Hot_Split': False, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1547.0, 'Recovered_Energy': 43.2}], 'theo_minimum_hot_utility': 0.0, 'theo_minimum_cold_utility': 14.799999999999999}

     """

