"""
alisboa/jmcunha


##############################
INFO: It were created correlations for the turnkey, om_fix, and equipment efficiency based on the various info from suppliers
      and the literature. In this script, these equipment characteristics are obtained according to its characteristic parameter
      (e.g., boilers - power [kW]; hx_plate - area [m2],...)


##############################
INPUT:
        # equipment - equipment name
        # equipment_char -  characteristic parameter of the equipment ( check Json_file/equipment_details.json for more info)


##############################
OUTPUT:
        # global_conversion_efficiency  []
        # om_fix  [€/kW]
        # turnkey  [€]


"""


from dataclasses import dataclass


@dataclass
class EquipmentDetails:

    kb_data: dict

    def get_values(self, equipment, equipment_char):

        global_conversion_efficiency = 1
        electrical_conversion_efficiency = 1
        om_fix = 1
        turnkey = 1

        data = self.kb_data.get("equipment_details")

        try:
            turnkey = float(data[equipment]['turnkey_cost_S']) + float(
                data[equipment]['turnkey_cost_c']) * equipment_char ** float(data[equipment]['turnkey_cost_n'])

            om_fix = float(data[equipment]['fixed_om_c']) * turnkey ** float(data[equipment]['fixed_om_n'])

            global_conversion_efficiency = float(data[equipment]['global_conversion_efficiency_S']) + float(
                data[equipment]['global_conversion_efficiency_c']) * equipment_char ** float(
                data[equipment]['global_conversion_efficiency_n'])
            electrical_conversion_efficiency = float(data[equipment]['electrical_efficiency_c']) * equipment_char ** float(
                data[equipment]['electrical_efficiency_n'])
        except:
            raise Exception("Equipment not in the Knowledge Base." )


        # special case CHP
        if equipment == 'chp_gas_engine' or equipment == 'chp_gas_turbine':
            global_conversion_efficiency = [global_conversion_efficiency, electrical_conversion_efficiency]  # thermal and electrical efficiency

        return global_conversion_efficiency, om_fix, turnkey
