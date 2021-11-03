

from Source.characterization.Generate_Equipment.generate_burner import Burner


class GenerateBurner():

    def __init__(self):

        # Defined var
        self.equipment_sub_type = 'burner'


        ###################
        # INPUT
        self.id = 1000

        # Schedule
        self.saturday_on = 0
        self.sunday_on = 0
        self.shutdown_periods = [[60, 75], [150, 155], [360, 365]]
        self.daily_periods = [[0, 14]]

        # Generate_Equipment Characteristics FROM USER
        self.supply_temperature = 180

        ###################################
        # If user does not want to put directly the nominal capacity, the processes fed by this boiler must be input - check in TESTS -> Source -> chracterization -> Process.py
        self.supply_capacity = 7500
        self.processes = []

        ###################
        # Optional/Expert User inputs -  should be shown on the platform as default values
        self.fuel_type = 'natural_gas'  # Fuel type  (Natural gas, Fuel oil, Biomass)
        self.global_conversion_efficiency = 0.9



def testGenerateBurner():

    data = GenerateBurner()
    test = Burner(data)


    print(test.streams[1]['flowrate'])

    """
    print(test.streams[1]['flowrate'])

    Expected:
    18234.66484501108
    """

