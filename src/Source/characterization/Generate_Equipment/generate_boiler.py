from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.combustion_mass_flows import combustion_mass_flows
from ....General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....KB_General.medium import Medium
from ....KB_General.equipment_details import EquipmentDetails
from ....utilities.kb import KB


class Boiler:
    """Create Boiler Object and characterize its streams

    Attributes
    ----------
    id : int
        Equipment ID

    object_type : str
        DEFAULT = "equipment"

    streams : list
        Data of the streams associated to this equipment

    fuel_type : str
        Fuel type

    supply_capacity : float
        Equipment supply capacity [kW]

    global_conversion_efficiency : float
        Equipment efficiency []

    equipment_sub_type  : str
        Equipment designation

    Parameters
    ----------
    in_var : dict
        Equipment characterization data, with the following keys:

            id : int
                Equipment ID

            object_type : str
                Equipment type: "process", "boiler","chp", "burner", "cooling_equipment", "stream"

            fuel_type : str
                Fuel type

            boiler_equipment_sub_type: str
                Options: "steam_boiler" or "hot_water_boiler"

            supply_capacity : float
                Equipment supply capacity [kW]

            global_conversion_efficiency : float
                Conversion efficiency []

            processes : list
                List of processes objects associated to the equipment

            equipment_supply_temperature : float
                Equipment circuit supply temperature [ºC]

            open_closed_loop : int
                Whether is a opens or closed loop boiler; 1 (yes)  or 0 (no)

            saturday_on : int
                If it is available on Saturday []; 1 (yes)  or 0 (no)

            sunday_on : int
                If it is available on Sunday []; 1 (yes)  or 0 (no)

            shutdown_periods : list
                List with lists of periods of days it is not available [day]; e.g. [[130,140],[289,299]]

            daily_periods : list
                List with lists of hourly periods it is available [h]; e.g. [[8,12],[15,19]]

            equipment_return_temperature : float, optional
                Equipment working fluid return temperature [ºC]

            boiler_supply_flowrate : float, optional
                Equipment working fluid mass flowrate. Only for steam boilers.

    kb : dict
        Knowledge Base data


    """

    def __init__(self, in_var, kb: KB):

        ############################################################################################
        # KB
        medium = Medium(kb)
        equipment_details = EquipmentDetails(kb)

        # Defined Vars
        self.object_type = 'equipment'
        self.streams = []
        inflow_fluid = 'air'
        inflow_supply_temperature = 20  # Ambient Temperature
        excess_heat_fluid = 'flue_gas'  # Excess heat fluid type
        excess_heat_target_temperature = 120  # flue_gas is usually cooled until 120ºC  due to the formation of condensates
        inflow_target_temperature = 80
        supply_fluid = "water"  # this is only used in the PINCH -> water for both steam/hot water boiler

        ############################################################################################
        # INPUT
        self.id = in_var['id']  # equipment ID
        self.fuel_type = in_var['fuel_type']  # Fuel type  (Natural gas, Fuel oil, Biomass)
        self.equipment_sub_type = in_var['boiler_equipment_sub_type']
        self.supply_capacity = in_var['supply_capacity']
        self.global_conversion_efficiency = in_var['global_conversion_efficiency']
        processes = in_var['processes']
        supply_temperature = in_var['equipment_supply_temperature']
        open_closed_loop = in_var['open_closed_loop']  # Open heating circuit? (1-Yes, 0-No)
        saturday_on = in_var['saturday_on']
        sunday_on = in_var['sunday_on']
        shutdown_periods = in_var['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var['daily_periods']  # e.g: [[8,12],[15,19]]

        if open_closed_loop == 1:
            return_temperature = 20  # Ambient Temperature
        else:
            return_temperature = in_var['equipment_return_temperature']

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

        # efficiency
        if self.global_conversion_efficiency is None:
            self.global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details.get_values(
                self.equipment_sub_type, self.supply_capacity)

        # fuel consumption
        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(kb,
                                                                    self.supply_capacity,
                                                                    self.global_conversion_efficiency,
                                                                    self.fuel_type)

        # supply heat stream
        if supply_temperature > 100:
            supply_flowrate = in_var['boiler_supply_flowrate']  # [kg/h]
            supply_capacity_water = supply_flowrate * 4.2 * (100 - return_temperature)
        else:
            supply_flowrate = compute_flow_rate(kb,
                                                supply_fluid,
                                                self.supply_capacity,
                                                supply_temperature,
                                                return_temperature)

            supply_capacity_water = self.supply_capacity

        thermal_capacity = self.supply_capacity / self.global_conversion_efficiency

        # excess heat stream
        excess_heat_supply_capacity = thermal_capacity - self.supply_capacity
        excess_heat_flowrate = m_flue_gas
        excess_heat_supply_temperature = excess_heat_target_temperature + excess_heat_supply_capacity / (
                    m_flue_gas / 3600 * 1.4)

        # inflow stream
        inflow_flowrate = m_air
        inflow_fluid_cp = medium.cp(inflow_fluid, (inflow_supply_temperature + inflow_target_temperature) / 2)
        inflow_capacity = inflow_flowrate * (
                    inflow_target_temperature - inflow_supply_temperature) * inflow_fluid_cp / 3600  # [kW]

        ############################################################
        # CHARACTERIZE STREAMS
        # air inflow
        self.streams.append(stream_industry('boiler air inflow',
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
                                            eff_equipment=1))

        # supply heat
        self.streams.append(stream_industry('boiler circuit',
                                            self.id,
                                            'supply_heat',
                                            supply_fluid,
                                            return_temperature,
                                            supply_temperature,
                                            supply_flowrate,
                                            supply_capacity_water,
                                            schedule,
                                            stream_id=2,
                                            fuel=self.fuel_type,
                                            eff_equipment=self.global_conversion_efficiency
                                            ))

        # excess heat
        self.streams.append(stream_industry('boiler flue gas',
                                            self.id,
                                            'excess_heat',
                                            excess_heat_fluid,
                                            excess_heat_supply_temperature,
                                            excess_heat_target_temperature,
                                            excess_heat_flowrate,
                                            excess_heat_supply_capacity,
                                            schedule,
                                            stream_id=3,
                                            fuel="none",
                                            eff_equipment=None
                                            ))
