




import math
from General.Simple_User.simple_user import simple_user
from Source.characterization.Generate_Equipment.generate_boiler import Boiler
from Source.characterization.Generate_Equipment.generate_chp import Chp
from Source.characterization.Process.process import Process
from Source.simulation.Heat_Recovery.generate_heat_recovery import generate_heat_recovery
from General.Auxiliary_General.stream import Stream


class Boiler_data():
    def __init__(self):
        self.id = 1000

        # Schedule
        self.saturday_on = 0
        self.sunday_on = 0
        self.shutdown_periods = [[60, 75], [150, 155], [360, 365]]
        self.daily_periods = [[0, 14]]

        # Generate_Equipment Characteristics FROM USER
        self.equipment_sub_type = 'steam_boiler'
        self.supply_capacity_nominal = 7500
        self.supply_temperature = 180
        self.open_closed_loop = 0  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = 'natural_gas'  # Fuel type  (Natural gas, Fuel oil, Biomass)

        # Generate_Equipment Characteristics FROM KB_General/USER
        self.global_conversion_efficiency = 0.95
        self.supply_fluid = 'steam'
        self.excess_heat_fluid = 'oil'
        self.return_temperature = 50


class Chp_data():
    def __init__(self):
        self.id = 3000

        # Schedule
        self.saturday_on = 1
        self.sunday_on = 1
        self.shutdown_periods = [[60, 75], [150, 155], [360, 365]]
        self.daily_periods = [[9, 24]]

        # Generate_Equipment Characteristics FROM USER
        self.equipment_sub_type = 'gas_engine'
        self.electrical_generation = 500
        self.supply_temperature = 180
        self.open_closed_loop = 0  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = 'natural_gas'  # Fuel type  (Natural gas, Fuel oil, Biomass)

        # Generate_Equipment Characteristics FROM KB_General/USER
        self.global_conversion_efficiency = 0.8406
        self.thermal_conversion_efficiency = 0.525
        self.supply_fluid = 'oil'
        self.excess_heat_fluid = 'oil'
        self.return_temperature = 50


class Process_data():
    def __init__(self):
        self.id = 55
        self.equipment = 1000
        self.saturday_on = 1
        self.sunday_on = 1
        self.shutdown_periods = []
        self.daily_periods = [[0, 2], [8, 12], [15, 20]]
        self.operation_temperature = 80
        self.schedule_type = 0
        self.cycle_time_percentage = 0

        self.startup_data = []
        self.maintenance_data = []
        self.inflow_data = [Inflow()]
        self.outflow_data = [Outflow()]


class Inflow():
    def __init__(self):
        self.id = 6000
        self.supply_temperature = 20
        self.fluid = 'oil'
        self.flowrate = 50
        self.fluid_cp = 2


class Outflow():
    def __init__(self):
        self.id = 9000
        self.daily_periods = [[3, 5], [21, 24]]
        self.target_temperature = 30
        self.fluid = 'oil'
        self.flowrate = 23
        self.fluid_cp = 2


class Info_HX_Recovery():

    def __init__(self, delta_T_min, all_objects):
        self.delta_T_min = delta_T_min
        self.all_objects = all_objects



class Source_simplified():
    def __init__(self):
        # Input
        # Input
        self.object_id = 5
        self.type_of_object = 'source'
        self.streams = [{'supply_temperature':500,'target_temperature':55,'fluid':'flue_gas','fluid_cp':10,'flowrate':10,'saturday_on':1
                         ,'sunday_on':1,'shutdown_periods':[],'daily_periods':[[10,18]]},
                        {'supply_temperature':150,'target_temperature':100,'fluid':'water','fluid_cp':10,'flowrate':10,'saturday_on':1
                         ,'sunday_on':1,'shutdown_periods':[],'daily_periods':[[10,18]]}]



# SOURCE Simple ----------------------------------------
source = Source_simplified()
industry_stream_test = simple_user(source)


