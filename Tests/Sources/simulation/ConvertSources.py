

from Source.simulation.Convert.convert_sources import convert_sources


class ConvertSource():
    def __init__(self):

        self.grid_losses =[] # first iteration not needed. Second iteration -> [[200],[150],...]. - CHECK convert_sources info
        self.last_iteration_data =[] # first iteration not needed. Second iteration needed - CHECK convert_sources info
        self.sink_group_grid_supply_temperature = 85
        self.sink_group_grid_return_temperature = 55

        stream_1 = {
            'id':2,
            'object_type':'stream',
            'stream_type':'excess_heat',
            'fluid':'flue_gas',
            'capacity':434,
            'supply_temperature': 220,
            'target_temperature':120,
            'hourly_generation':[1000, 1000, 1000]}

        self.group_of_sources = [ {'id':1,
                            'consumer_type': 'non-household',
                             'location':[10,10],
                             'streams':[stream_1]
                                }]


def testConvertSource():

    data = ConvertSource()
    test = convert_sources(data)

    for sources in test:
        print(sources['streams_converted'][0].keys())

    """
    print(sources['streams_converted'][0].keys())

     Expected:
    dict_keys(['stream_id', 'hourly_stream_capacity', 'conversion_technologies'])
     """





