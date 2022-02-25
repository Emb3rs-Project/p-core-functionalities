

from ....Source.characterization.Generate_Equipment.generate_chp import Chp
from ....utilities.kb import KB
from ....utilities.kb_data import kb

class GenerateChp():

    def __init__(self):

        ###################
        # MANDATORY INPUT
        self.id = 3000
        self.saturday_on = 1
        self.sunday_on = 1
        self.shutdown_periods = [[60, 75], [150, 155], [360, 365]]
        self.daily_periods = [[9, 24]]
        self.supply_temperature = 180
        self.open_closed_loop = 0  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = 'natural_gas'  # Fuel type  (Natural gas, Fuel oil, Biomass)
        self.equipment_sub_type = 'chp_gas_engine'  # Fuel type  (Natural gas, Fuel oil, Biomass)
        self.global_conversion_efficiency = 0.8406


        # DEPENDING ON OTHER VARS
        # If user does not want to put directly the nominal capacity, the processes fed by this boiler must be input - check in TESTS -> Source -> chracterization -> Process.py
        self.supply_capacity = 7500
        self.processes = []

        # user must introduce thermal/electric efficiency or both
        self.thermal_conversion_efficiency = 0.1

        # user must introduce thermal/electric supply capacity
        self.electrical_generation = 500




def testGenerateChp():

    data = GenerateChp()
    input_data = {}
    input_data['platform'] = data.__dict__
    test = Chp(input_data, KB(kb))


    print(test.streams[0]['capacity'])

    """
    Expected:
    211.258538887277
    """

