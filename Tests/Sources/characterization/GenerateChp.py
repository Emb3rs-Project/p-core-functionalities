

from ....Source.characterization.Generate_Equipment.generate_chp import Chp


class GenerateChp():

    def __init__(self):

        ###################
        # INPUT Mandatory
        self.id = 3000

        # Schedule
        self.saturday_on = 1
        self.sunday_on = 1
        self.shutdown_periods = [[60, 75], [150, 155], [360, 365]]
        self.daily_periods = [[9, 24]]

        # Generate_Equipment Characteristics FROM USER
        self.supply_temperature = 180
        self.open_closed_loop = 0  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = 'natural_gas'  # Fuel type  (Natural gas, Fuel oil, Biomass)

        # Generate_Equipment Characteristics FROM KB_General/USER
        self.global_conversion_efficiency = 0.8406
        self.return_temperature = 50

        ###################

        ###################################
        # If user does not want to put directly the nominal capacity, the processes fed by this boiler must be input - check in TESTS -> Source -> chracterization -> Process.py
        self.supply_capacity = 7500
        self.processes = []

        # Optional/Expert User inputs -  should be shown on the platform as default values
        self.equipment_sub_type = 'gas_engine'
        self.supply_fluid = 'steam'
        self.inflow_fluid = 'air'
        self.supply_fluid = 'oil'

        # user must introduce thermal/electric efficiency or both
        self.thermal_conversion_efficiency = 0.1

        # user must introduce thermal/electric supply capacity
        self.electrical_generation = 500




def testGenerateChp():

    data = GenerateChp()
    test = Chp(data)


    print(test.streams[2]['flowrate'])

    """
    print(test.streams[2]['flowrate'])

    Expected:
    280470.4035813954
    """

