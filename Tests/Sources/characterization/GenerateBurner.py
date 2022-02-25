

from ....Source.characterization.Generate_Equipment.generate_burner import Burner
from ....utilities.kb import KB
from ....utilities.kb_data import kb

class GenerateBurner():

    def __init__(self):

        ###################
        # MANDATORY INPUT
        self.id = 1000
        self.saturday_on = 0
        self.sunday_on = 0
        self.shutdown_periods = [[60, 75], [150, 155], [360, 365]]
        self.daily_periods = [[0, 14]]
        self.fuel_type = 'biomass'  # Fuel type  (Natural gas, Fuel oil, Biomass)
        self.excess_heat_supply_temperature = 400  # RECOVERABLE EXCESS HEAT
        self.excess_heat_target_temperature = 120
        self.excess_heat_flowrate = 20

        # DEPENDING ON OTHER VARS
        # If user does not want to put directly the nominal capacity, the processes fed by this equipment must be given
        self.supply_capacity = 7500
        self.processes = []

        ###################
        # Optional/Expert User inputs -  should be shown on the platform as default values
        self.global_conversion_efficiency = 0.9



def testGenerateBurner():

    data = GenerateBurner()
    input_data = {}
    input_data['platform'] = data.__dict__
    test = Burner(input_data, KB(kb))


    print(test.streams[0]['capacity'])

    """

    Expected:
    511.4306137027777
    """

