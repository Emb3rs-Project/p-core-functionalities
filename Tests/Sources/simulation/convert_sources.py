

from Source.simulation.Convert.convert_sources import convert_sources


class ConvertSource():
    def __init__(self):

        stream_1 = {
            'id':2,
            'object_type':'stream',
            'stream_type':'inflow',
            'fluid':'water',
            'capacity':263,
            'supply_temperature':10,
            'target_temperature':80,
            'hourly_generation':[1000, 1000, 1000]}

        self.group_of_sinks = [{
                                'id':1,
                                'consumer_type':'non-household',
                                'location':[10, 10],
                                'streams':[stream_1]
                            },
                            {
                                'id':56,
                                'consumer_type':'household',
                                'location':[11, 11],
                                'streams':[stream_1]
                                }]


def testConvertSink():

    data = ConvertSource()
    test = convert_sources(data)

    """



