
from Source.characterization.Process.process import Process

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

        self.inflow_data = [Inflow().__dict__]
        self.outflow_data = [Outflow().__dict__]


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
        self.target_temperature = 30
        self.fluid = 'oil'
        self.flowrate = 23
        self.fluid_cp = 2


def testProcess():

    process_data = Process_data()
    process = Process(process_data)