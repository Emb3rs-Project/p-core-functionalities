
class Stream():

    def __init__(self,object_id,stream_type,fluid,supply_temperature,target_temperature,mass_flowrate,capacity,schedule):
        self.id = 0
        self.object_type = 'stream'
        self.object_id = object_id  # Object ID associated; e.g. process or equipment ID
        self.stream_type = stream_type  # e.g. inflow, supply_heat, excess_heat
        self.supply_temperature = supply_temperature # T_in  # [ºC]
        self.target_temperature = target_temperature # T_out  # [ºC]
        self.fluid = fluid
        self.flowrate = mass_flowrate  # [kg/h]
        self.schedule = schedule  # vector with 1 and 0
        self.hourly_generation = [i *capacity for i in schedule]  # [kWh]
        self.capacity = capacity  # [kW]

