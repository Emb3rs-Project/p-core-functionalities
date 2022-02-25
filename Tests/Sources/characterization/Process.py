
from ....Source.characterization.Process.process import Process
from ....utilities.kb import KB
from ....utilities.kb_data import kb

class Process_data():

    def __init__(self):

        self.id = 55
        self.equipment = 1000
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
            'fluid':'oil',
            'fluid_cp':2,
            'supply_temperature':10
            }

        inflow_stream_2 = {
            'flowrate':100,
            'fluid':'oil',
            'fluid_cp':2,
            'supply_temperature':10
            }

        outflow_stream_1 = {
            'flowrate':100,
            'fluid_cp':2,
            'fluid':'oil',
            'target_temperature':45
            }

        self.startup_data = [startup_stream_1]
        self.maintenance_data = [maintenance_stream_1]
        self.inflow_data = [inflow_stream_1, inflow_stream_2]
        self.outflow_data = [outflow_stream_1]




def testProcess():

    process_data = Process_data()
    input_data = {}
    input_data['platform'] = process_data.__dict__
    process = Process(input_data,KB(kb))

    for stream in process.streams:
        print(stream['stream_type'])

    """    
    Expected:
    startup
    maintenance
    inflow
    inflow
    outflow
    """

