from ....Error_Handling.error_isolated_stream import PlatformIsolatedStream
from ....General.Simple_User.isolated_stream import isolated_stream
from .Pinch.convert_pinch import convert_pinch
from ....utilities.kb import KB


def convert_pinch_isolated_streams(in_var, kb: KB):
    '''
    Perform Pinch Analysis to isolated streams.
    Return best solutions data and report

    :param in_var:
        streams : dict
            Streams data

        pinch_delta_T_min : float
            Pinch delta_T

        location : list
            Latitude and Longitude

    :return:
        best_options : dict.
            Dicts with solutions data for:
                - 'co2_optimization'
                - 'energy_recovered_optimization'
                - 'energy_investment_optimization'

        report : str
            HTML Report

    '''

    raw_streams_data = PlatformIsolatedStream(**in_var['platform'])
    streams_data = [vars(stream) for stream in raw_streams_data.streams]

    # get streams data
    isolated_stream_output = isolated_stream(streams_data)
    streams = isolated_stream_output['streams']

    # perform pinch analysis
    input_data = {
        "platform": {
            'all_input_objects': streams,
            'pinch_delta_T_min': in_var['platform']['pinch_delta_T_min'],
            'location': in_var['platform']['location']}
    }


    pinch_output = convert_pinch(input_data, kb)

    return pinch_output
