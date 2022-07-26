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
    """Get fluid properties

    Fluids and materials properties script. According to the called function, it is possible to get a fluid's density
    (rho), specific_heat (cp) and state (liquid, solid, gas)

    """

    kb_data: dict

    def cp(self, fluid_name, temperature):
        """ Get fluid cp

        Parameters
        ----------
        fluid_name : str
            Fluid name

        temperature : float
            Fluid temperature [ºC]

        Returns
        -------
        fluid_cp :
            Fluid cp [kJ/kg.K]

        """

        data = self.kb_data.get('medium_list')

        try:
            fluid_cp = float(data[fluid_name]['specific_heat_c0']) + float(
                data[fluid_name]['specific_heat_c1']) * temperature \
                       + float(data[fluid_name]['specific_heat_c2']) * temperature ** 2 + float(
                data[fluid_name]['specific_heat_c3']) * temperature ** 3

        except:
            raise Exception(fluid_name + ' does not exist in the Knowledge Base. '
                                     'Cp not known.')

        return fluid_cp


    def rho(self, fluid_name, temperature):
        """ Get fluid tho

        Parameters
        ----------
        fluid_name : str
            Fluid name

        temperature : float
            Fluid temperature [ºC]

        Returns
        -------
        rho : float
            Fluid density; [kg/m3]
        """

        data = self.kb_data.get('medium_list')

        try:
            rho = float(data[fluid_name]['density_c0']) + float(data[fluid_name]['density_c1']) * temperature \
                  + float(data[fluid_name]['density_c2']) * temperature ** 2 + float(data[fluid_name][
                                                                                         'density_c3']) * temperature ** 3
        except:
            raise Exception(fluid_name + ' does not exist in the Knowledge Base. '
                                         'Density not known.')


        return rho


    def state(self, fluid_name):
        """ Get fluid state

        Parameters
        ----------
        fluid_name : str
            Fluid name

        temperature : float
            Fluid temperature [ºC]

        Returns
        -------
        state : float
            Fluid state
        """

        data = self.kb_data.get('medium_list')

        try:
            state = data[fluid_name]['fluid_type']

        except:
            raise Exception(fluid_name + ' does not exist in the Knowledge Base. '
                                     'Fluid state (liquid, gas, solid) not known.')

        return state
