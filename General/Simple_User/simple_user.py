from ...General.Auxiliary_General.stream_industry import stream_industry
from ...General.Auxiliary_General.schedule_hour import schedule_hour
from ...Error_Handling.error_simple_user import PlatformSimpleUser
from .adjust_capacity import adjust_capacity


def simple_user(in_var):

    """Simple User streams characterization.

    Receives user's streams data from the platform and creates a standard stream
    data output to be used in other modules.

    Parameters
    ----------
    in_var : dict
        All necessary data to perform the simple characterization data, with the following key:

        platform: dict
            Data obtained from the platform

                - type_of_object: str
                    'sink' or 'source'

                - streams : list with dict
                    Streams to be analyzed. Each stream with the following keys:

                        - name: int
                            stream ID []

                        - supply_temperature: str
                            stream's supply/initial temperature [ºC]

                        - target_temperature: str
                            stream's target/final temperature [ºC]

                        - fluid: str:
                            stream's fluid []

                        - capacity: float
                            stream's capacity [kW] - provide capacity or fluid_cp and flowrate

                        - fluid_cp: float
                            stream's fluid cp [kJ/kg.K] - provide capacity or fluid_cp and flowrate

                        - flowrate: float
                            stream's mass flowrate [kg/h] - provide capacity or fluid_cp and flowrate

                        - daily_periods: float
                            period of daily periods [h]

                        - shutdown_periods: list
                            period of days stream is not available [day]

                        - saturday_on: int
                            if available on saturdays - available (1); not available (0)

                        - sunday_on: int
                            if available on sundays - available (1); not available (0)

                        - ref_system_fuel_type: str
                            Fuel type associated

                        - real_hourly_capacity: list, optional
                            Real hourly data - for each hour of the year

                        - real_daily_capacity: list, optional
                            Real daily data - for each day of the year

                        - real_monthly_capacity: dict, optional
                            Real monthly data - for each month of the year

                        - real_yearly_capacity: float, optional
                            Real yearly data - single value

    Returns
    -------
    output : dict
        Streams data

        - streams : list
            List with dicts of all streams with the following keys:

                - id : int
                    stream ID []

                - name : str
                    Stream name []

                - object_type : str
                    DEFAULT = "stream" []

                - object_linked_id
                    None: DEFAULT=NONE, since no equipment/process is associated

                - stream_type : str
                    Stream designation []; inflow, outflow, excess_heat

                - supply_temperature : float
                    Stream's supply/initial temperature [ºC]

                - target_temperature : float
                    Stream's target/final temperature [ºC]

                - fluid : str
                    Stream fluid name

                - flowrate : float
                    Stream mass flowrate[kg/h]

                - schedule : list
                    Hourly values between 0 and 1, according to the capacity ration on that hour

                - hourly_generation: list
                    Stream's hourly capacity [kWh]

                - capacity : float
                    Stream's capacity [kW]

                - monthly_generation : list
                    Stream's monthly capacity [kWh]

                - fuel : str
                    Associated equipment fuel name []

                - eff_equipment : float
                    Associated equipment efficiency []

    """

    ##########################################################################################
    # INPUT
    platform_data = PlatformSimpleUser(**in_var['platform'])
    streams = platform_data.streams
    streams = [vars(stream) for stream in streams]
    type_of_object = platform_data.type_of_object

    ##########################################################################################
    # COMPUTE
    streams_output = []

    if type_of_object == 'sink':
        stream_type = "inflow"
    else:
        stream_type = "excess_heat"

    for index_stream, stream in enumerate(streams):
        index_stream += 1  # to start at 1

        # check if capacity or flowrate given
        if stream['capacity'] == None:
            try:
                capacity = (stream["flowrate"] * stream["fluid_cp"] * abs((stream["supply_temperature"] - stream["target_temperature"]))/ 3600)
                flowrate = stream['flowrate']
            except:
                pass
        else:
            capacity = stream["capacity"]
            if stream['fluid'] == "steam":
                flowrate = None
            else:
                try:
                    flowrate = stream['flowrate']
                except:
                    flowrate = capacity * 3600 /(abs(stream["supply_temperature"] - stream["target_temperature"]))

        # check if real hourly capacity is given
        if stream['real_hourly_capacity'] is None:
            schedule = schedule_hour(
                stream["saturday_on"],
                stream["sunday_on"],
                stream["shutdown_periods"],
                stream["daily_periods"],
            )
            hourly_generation = None
        else:
            hourly_generation = stream['real_hourly_capacity']
            schedule = None
            capacity = max(hourly_generation)
            flowrate = capacity * 3600 / (abs(stream["supply_temperature"] - stream["target_temperature"]))

        # get fuel properties
        if type_of_object == 'sink':
            eff_equipment = stream["ref_system_eff_equipment"]
        else:
            eff_equipment = None

        # generate stream data
        info_stream = stream_industry(
            stream["name"],
            None,
            stream_type,
            stream["fluid"],
            stream["supply_temperature"],
            stream["target_temperature"],
            flowrate,
            capacity,
            schedule=schedule,
            hourly_generation=hourly_generation,
            stream_id=index_stream,
            fuel=stream["ref_system_fuel_type"],
            eff_equipment=eff_equipment
        )

        # adjust capacity of the stream if needed
        if stream["real_daily_capacity"] != None:
            info_stream = adjust_capacity(info_stream, user_daily_capacity=stream["real_daily_capacity"])
        elif stream["real_monthly_capacity"] != None:
            info_stream = adjust_capacity(info_stream, user_monthly_capacity=vars(stream["real_monthly_capacity"]))
        elif stream["real_yearly_capacity"] != None:
            info_stream = adjust_capacity(info_stream, user_yearly_capacity=stream["real_yearly_capacity"])


        streams_output.append(info_stream)

    output = {'streams': streams_output}

    return output
