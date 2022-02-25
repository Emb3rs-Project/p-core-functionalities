"""
alisboa/jmcunha


##############################
INFO: Fluids and materials properties script. According to the called function, it is possible to get a fluid's density
      (rho), specific_heat (cp) and state (liquid, solid, gas)


##############################
INPUT:
        # fluid_name
        # temperature - only in fluid_material_cp and fluid_material_rho  [ºC]

##############################
OUTPUT: according to the called function:

        # fluid_cp  [kJ/kg.K]
        # state - e.g. liquid, solid, gas
        # rho  [kg/m3]


"""

from dataclasses import dataclass



@dataclass
class Medium:

    kb_data: dict

    def cp(self, fluid_name, temperature):

        data = self.kb_data.get('medium_list')

        try:
            fluid_cp = float(data[fluid_name]['specific_heat_c0']) + float(
                data[fluid_name]['specific_heat_c1']) * temperature \
                       + float(data[fluid_name]['specific_heat_c2']) * temperature ** 2 + float(
                data[fluid_name]['specific_heat_c3']) * temperature ** 3

        except:
            print(fluid_name)
            print('fluid does not exist in db. default: fluid_cp = 1')
            fluid_cp = 1

        return fluid_cp


    def rho(self, fluid_name, temperature):

        data = self.kb_data.get('medium_list')

        try:
            rho = float(data[fluid_name]['density_c0']) + float(data[fluid_name]['density_c1']) * temperature \
                  + float(data[fluid_name]['density_c2']) * temperature ** 2 + float(data[fluid_name][
                                                                                         'density_c3']) * temperature ** 3
        except:
            print('fluid does not exist in db. default: rho = 1')
            rho = 1

        return rho


    def state(self, fluid_name):

        data = self.kb_data.get('medium_list')

        try:
            state = data[fluid_name]['fluid_type']

        except:
            print('fluid state does not exist in db. default: state = liquid')
            state = 'liquid'

        return state
