from ....Error_Handling.error_isolated_stream import PlatformIsolatedStream
from ....General.Simple_User.isolated_stream import isolated_stream
from .Pinch.convert_pinch import convert_pinch
from ....utilities.kb import KB


def convert_pinch_isolated_streams(in_var, kb: KB):
    """ Perform Pinch Analysis to isolated streams.

    Return best solutions data and report

    Parameters
    ----------
    in_var : dict
        Data to perform pinch analysis

            platform : dict
                Platform data

                    streams : dict
                        Streams data

                    pinch_delta_T_min : float
                        Pinch delta_T

                    location : list
                        [latitude, longitude] [º]

                    fuels_data: dict:
                        Fuels price and CO2 emission, with the following keys:

                            - natural_gas: dict
                                Natural gas data

                                    - co2_emissions: float:
                                        Fuel CO2 emission [kg CO2/kWh]

                                    - price: float:
                                        Fuel price [€/kWh]

                            - fuel_oil
                                Same keys as "natural_gas"

                            - electricity
                                Same keys as "natural_gas"

                            - biomass
                                Same keys as "natural_gas"

                    streams_to_analyse : list
                        Stream ID to analyse

    kb : dict
        Knowledge Base

    Returns
    -------
    pinch_output : dict
        Pinch analysis, with the following keys:

            best_options : dict
                Dicts with solutions data for:

                    co2_optimization : list
                        List with best design options of the respective category

                    energy_recovered_optimization : list
                        List with best design options of the respective category

                    energy_investment_optimization : list
                        List with best design options of the respective category

            report : str
                HTML Report

    """

    raw_streams_data = PlatformIsolatedStream(**in_var['platform'])
    streams_data = [vars(stream) for stream in raw_streams_data.streams]


    # get streams data
    isolated_stream_output = isolated_stream(streams_data)
    streams = isolated_stream_output['streams']


    # perform pinch analysis
    input_data = {
        "platform": {
            "fuels_data":  in_var['platform']["fuels_data"],
            "streams_to_analyse": in_var['platform']['streams_to_analyse'],
            "all_input_objects": streams,
            "pinch_delta_T_min": in_var['platform']['pinch_delta_T_min'],
            "location": in_var['platform']['location'],
            "interest_rate": in_var['platform']['interest_rate']}
    }

    pinch_output = convert_pinch(input_data, kb)

    return pinch_output
