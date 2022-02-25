"""
alisboa/jmcunha


##############################
INFO: Receives heatx exchanger working fluids and return appropriate heat exchanger and u value.


##############################
INPUT:
        # fluids to be analyzed: fluid_1, fluid_2


##############################
OUTPUT:
        # hx_type - e.g. hx_kettle_boiler, hx_economizer, hx_plate
        # hx_u_value  [W/m2.K]


"""


from dataclasses import dataclass

@dataclass
class HxData:

    kb_data: dict

    def get_values(self,fluid_1, fluid_2):

        data = self.kb_data.get('medium_list')

        # get fluid 1 state
        try:
            state_1 = data[fluid_1]['fluid_type']
        except:
            print('fluid does not exist in db. state = liquid')
            state_1 = 'liquid'

        # get fluid 2 state
        try:
            state_2 = data[fluid_2]['fluid_type']
        except:
            print('fluid does not exist in db. state = liquid')
            state_2 = 'liquid'

        # get hx values
        if state_1 == 'liquid' and state_2 == 'liquid':
            hx_type = 'hx_plate'
            hx_u_value = 2000

        elif (state_1 == 'flue_gas' and state_2 == 'liquid') or (state_1 == 'liquid' and state_2 == 'flue_gas') or  (state_1 == 'gas' and state_2 == 'flue_gas') or  (state_1 == 'flue_gas' and state_2 == 'gas'):
            hx_type = 'hx_economizer'
            hx_u_value = 50

        elif (state_1 == 'liquid' and state_2 == 'steam') or (state_1 == 'steam' and state_2 == 'liquid'):
            hx_type = 'hx_kettle_boiler'
            hx_u_value = 800

        else:
            print('combination of liquids not in db')
            hx_type = 'hx_plate'
            hx_u_value = 800

        return hx_type, hx_u_value