# SOURCE Detailed ----------------------------------------
# create chp
chp_data = Chp_data()
chp = Chp(chp_data)
chp.id = 58
# user that wants to put average supply capacity directly - chp.update_supply_capacity(10000)
chp.update_supply_capacity(3000)

create_stream_id = 200
for stream in chp.streams:  # Give a stream ID
    stream.id = create_stream_id
    create_stream_id += 1


# create boiler
boiler_data = Boiler_data()
boiler = Boiler(boiler_data)
for stream in boiler.streams:
    stream.id = create_stream_id
    create_stream_id += 1


# create process
process_data = Process_data()
process = Process(process_data)
for stream in process.streams:
    stream.id = create_stream_id
    create_stream_id += 1


# update equipments linked to processes
# user that wants to put average supply capacity directly - boiler.update_supply_capacity(10000)
boiler.update_processes([process])


###########################
# HX Recovery --------------------------
# Get delta_T for pinch analysis
delta_T_min = int(input('Introduce delta_T:'))
delta_T_min = 10

### OPTION 1 - just pinch analysis - INPUT: isolated streams
print('Introduce Stream? (no excess heat from equipments supplying process):')
prompt = int(input('Yes?'))
prompt = 1
if prompt == 1:
    info_data = [Stream(1, 'outflow', 'oil', 250, 40, 0.15 * 3600, 1, [1, 1, 1, 1]),
                 Stream(1, 'outflow', 'oil', 200, 80, 0.25 * 3600, 1, [1, 1, 1, 1]),
                 Stream(1, 'outflow', 'oil', 20, 180, 0.2 * 3600, 1, [1, 1, 1, 1]),
                 Stream(1, 'outflow', 'oil', 140, 230, 0.3 * 3600, 1, [1, 1, 1, 1])]  # Stream(source,stream_type,fluid,supply_temperature,target_temperature,mass_flowrate,capacity,hourly_generation)

# in_var
data_recovery = Info_HX_Recovery(delta_T_min, info_data)
# recovery
df_hx_processes = generate_heat_recovery(
    data_recovery)  # Heat Recovery module - input process and equipment  or only equipment

print(df_hx_processes)

### OPTION 2 - pinch analysis with processes - INPUT:processes, equipments
# Get all process and equipment from User
info_data = [process, boiler]  # all streams
# in_var
data_recovery = Info_HX_Recovery(delta_T_min, info_data)
# recovery full pinch
df_hx_processes = generate_heat_recovery(data_recovery)  # Heat Recovery module - input process and equipment  or only equipment

### OPTION 3 - pinch analysis with processes and isolated streams - INPUT:processes, equipments and isolated streams
# Get all process, equipment and random stream from User
info_data = [process, boiler, Stream(1, 'outflow', 'thermal_oil', 2, 200, 0.15 * 3600, 2, [1, 1, 1, 0])]  # all streams
# in_var
data_recovery = Info_HX_Recovery(delta_T_min, info_data)
# recovery full pinch
df_hx_processes = generate_heat_recovery(data_recovery)  # Heat Recovery module - input process and equipment  or only equipment


### OPTION 4 - equipment internal optimization - INPUT:only one equipment at a time
# Recover heat on equipment (flue gas and intake) - do this for each equipment individually
print('Analyze possible equipment/process internal recovery:')
reply = input('Y/N?: ')
reply = 'Y'
if reply == 'Y':
    equipments = []
    for object in info_data:
        if object.object_type == 'equipment':
            equipments.append(object)
    df_hx_equipments = []
    for equipment in equipments:
        info_data = [equipment]  # all streams
        print('yooo')
        print(info_data)
        print(equipment.streams)

        data_recovery = Info_HX_Recovery(delta_T_min, info_data)
        df_hx_new_equipment = generate_heat_recovery(data_recovery)
        df_hx_equipments.append(df_hx_new_equipment)  # Heat Recovery module







