

from module.Sink.characterization.Building.sink_adjust_capacity import sink_adjust_capacity

input_data = {}
input_data['platform'] = {}
input_data['platform']['user_monthly_capacity'] = [120,120,120,120,120,120,120,120,120,120,120,120]

input_data['cf_module'] = {}

stream = {'monthly_generation': [140,140,140,140,140,140,140,140,140,140,140,140]

}

input_data['cf_module']['stream_building'] = stream

a = sink_adjust_capacity(input_data)