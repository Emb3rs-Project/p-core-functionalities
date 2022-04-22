

from ....Source.characterization.Generate_Equipment.generate_boiler import Boiler
from ....utilities.kb import KB
from ....utilities.kb_data import kb

class GenerateBoiler():

    def __init__(self):

        ###################
        # MANDATORY INPUT
        self.id = 1000
        self.saturday_on = 0
        self.sunday_on = 0
        self.shutdown_periods = [[60, 75], [150, 155], [360, 365]]
        self.daily_periods = [[0, 14]]
        self.equipment_supply_temperature = 180
        self.open_closed_loop = 0  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = 'natural_gas'  # Fuel type  (Natural gas, Fuel oil, Biomass)

        # DEPENDING ON OTHER VARS
        # if open_closed_loop == 1:
        self.equipment_return_temperature = 50
        # If user does not want to put directly the nominal capacity, the processes fed by this equipment must be given
        self.supply_capacity = 7500
        self.processes = []

        ###################
        # OPTIONAL/EXPERT User inputs -  should be shown on the platform as default values
        self.global_conversion_efficiency = 0.88


def testGenerateBoiler():

    data = GenerateBoiler()
    input_data = {}
    input_data['platform'] = data.__dict__
    test = Boiler(input_data, KB(kb))

    print(test.streams[2]['supply_temperature'])

    """
    Expected:
    186.93045030383692
    """

