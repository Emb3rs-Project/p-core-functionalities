

from ....Source.characterization.Generate_Equipment.generate_cooling_equipment import Cooling_Equipment
from ....utilities.kb import KB
from ....utilities.kb_data import kb

class GenerateCoolingEquipment():

    def __init__(self):

        ###################
        # INPUT Mandatory
        self.id = 3000
        self.saturday_on = 1
        self.sunday_on = 1
        self.shutdown_periods = [[60, 75], [150, 155], [360, 365]]
        self.daily_periods = [[9, 24]]
        self.equipment_sub_type = 'compression_chiller'

        # DEPENDING ON OTHER VARS
        # If user does not want to put directly the nominal capacity, the processes fed by this boiler must be input - check in TESTS -> Source -> chracterization -> Process.py
        self.supply_capacity = 7500
        self.processes = []




def testGenerateCoolingEquipment():

    data = GenerateCoolingEquipment()
    input_data = {}
    input_data['platform'] = data.__dict__
    test = Cooling_Equipment(input_data, KB(kb))

    print(test.streams[0]['capacity'])

    """   
    Expected:
    5978.8359788359785
    """



