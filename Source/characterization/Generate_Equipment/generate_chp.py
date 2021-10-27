"""
##############################
INFO: Create CHP Object and characterize its streams.

##############################
INPUT: object with:

        # id - equipment id
        # supply_temperature [ºC]
        # return_temperature [ºC]
        # global_conversion_efficiency
        # fuel_type -  fuel type (natural_gas, fuel_oil, biomass, electricity)
        # saturday_on - 1 (yes)  or 0 (no)
        # sunday_on - 1 (yes)  or 0 (no)
        # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
        # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]

        IMPORTANT
        1) user can input electrical generation or supply heat capacity, with corresponding conversion efficiencies
                # thermal_conversion_efficiency (0 to 1) and supply_capacity [kW]
                # electrical_conversion_efficiency (0 to 1) and electrical_generation [kW]


        2) To compute excess heat characteristics the equipment supply capacity must be known.
        The user may choose to add directly the equipment supply_capacity or link processes with the equipment.
            # supply_capacity [kW]
            # processes - vector with processes [process_1,process_2,..]; each process contains dictionary with dictionaries of streams;

                Where, e.g, in process_1:
                    # process_1 = {'streams':[{stream_1_info},{stream_2_info},..]

##############################
OUTPUT: object CHP.

        IMPORTANT:
         # chp.streams important attribute for CF Internal Heat Recovery  and convert streams

"""

from General.Auxiliary_General.schedule_hour import schedule_hour
from General.Auxiliary_General.combustion import T_flue_gas,combustion_mass_flows
from General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from General.Auxiliary_General.stream import Stream
from KB_General.fluid_material import fluid_material_cp



class Chp():

    def __init__(self,in_var):

        # Defined Vars
        self.object_type = 'equipment'
        self.streams = []
        excess_heat_fluid = 'flue_gas'  # Excess heat fluid type
        inflow_supply_temperature = 20  # Ambient Temperature [ºC]
        excess_heat_target_temperature = 120  # flue_gas is usually cooled until 120ºC  due to the formation of condensates


        # INPUT
        self.id = in_var.id
        self.fuel_type = in_var.fuel_type  # Fuel type  (Natural gas, Fuel oil, Biomass)
        saturday_on = in_var.saturday_on
        sunday_on = in_var.sunday_on
        shutdown_periods = in_var.shutdown_periods
        daily_periods = in_var.daily_periods
        return_temperature = in_var.return_temperature
        supply_temperature = in_var.supply_temperature


        if supply_temperature < 100:
            self.equipment_sub_type = 'chp_gas_engine'
            supply_fluid = 'water'
            inflow_fluid = 'air'

        else:
            self.equipment_sub_type = 'chp_gas_turbine'
            supply_fluid = 'water'
            inflow_fluid = 'water'


        try:
            self.global_conversion_efficiency = in_var.global_conversion_efficiency
            self.thermal_conversion_efficiency = in_var.thermal_conversion_efficiency
            self.electrical_conversion_efficiency = self.global_conversion_efficiency - self.thermal_conversion_efficiency
        except:
            self.global_conversion_efficiency = in_var.global_conversion_efficiency
            self.electrical_conversion_efficiency = in_var.electrical_conversion_efficiency
            self.electrical_conversion_efficiency = self.global_conversion_efficiency - self.electrical_conversion_efficiency

        try:
            self.supply_capacity = in_var.supply_capacity  # heat [kW]
            self.electrical_generation = self.supply_capacity/self.thermal_conversion_efficiency*self.electrical_conversion_efficiency # [kW]
        except:
            self.electrical_generation = in_var.electrical_generation  # electrical [kW]
            self.supply_capacity = self.electrical_generation/self.electrical_conversion_efficiency*self.thermal_conversion_efficiency # [kW]

        # schedule
        schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)

        # get supply capacity to compute excees heat characteristics
        try:
            supply_capacity = in_var.supply_capacity
            self.supply_capacity = supply_capacity
        except:
            processes = in_var.processes
            total_yearly_supply_capacity = 0

            if processes != []:
                for process in processes:
                    for stream in process['streams']:
                        if stream['stream_type'] != 'outflow':
                           total_yearly_supply_capacity += stream.capacity * sum(stream.schedule)

                self.supply_capacity = total_yearly_supply_capacity / (sum(schedule))
            else:
                self.supply_capacity = 0

        # fuel consumption [kg/h]
        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(self.supply_capacity,
                                                                    self.global_conversion_efficiency,
                                                                    self.fuel_type)

        thermal_capacity = self.electrical_generation / self.electrical_conversion_efficiency


        # Excess Heat
        # supply temperature [ºC]
        excess_heat_supply_temperature, inflow_target_temperature = T_flue_gas(self.supply_capacity,
                                                                         self.fuel_type, fuel_consumption,
                                                                         m_flue_gas)

        # Inflow
        inflow_flowrate = m_air
        inflow_fluid_cp = fluid_material_cp(inflow_fluid,(inflow_supply_temperature+inflow_target_temperature)/2)
        inflow_capacity = inflow_flowrate * (inflow_target_temperature - inflow_supply_temperature) * inflow_fluid_cp/3600  # [kW]

        # Supply Capacity [kW]
        excess_heat_supply_capacity = thermal_capacity - self.supply_capacity - self.electrical_generation

        # Flowrate [kg/h]
        excess_heat_flowrate = compute_flow_rate(excess_heat_fluid,
                                                 excess_heat_supply_capacity,
                                                 excess_heat_supply_temperature,
                                                 excess_heat_target_temperature)

        # Supply Heat
        # Flowrate [kg/h]
        supply_flowrate = compute_flow_rate(supply_fluid,
                                            self.supply_capacity,
                                            supply_temperature,
                                            return_temperature)

        # inflow defined
        self.streams.append(Stream(self.id,
                                   'inflow',
                                   inflow_fluid,
                                   inflow_supply_temperature,
                                   inflow_target_temperature,
                                   inflow_flowrate,
                                   inflow_capacity,
                                   schedule))

        self.streams.append(Stream(self.id,
                                   'supply_heat',
                                   supply_fluid,
                                   return_temperature,
                                   supply_temperature,
                                   supply_flowrate,
                                   self.supply_capacity,
                                   schedule))

        self.streams.append(Stream(self.id,
                                   'excess_heat',
                                   excess_heat_fluid,
                                   excess_heat_supply_temperature,
                                   excess_heat_target_temperature,
                                   excess_heat_flowrate,
                                   excess_heat_supply_capacity,
                                   schedule))




