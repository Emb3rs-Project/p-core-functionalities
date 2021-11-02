

from Source.characterization.Generate_Equipment.generate_burner import Burner


class GenerateBurner():

    def __init__(self):

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
        self.open_closed_loop = 0  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = 'natural_gas'  # Fuel type  (Natural gas, Fuel oil, Biomass)

        # Generate_Equipment Characteristics FROM KB_General/USER
        self.return_temperature = 50

        ###################################
        # If user does not want to put directly the nominal capacity, the processes fed by this boiler must be input - check in TESTS -> Source -> chracterization -> Process.py
        self.supply_capacity = 7500
        self.processes = []

        ###################
        # Optional/Expert User inputs -  should be shown on the platform as default values
        self.equipment_sub_type = 'steam_boiler'
        self.supply_fluid = 'steam'
        self.global_conversion_efficiency = 0.95




def testGenerateBurner():

    data = GenerateBoiler()
    test = Boiler(data)


    print(test.streams[2]['flowrate'])

    """
    print(test.streams[2]['flowrate'])

    Expected:
    54662.071524819985
    """

