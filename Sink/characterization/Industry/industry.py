from General.Auxiliary_General.stream import Stream
from General.Auxiliary_General.schedule_hour import schedule_hour


def industry(in_var):

        # INPUT  ------------------------
        sink_id = in_var.sink_id
        stream_type = 'inflow'
        supply_temperature = in_var.supply_temperature
        target_temperature = in_var.target_temperature
        fluid = in_var.fluid
        fluid_cp = in_var.fluid_cp
        flowrate = in_var.flowrate

        # COMPUTE ------------------------
        capacity = flowrate * fluid_cp * abs((supply_temperature - target_temperature))/3600  # [kW]

        # Schedule Process FROM USER OR INVAR ASSUMES MASTER SCHEDULE
        saturday_on = in_var.saturday_on
        sunday_on = in_var.sunday_on
        shutdown_periods = in_var.shutdown_periods
        daily_periods = in_var.daily_periods

        hourly_generation = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)


        # OUTPUT ------------------------
        output = Stream(sink_id,stream_type,fluid,supply_temperature,target_temperature,flowrate,capacity,hourly_generation)

        return output


