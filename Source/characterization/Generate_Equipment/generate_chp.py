from ....General.Auxiliary_General.get_country import get_country
from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.combustion_mass_flows import combustion_mass_flows
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....KB_General.medium import Medium
from ....utilities.kb import KB
from ....KB_General.fuel_properties import FuelProperties


class Chp:

    def __init__(self, in_var, kb: KB):

        """
        Create CHP Object and characterize its streams.

        :param in_var: ``dict``: CHP characterization data

                - id: ``int``: equipment ID []
                - fuel_type: ``str``: fuel type []; (natural_gas, fuel_oil, biomass)
                - supply_capacity: ``float``: [OPTIONAL] equipment supply capacity [kW]
                - electrical_generation: ``float``: [OPTIONAL] equipment electrical generation capacity [kW]
                - global_conversion_efficiency: ``float``: equipment efficiency []
                - thermal_conversion_efficiency: ``float``: [OPTIONAL] CHP thermal efficiency []
                - electrical_conversion_efficiency: ``float``: CHP electrical efficiency []
                - saturday_on: ``int``: if it is available on Saturday []; 1 (yes)  or 0 (no)
                - sunday_on: ``int``: if it is available on Sunday []; 1 (yes)  or 0 (no)
                - shutdown_periods: ``list``: list with lists of periods of days it is not available [day]; e.g. [[130,140],[289,299]]
                - daily_periods: ``list``: list with lists of hourly periods it is available [h]; e.g. [[8,12],[15,19]]
                - location: ``list``: [latitude, longitude]
                - fuel_price: ``float``: [OPTIONAL]
                - fuel_co2_emissions: ``float``: [OPTIONAL]

        :param kb: Knowledge Base data

        """

        ############################################################################################
        # KB
        medium = Medium(kb)

        # Defined Vars
        self.object_type = 'equipment'
        self.streams = []
        inflow_supply_temperature = 20  # Ambient Temperature [ºC]
        inflow_target_temperature = 80
        inflow_fluid = 'air'

        ############################################################################################
        # INPUT
        self.id = in_var['id']  # equipment ID
        self.fuel_type = in_var['fuel_type']  # Fuel type  (Natural gas, Fuel oil, Biomass)

        self.equipment_sub_type = 'chp'
        self.supply_capacity = in_var['supply_capacity']
        self.electrical_generation = in_var['electrical_generation']
        self.global_conversion_efficiency = in_var['global_conversion_efficiency']
        self.thermal_conversion_efficiency = in_var['thermal_conversion_efficiency']
        self.electrical_conversion_efficiency = in_var['electrical_conversion_efficiency']
        processes = in_var['processes']
        saturday_on = in_var['saturday_on']
        sunday_on = in_var['sunday_on']
        shutdown_periods = in_var['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var['daily_periods']  # e.g: [[8,12],[15,19]]

        ############################################################################################
        # COMPUTE
        # schedule
        schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)

        # efficiency
        if self.thermal_conversion_efficiency is None:
            self.thermal_conversion_efficiency = self.global_conversion_efficiency - self.electrical_conversion_efficiency
        elif self.electrical_conversion_efficiency is None:
            self.electrical_conversion_efficiency = self.global_conversion_efficiency - self.thermal_conversion_efficiency

        # supply capacity
        if self.supply_capacity is None:
            if self.electrical_generation is not None:
                self.supply_capacity = self.electrical_generation / self.electrical_conversion_efficiency * self.thermal_conversion_efficiency  # [kW]
            else:
                self.total_yearly_supply_capacity = 0
                for process in processes:
                    for stream in process['streams']:
                        if stream['stream_type'] != 'outflow':
                            self.total_yearly_supply_capacity += stream['capacity'] * sum(stream['schedule'])
                self.supply_capacity = self.total_yearly_supply_capacity / (sum(schedule))

        # fuel
        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(kb,
                                                                    self.supply_capacity,
                                                                    self.global_conversion_efficiency,
                                                                    self.fuel_type)

        # inflow stream
        inflow_flowrate = m_air
        inflow_fluid_cp = medium.cp(inflow_fluid, (inflow_supply_temperature + inflow_target_temperature) / 2)
        inflow_capacity = inflow_flowrate * (
                inflow_target_temperature - inflow_supply_temperature) * inflow_fluid_cp / 3600  # [kW]

        ############################################################################################
        # CHARACTERIZE STREAMS
        # inflow
        self.streams.append(stream_industry('chp air inflow',
                                            self.id,
                                            'inflow',
                                            inflow_fluid,
                                            inflow_supply_temperature,
                                            inflow_target_temperature,
                                            inflow_flowrate,
                                            inflow_capacity,
                                            schedule,
                                            stream_id=1,
                                            fuel=self.fuel_type,
                                            eff_equipment=1
                                            ))
