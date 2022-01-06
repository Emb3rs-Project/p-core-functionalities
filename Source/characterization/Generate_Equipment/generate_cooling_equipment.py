"""
alisboa/jmcunha

##############################
INFO: Create Cooling Equipment Object and characterize its streams.

##############################
INPUT: object with:

        # id - equipment id
        # equipment_sub_type - 'co2_chiller', 'cooling_tower', 'air_cooled_chiller', 'water_cooled_chiller'
        # supply_temperature [ºC]
        # return_temperature [ºC]
        # global_conversion_efficiency - COP
        # saturday_on - 1 (yes)  or 0 (no)
        # sunday_on - 1 (yes)  or 0 (no)
        # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
        # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]

        !!!
        IMPORTANT
        1) Optional input - 'co2_chiller' :
            # excess_heat_supply_temperature
            # excess_heat_target_temperature

        2) Optional input - chillers (except co2_chiller) :
            # supply_fluid

        3) Mandatory input - To compute excess heat characteristics the equipment supply capacity must be known.
        The user may choose to add directly the equipment supply_capacity or link processes with the equipment.
            # supply_capacity [kW]
            # processes - vector with processes [process_1,process_2,..]; each process contains dictionary with dictionaries of streams;

                Where, e.g, in process_1:
                    # process_1 = {'streams':[{stream_1_info},{stream_2_info},..]


##############################
OUTPUT: object Cooling Equipment.

        !!!
        IMPORTANT:
         # only 'co2_chiller' has excess heat. Heat recovered before gas cooler
         # cooling_equipment.streams important attribute for simulation - Heat Recovery


"""

from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from ....General.Auxiliary_General.stream_industry import stream_industry


class Cooling_Equipment():

    def __init__(self, in_var):

        # Defined Vars
        self.object_type = 'equipment'
        self.streams = []
        self.fuel_type = 'electricity'  # Electricity

        # INPUT ---
        self.id = in_var.id  # Equipment ID
        self.equipment_sub_type = in_var.equipment_sub_type  # Equipment type (co2_chiller/ cooling_tower/ air_cooled_chiller/
        # water_cooled_chiller)
        saturday_on = in_var.saturday_on
        sunday_on = in_var.sunday_on
        shutdown_periods = in_var.shutdown_periods
        daily_periods = in_var.daily_periods

        if self.equipment_sub_type == 'co2_chiller':
            supply_fluid = 'R744'
            self.global_conversion_efficiency = in_var.global_conversion_efficiency  # COP
            excess_heat_fluid = 'water'  # excess heat fluid type
            excess_heat_supply_temperature = 90  # discharge temperature [ºC]
            excess_heat_target_temperature = 60  # gas cooler entry temperature [ºC]

        else:
            self.global_conversion_efficiency = in_var.global_conversion_efficiency  # COP
            supply_temperature = in_var.supply_temperature
            return_temperature = in_var.return_temperature
            try:
                supply_fluid = in_var.supply_fluid
            except:
                supply_fluid = 'water'

        # schedule
        schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)

        # get supply capacity to compute excess heat characteristics
        try:
            self.supply_capacity = in_var.supply_capacity
        except:
            processes = in_var.processes
            self.total_yearly_supply_capacity = 0

            if processes != []:
                for process in processes:
                    for stream in process['streams']:
                        if stream['stream_type'] != 'outflow':
                            self.total_yearly_supply_capacity += stream.capacity * sum(stream.schedule)

                self.supply_capacity = self.total_yearly_supply_capacity / (sum(schedule))
            else:
                self.supply_capacity = 0

        # Supply Heat
        # flowrate [kg/h]
        supply_flowrate = compute_flow_rate(supply_fluid,
                                            self.supply_capacity,
                                            return_temperature,
                                            supply_temperature)

        # Excess Heat
        if self.equipment_sub_type == 'co2_chiller':
            # capacity [kW]
            excess_heat_supply_capacity = self.supply_capacity * 1.520

            # flowrate [kg/h]
            excess_heat_flowrate = compute_flow_rate(excess_heat_fluid,
                                                     excess_heat_supply_capacity,
                                                     excess_heat_supply_temperature,
                                                     excess_heat_target_temperature)
        else:
            excess_heat_supply_capacity = 0
            excess_heat_flowrate = 0

        # electrical consumption [kW]
        fuel_consumption = self.supply_capacity / self.global_conversion_efficiency

        # equipment streams
        # supply heat
        self.streams.append(stream_industry(self.id,
                                            'supply_heat',
                                            supply_fluid,
                                            return_temperature,
                                            supply_temperature,
                                            supply_flowrate,
                                            self.supply_capacity,
                                            schedule))

        # excess heat
        if self.equipment_sub_type == 'co2_chiller':
            self.streams.append(stream_industry(self.id,
                                                'excess_heat',
                                                excess_heat_fluid,
                                                excess_heat_supply_temperature,
                                                excess_heat_target_temperature,
                                                excess_heat_flowrate,
                                                excess_heat_supply_capacity,
                                                schedule))
