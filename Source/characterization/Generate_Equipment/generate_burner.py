from ....General.Auxiliary_General.get_country import get_country
from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.combustion_mass_flows import combustion_mass_flows
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....KB_General.medium import Medium
from ....utilities.kb import KB
from ....KB_General.fuel_properties import FuelProperties


class Burner:

    def __init__(self, in_var, kb: KB):
        """
        Create Burner Object and characterize its streams.

        :param in_var: ``dict``: burner characterization data with the following keys:

                - id: ``int``: equipment ID []
                - burner_equipment_sub_type: ``str``: if direct_burner or indirect_burner
                - fuel_type: ``str``: fuel type []; (natural_gas, fuel_oil, biomass, electricity)
                - global_conversion_efficiency: ``float``: equipment efficiency []
                - supply_capacity: ``float``: equipment supply capacity [kW]
                - burner_excess_heat_supply_temperature: ``float``: recoverable excess heat supply/initial temperature [ºC]
                - burner_excess_heat_flowrate: ``float``: recoverable excess heat supply/initial mass flowrate [kg/h]
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
        inflow_fluid = 'air'
        inflow_supply_temperature = 20  # ambient temperature
        inflow_target_temperature = 80  # [ºC]

        ############################################################################################
        # INPUT
        self.id = in_var['id']  # equipment ID
        self.equipment_sub_type = in_var['burner_equipment_sub_type']  # direct_burner or indirect_burner
        self.fuel_type = in_var['fuel_type']  # Fuel type  (Natural gas, Fuel oil, Biomass)
        self.global_conversion_efficiency = in_var['global_conversion_efficiency']
        self.supply_capacity = in_var['supply_capacity']
        processes = in_var['processes']
        excess_heat_supply_temperature = in_var['burner_excess_heat_supply_temperature']
        excess_heat_flowrate = in_var['burner_excess_heat_flowrate']
        saturday_on = in_var['saturday_on']
        sunday_on = in_var['sunday_on']
        shutdown_periods = in_var['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var['daily_periods']  # e.g: [[8,12],[15,19]]

        if self.global_conversion_efficiency is None:
            self.global_conversion_efficiency = 0.80

        if self.equipment_sub_type == 'direct_burner':
            supply_fluid = 'flue_gas'  # Excess heat fluid type
            excess_heat_target_temperature = 120
        else:
            supply_fluid = 'air'  # Excess heat fluid type
            excess_heat_target_temperature = 25

        ############################################################################################
        # COMPUTE
        # schedule
        schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)

        # supply capacity
        if self.supply_capacity is None:
            self.total_yearly_supply_capacity = 0
            for process in processes:
                for stream in process['streams']:
                    if stream['stream_type'] != 'outflow':
                        self.total_yearly_supply_capacity += stream['capacity'] * sum(stream['schedule'])

            self.supply_capacity = self.total_yearly_supply_capacity / (sum(schedule))


        # fuel consumption
        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(kb,
                                                                    self.supply_capacity,
                                                                    self.global_conversion_efficiency,
                                                                    self.fuel_type)


        # inflow stream
        inflow_flowrate = m_air
        inflow_fluid_cp = medium.cp(inflow_fluid, (inflow_supply_temperature + inflow_target_temperature) / 2)
        inflow_capacity = inflow_flowrate * (inflow_target_temperature - inflow_supply_temperature) \
                          * inflow_fluid_cp / 3600  # [kW]

        # excess heat stream
        flue_gas_cp = medium.cp(supply_fluid, excess_heat_supply_temperature)

        if excess_heat_target_temperature > excess_heat_supply_temperature:
            excess_heat_supply_capacity = 0
        else:
            excess_heat_supply_capacity = excess_heat_flowrate/3600 * abs(excess_heat_supply_temperature - excess_heat_target_temperature) * flue_gas_cp

        # GET STREAMS
        # air inflow
        self.streams.append(stream_industry('burner air inflow',
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

        if excess_heat_target_temperature < excess_heat_supply_temperature:
            self.streams.append(stream_industry('burner excess heat',
                                                self.id,
                                                'excess_heat',
                                                supply_fluid,
                                                excess_heat_supply_temperature,
                                                excess_heat_target_temperature,
                                                excess_heat_flowrate,
                                                excess_heat_supply_capacity,
                                                schedule,
                                                stream_id=2,
                                                fuel="none",
                                                eff_equipment=None
                                                ))
