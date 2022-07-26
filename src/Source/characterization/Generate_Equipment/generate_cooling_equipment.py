from ....General.Auxiliary_General.compute_cop_eer import compute_cop_eer
from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....KB_General.medium import Medium
from ....KB_General.equipment_details import EquipmentDetails
from ....utilities.kb import KB


class Cooling_Equipment:
    """Create Cooling Equipment Object and characterize its streams

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

            fuel_type : str
                Fuel type

            object_type : str
                Equipment type: "process", "boiler","chp", "burner", "cooling_equipment", "stream"

            global_conversion_efficiency : float
                Chiller COP []

            supply_capacity : float
                Equipment supply capacity [kW]

            cooling_equipment_sub_type : str
                Type of cooling equipment; 'co2_chiller', 'cooling_tower', 'compression_chiller'

            processes : list
                List of processes objects associated to the equipment

            saturday_on : int
                If it is available on Saturday []; 1 (yes)  or 0 (no)

            sunday_on : int
                If it is available on Sunday []; 1 (yes)  or 0 (no)

            shutdown_periods : list
                List with lists of periods of days it is not available [day]; e.g. [[130,140],[289,299]]

            daily_periods : list
                List with lists of hourly periods it is available [h]; e.g. [[8,12],[15,19]]

    kb : dict
        Knowledge Base data

    """

    def __init__(self, in_var, kb: KB):

        ############################################################################################
        # KB
        equipment_details = EquipmentDetails(kb)
        medium = Medium(kb)

        # Defined Vars
        self.object_type = 'equipment'
        self.streams = []
        self.fuel_type = 'electricity'  # Electricity

        self.global_conversion_efficiency = in_var['global_conversion_efficiency']
        excess_heat_fluid = 'water'  # excess heat fluid type

        ############################################################################################
        # INPUT
        self.id = in_var['id']  # equipment ID
        self.equipment_sub_type = in_var['cooling_equipment_sub_type']  # Equipment type (co2_chiller/compression_chiller/cooling_tower)
        self.supply_capacity = in_var['supply_capacity']
        processes = in_var['processes']
        saturday_on = in_var['saturday_on']
        sunday_on = in_var['sunday_on']
        shutdown_periods = in_var['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var['daily_periods']  # e.g: [[8,12],[15,19]]

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

        # COP
        if self.global_conversion_efficiency is None:
            if self.equipment_sub_type == 'compression_chiller':
                cop = compute_cop_eer(self.equipment_sub_type)
            else:
                cop, om_fix, turnkey = equipment_details.get_values(self.equipment_sub_type, self.supply_capacity)

            self.global_conversion_efficiency = cop

        # excess heat characteristics
        if self.equipment_sub_type == 'co2_chiller':
            excess_heat_supply_temperature = 90  # discharge temperature [ºC]
            excess_heat_target_temperature = 60  # gas cooler entry temperature [ºC]
            excess_heat_fluid_cp = medium.cp(excess_heat_fluid, (
                    excess_heat_supply_temperature + excess_heat_target_temperature) / 2)

        elif self.equipment_sub_type == 'compression_chiller':
            excess_heat_supply_temperature = 45
            excess_heat_target_temperature = 35
            excess_heat_fluid_cp = medium.cp(excess_heat_fluid, (
                    excess_heat_supply_temperature + excess_heat_target_temperature) / 2)

        elif self.equipment_sub_type == 'cooling_tower':
            excess_heat_supply_temperature = 38
            excess_heat_target_temperature = 33
            excess_heat_fluid_cp = medium.cp(excess_heat_fluid, (
                    excess_heat_supply_temperature + excess_heat_target_temperature) / 2)

        # excess heat stream
        if self.equipment_sub_type == 'co2_chiller':
            excess_heat_supply_capacity = self.supply_capacity * 1.520

            excess_heat_flowrate = compute_flow_rate(kb,excess_heat_fluid,
                                                     excess_heat_supply_capacity,
                                                     excess_heat_supply_temperature,
                                                     excess_heat_target_temperature)
        else:
            excess_heat_supply_capacity = self.supply_capacity * (1 - 1 / self.global_conversion_efficiency)
            excess_heat_flowrate = excess_heat_supply_capacity / (abs(excess_heat_supply_temperature - excess_heat_target_temperature) * excess_heat_fluid_cp) *3600

        ############################################################################################
        # GET STREAMS
        # excess heat
        self.streams.append(stream_industry(self.equipment_sub_type + ' excess heat',
                                            self.id,
                                            'excess_heat',
                                            excess_heat_fluid,
                                            excess_heat_supply_temperature,
                                            excess_heat_target_temperature,
                                            excess_heat_flowrate,
                                            excess_heat_supply_capacity,
                                            schedule=schedule,
                                            stream_id=1,
                                            fuel="none",
                                            eff_equipment=None
                                            ))
