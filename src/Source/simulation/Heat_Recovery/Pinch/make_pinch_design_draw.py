import matplotlib.pyplot as plt, mpld3
import matplotlib.lines as mlines

def make_pinch_design_draw(info):
    """Make pinch analysis diagram

    Parameters
    ----------
    info : dict
        Data from "convert_pinch" to make draw

            streams_info : list
                List with streams dict, with the following keys

            pinch_temperature : float
                Pinch temperature [ºC]

            pinch_delta_T_min : float
                Minimum temperature difference considered for pinch analysis

            df_hx : df
                Designed heat exchangers data

    Returns
    -------
    fig_html: str
        HTML report

    """

    streams_info = info['streams_info']
    pinch_temperature = info['pinch_temperature']
    pinch_data = info['df_hx'].to_dict(orient='records')
    pinch_delta_temperature = info['pinch_delta_T_min']
    pinch_delta_temperature = pinch_delta_temperature/2
    pinch_temperature -= pinch_delta_temperature


    pinch_hot = pinch_temperature + pinch_delta_temperature
    pinch_cold = pinch_temperature - pinch_delta_temperature

    ###########################
    # Defined vars
    dict_for_hx = {}
    left_side_pinch = []
    right_side_pinch = []
    arrow_width = 0.1
    circle_radius = 1.4  # HX big circle - black
    small_circle_radius = 1.2  # inside HX big circle - white
    height_hx_power = circle_radius + 0.3  # height to write HX Power
    diagonal_space = 5  # space to make splits diagonals
    mini_space = 3.5
    space_between_streams = 10
    space_between_splits = 5
    height_temperature_text = 0.9  # height to write temperatures

    ######################################################################################
    # Obtain x_min, x_max and y_min, by knowing the number of streams and splits
    number_streams = 0
    for stream in streams_info:
        if len(stream['above_pinch']) > 1 or len(stream['below_pinch']) > 1:
            if len(stream['above_pinch']) == len(stream['below_pinch']):
                number_streams += (1 + 0.5 * (len(stream['above_pinch']) - 1))
            elif len(stream['above_pinch']) > len(stream['below_pinch']):
                number_streams += (1 + 0.5 * (len(stream['above_pinch']) - 1))
            else:
                number_streams += (1 + 0.5 * (len(stream['below_pinch']) - 1))
        else:
            number_streams += 1

    x_min = 0
    y_min = 0
    y_max = space_between_streams * (number_streams + 1)
    x_max = y_max * 2
    pinch = x_max / 2

    ######################################################################################
    # get HX info
    above_pinch_hx = []
    below_pinch_hx = []
    info_to_design_hx = {}
    for match_data in pinch_data:
        if match_data['HX_Hot_Stream_T_Cold'] >= pinch_hot:
            above_pinch_hx.append(match_data)
        else:
            below_pinch_hx.append(match_data)

    mini_space_cold_stream_out = (x_max/2)/(len(above_pinch_hx)+2)
    diagonal_space_cold_stream_out = (x_max/2)/(len(above_pinch_hx)+2) +2
    mini_space_hot_stream_out = (x_max/2)/(len(below_pinch_hx)+2)
    diagonal_space_hot_stream_out = (x_max/2)/(len(below_pinch_hx)+2) +2

    ######################################################################################
    # create two list with temperature steps left/right to the pinch - e.g [300, 240, 210...] - so that when hot stream
    # does not reach pinch, or cold pinch does not reach pinch -> the stream is drawn until  mid points between stream start and pinch T.

    y_stream = y_max
    y_stream -= space_between_streams  # y of first stream to be drawn


    for stream in streams_info:
        supply_temperature, target_temperature = stream['temperatures']

        # hot stream
        if supply_temperature > target_temperature:
            if supply_temperature > pinch_hot and target_temperature > pinch_hot:
                left_side_pinch.append(target_temperature)
            elif supply_temperature < pinch_hot and target_temperature < pinch_hot:
                right_side_pinch.append(supply_temperature)
        # cold stream
        else:
            if supply_temperature < pinch_cold and target_temperature < pinch_cold:
                right_side_pinch.append(target_temperature)
            elif supply_temperature > pinch_cold and target_temperature > pinch_cold:
                left_side_pinch.append(supply_temperature)

    # sort temperature steps
    if len(left_side_pinch) > 0:
        left_side_pinch.sort()
    if len(right_side_pinch) > 0:
        right_side_pinch.sort(reverse=True)

    ######################################################################################
    # DRAW MAIN STREAMS AND SPLITS - stream per stream

    for stream in streams_info:

        number_splits_above = 0
        number_splits_below = 0
        supply_temperature, target_temperature = stream['temperatures']

        # hot streams
        if supply_temperature > target_temperature:
            # write stream ID
            # manual bold
            plt.gca().text(x_min - 4, y_stream, str(stream['id']),color="red", size='large', style='normal', weight='bold', ha='right', va='center')
            plt.gca().text(x_min - 4, y_stream, str(stream['id']), color="red", size='large', style='normal', weight='bold', ha='right', va='center')

            if supply_temperature > pinch_hot:
                left_temperature = x_min
            elif supply_temperature == pinch_hot:
                left_temperature = pinch
            else:
                left_temperature = pinch + (right_side_pinch.index(supply_temperature) + 1) * 3

            if target_temperature < pinch_hot:
                right_temperature = x_max
            elif target_temperature == pinch_hot:
                right_temperature = pinch
            else:
                right_temperature = pinch-(left_side_pinch.index(target_temperature) + 1) * 3

            plt.gca().text(left_temperature + 0.5 , y_stream+height_temperature_text, "{:.0f}".format(supply_temperature) + 'º', ha="left", va="bottom")   # draw left temperature
            plt.gca().text(right_temperature - 3, y_stream+height_temperature_text, "{:.0f}".format(target_temperature)+ 'º', ha="left", va="bottom")   # draw right temperature
            rectangle = plt.Rectangle((left_temperature-0.1, y_stream-1), 0.2, 2, color='r')
            plt.gca().add_patch(rectangle)  # draw beginning of stream

            # MAIN STREAM
            plt.arrow(left_temperature,  # x1
                      y_stream,  # y1
                      (right_temperature - left_temperature)-1.5,  # x2 - x1
                      0,
                      width=arrow_width,  # y2 - y1
                      head_width=1,
                      color='r')

            # gather stream ID and corresponding y where it was placed
            dict_for_hx[str(stream['id'])] = y_stream


            # SPLIT ABOVE PINCH
            if len(stream['above_pinch']) > 1:
                i = 0
                for iterator in range(len(stream['above_pinch'])):
                    if stream['above_pinch'][iterator]['id'] != stream['id']:
                        if target_temperature < pinch_hot:
                            split_closest_pinch_temperature = pinch
                        else:
                            split_closest_pinch_temperature = right_temperature

                        plt.plot((left_temperature + diagonal_space, split_closest_pinch_temperature - diagonal_space), (y_stream-space_between_splits*(i+1), y_stream-space_between_splits*(i+1)), 'r')
                        plt.plot((left_temperature+mini_space, left_temperature + diagonal_space), (y_stream, y_stream-space_between_splits*(i+1)), 'r')
                        plt.plot((split_closest_pinch_temperature-diagonal_space, split_closest_pinch_temperature-mini_space), (y_stream-space_between_splits*(i+1), y_stream), 'r')
                        number_splits_above = len(stream['above_pinch']) - 1
                        dict_for_hx[str(stream['above_pinch'][iterator]['id'])] = y_stream-space_between_splits*(i+1)
                        i += 1

            # SPLIT BELOW PINCH
            if len(stream['below_pinch']) > 1:
                i = 0
                for iterator in range(len(stream['below_pinch'])):  # for iterator in range(len(stream['below_pinch']) - 1):
                    if stream['below_pinch'][iterator]['id'] != stream['id']:
                        if supply_temperature > pinch_hot:
                            split_closest_pinch_temperature = left_temperature
                        else:
                            split_closest_pinch_temperature = pinch

                        # split line
                        plt.plot((split_closest_pinch_temperature + diagonal_space, right_temperature - diagonal_space_hot_stream_out),(y_stream - space_between_splits * (i + 1), y_stream - space_between_splits * (i + 1)), 'r')
                        # split diagonal lines
                        plt.plot((split_closest_pinch_temperature + mini_space, split_closest_pinch_temperature + diagonal_space),(y_stream, y_stream - space_between_splits * (i + 1)), 'r')
                        plt.plot((right_temperature - diagonal_space_hot_stream_out, right_temperature - mini_space_hot_stream_out),(y_stream - space_between_splits * (i + 1), y_stream), 'r')
                        number_splits_below = len(stream['below_pinch']) - 1
                        dict_for_hx[str(stream['below_pinch'][iterator]['id'])] = y_stream - space_between_splits * (i + 1)
                        i += 1

        # cold streams
        else:
            # write stream ID
            # manual bold
            plt.gca().text(x_max + 4, y_stream, str(stream['id']),color="blue", size='large', style='normal', bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 10}, weight='bold', ha='left', va='center')
            plt.gca().text(x_max + 4, y_stream, str(stream['id']),color="blue", size='large', style='normal', bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 10}, weight='bold', ha='left', va='center')

            dict_for_hx[str(stream['id'])] = y_stream


            if supply_temperature == pinch_cold:
                right_temperature = pinch
            elif supply_temperature < pinch_cold:
                right_temperature = x_max
            else:
                right_temperature = pinch - (left_side_pinch.index(supply_temperature) + 1) * 3

            if target_temperature > pinch_cold:
                left_temperature = x_min
            elif target_temperature == pinch_cold:
                left_temperature = pinch
            else:
                left_temperature = pinch + (right_side_pinch.index(target_temperature) + 1) * 3

            # write temperatures
            plt.gca().text(left_temperature + 3, y_stream+height_temperature_text, "{:.0f}".format(target_temperature)+ 'º', ha="right", va="bottom")
            plt.gca().text(right_temperature - 0.8, y_stream+height_temperature_text, "{:.0f}".format(supply_temperature)+ 'º', ha="right", va="bottom")

            # draw arrows
            rectangle = plt.Rectangle((right_temperature-0.1, y_stream-1), 0.2, 2, color='b')
            plt.gca().add_patch(rectangle)
            plt.arrow(right_temperature,  # x1
                      y_stream,  # y1
                      (left_temperature-right_temperature)+1,  # x2 - x1
                      0,  # y2 - y1
                      width=arrow_width,
                      head_width=1,
                      color='b')


            # SPLIT ABOVE PINCH
            if len(stream['above_pinch']) > 1:
                i = 0
                for iterator in range(len(stream['above_pinch'])):
                    if stream['above_pinch'][iterator]['id'] != stream['id']:
                        if supply_temperature < pinch_cold:
                            split_closest_pinch_temperature = pinch
                        else:
                            split_closest_pinch_temperature = right_temperature

                        # split line
                        plt.plot((left_temperature + diagonal_space_cold_stream_out, split_closest_pinch_temperature - diagonal_space), (y_stream-space_between_splits*(i+1), y_stream-space_between_splits*(i+1)), 'b')
                        plt.plot((left_temperature+mini_space_cold_stream_out, left_temperature + diagonal_space_cold_stream_out), (y_stream, y_stream-space_between_splits*(i+1)), 'b')
                        plt.plot((split_closest_pinch_temperature-diagonal_space, split_closest_pinch_temperature-mini_space), (y_stream-space_between_splits*(i+1), y_stream), 'b')

                        number_splits_above = len(stream['above_pinch']) - 1
                        dict_for_hx[str(stream['above_pinch'][iterator]['id'])] = y_stream-space_between_splits*(i+1)
                        i += 1


            # SPLIT BELOW PINCH
            if len(stream['below_pinch']) > 1:
                i = 0
                for iterator in range(len(stream['below_pinch'])):
                    if stream['below_pinch'][iterator]['id'] != stream['id']:
                        if target_temperature > pinch_cold:
                            split_closest_pinch_temperature = pinch
                        else:
                            split_closest_pinch_temperature = left_temperature

                        plt.plot((split_closest_pinch_temperature + diagonal_space, right_temperature - diagonal_space), (y_stream - space_between_splits * (i + 1), y_stream - space_between_splits * (i + 1)),'b')
                        plt.plot((split_closest_pinch_temperature + mini_space, split_closest_pinch_temperature + diagonal_space),(y_stream, y_stream - space_between_splits * (i + 1)), 'b')
                        plt.plot((right_temperature - diagonal_space, right_temperature - mini_space),(y_stream - space_between_splits * (i + 1), y_stream), 'b')
                        number_splits_below = len(stream['below_pinch']) - 1
                        dict_for_hx[str(stream['below_pinch'][iterator]['id'])] = y_stream - space_between_splits * (i + 1)
                        i += 1

        y_stream -= space_between_streams + space_between_splits * max([number_splits_above, number_splits_below])


    ##########################################################################
    # DRAW HEAT EXCHANGERS
    info_to_design_hx['above_pinch'] = above_pinch_hx
    info_to_design_hx['below_pinch'] = below_pinch_hx

    left_movement = (x_max / 2) / (len(above_pinch_hx) + 2)
    go_to_the_left = x_max / 2 - left_movement

    # design HX above pinch
    if len(above_pinch_hx) > 0:

        #sort HX by temperatures
        info_to_design_hx['above_pinch'] = sorted(info_to_design_hx['above_pinch'], key=lambda d: d['HX_Cold_Stream_T_Hot'])

        for match in info_to_design_hx['above_pinch']:
            plt.plot((go_to_the_left, go_to_the_left), (dict_for_hx[str(match['HX_Cold_Stream'])], dict_for_hx[str(match['HX_Hot_Stream'])]), 'k-')

            circle_hot = plt.Circle((go_to_the_left, dict_for_hx[str(match['HX_Hot_Stream'])]), circle_radius, color='black', zorder=5)
            circle_cold = plt.Circle((go_to_the_left, dict_for_hx[str(match['HX_Cold_Stream'])]), circle_radius, color='black', zorder=5)
            plt.gca().add_patch(circle_hot)
            plt.gca().add_patch(circle_cold)
            small_circle_hot = plt.Circle((go_to_the_left, dict_for_hx[str(match['HX_Hot_Stream'])]), small_circle_radius, color='white', zorder=10)
            small_circle_cold = plt.Circle((go_to_the_left, dict_for_hx[str(match['HX_Cold_Stream'])]), small_circle_radius, color='white', zorder=10)
            plt.gca().add_patch(small_circle_hot)
            plt.gca().add_patch(small_circle_cold)
            plt.gca().text(go_to_the_left, dict_for_hx[str(match['HX_Cold_Stream'])] - height_hx_power, str(int(match['HX_Power'])) + 'kW', ha="center", va="top")
            plt.gca().text(go_to_the_left, dict_for_hx[str(match['HX_Hot_Stream'])], str(match['id']), size='large' ,weight='bold', zorder=15, ha="center", va="center")

            # write hot streams hx temperatures
            for stream_info in streams_info:
                if stream_info['id'] == match['HX_Original_Hot_Stream']:
                    if round(pinch_hot) != round(match['HX_Hot_Stream_T_Cold']) and round(stream_info['temperatures'][1]) != round(match['HX_Hot_Stream_T_Cold']):
                        plt.gca().text(go_to_the_left + 1,
                                       dict_for_hx[str(match['HX_Hot_Stream'])] + height_temperature_text ,
                                       "{:.0f}".format(round(match['HX_Hot_Stream_T_Cold'])) + 'º', ha="left", va="bottom")
                        break

            # write cold streams hx temperatures
            for stream_info in streams_info:
                if stream_info['id'] == match['HX_Original_Cold_Stream']:
                    if round(stream_info['temperatures'][1]) != round(match['HX_Cold_Stream_T_Hot']):
                        plt.gca().text(go_to_the_left - 1,
                                       dict_for_hx[str(match['HX_Cold_Stream'])] + height_temperature_text ,
                                       "{:.0f}".format(round(match['HX_Cold_Stream_T_Hot'])) + 'º', ha="right", va="bottom")
                        break

            go_to_the_left -= left_movement

    # design HX below pinch
    right_movement = (x_max / 2) / (len(below_pinch_hx) + 2)
    go_to_the_right = x_max / 2 + right_movement

    if len(below_pinch_hx) > 0:

        # sort HX by temperatures
        info_to_design_hx['below_pinch'] = sorted(info_to_design_hx['below_pinch'], key=lambda d: d['HX_Hot_Stream_T_Cold'], reverse=True)



        for match in info_to_design_hx['below_pinch']:

            plt.plot((go_to_the_right, go_to_the_right), (dict_for_hx[str(match['HX_Cold_Stream'])], dict_for_hx[str(match['HX_Hot_Stream'])]), 'k-')
            circle_hot = plt.Circle((go_to_the_right, dict_for_hx[str(match['HX_Hot_Stream'])]), circle_radius, color='black', zorder=5)
            circle_cold = plt.Circle((go_to_the_right, dict_for_hx[str(match['HX_Cold_Stream'])]), circle_radius, color='black', zorder=5)
            plt.gca().add_patch(circle_hot)
            plt.gca().add_patch(circle_cold)
            small_circle_hot = plt.Circle((go_to_the_right, dict_for_hx[str(match['HX_Hot_Stream'])]), small_circle_radius, color='white', zorder=10)
            small_circle_cold = plt.Circle((go_to_the_right, dict_for_hx[str(match['HX_Cold_Stream'])]), small_circle_radius, color='white', zorder=10)
            plt.gca().add_patch(small_circle_hot)
            plt.gca().add_patch(small_circle_cold)
            plt.gca().text(go_to_the_right , dict_for_hx[str(match['HX_Cold_Stream'])] - height_hx_power, str(int(match['HX_Power'])) + 'kW', ha="center", va="top")
            plt.gca().text(go_to_the_right , dict_for_hx[str(match['HX_Hot_Stream'])], str(match['id']), size='large',weight='bold', zorder=15, ha="center", va="center")

            # write hot hx temperatures
            for stream_info in streams_info:
                if stream_info['id'] == match['HX_Original_Hot_Stream']:
                    if round(stream_info['temperatures'][1]) != match['HX_Hot_Stream_T_Cold']:
                        plt.gca().text(go_to_the_right + 1,
                                       dict_for_hx[str(match['HX_Hot_Stream'])] + height_temperature_text ,
                                       "{:.0f}".format(round(match['HX_Hot_Stream_T_Cold'])) +'º', ha="left", va="bottom")

                        break

            # write cold streams hx temperatures
            for stream_info in streams_info:
                if stream_info['id'] == match['HX_Original_Cold_Stream']:
                    if round(pinch_cold) != round(match['HX_Cold_Stream_T_Hot']) and round(stream_info['temperatures'][1]) != round(match['HX_Cold_Stream_T_Hot']):
                        plt.gca().text(go_to_the_right - 1,
                                       dict_for_hx[str(match['HX_Cold_Stream'])] + height_temperature_text ,
                                       "{:.0f}".format(round(match['HX_Cold_Stream_T_Hot'])) + 'º', ha="right", va="bottom")
                        break

            go_to_the_right += right_movement


    ############################################################################################
    # DRAW UTILITIES
    dict_temperatures = {}

    for i in above_pinch_hx:
        dict_temperatures[str(i['HX_Original_Cold_Stream'])] = {}

    for i in above_pinch_hx:
        dict_temperatures[str(i['HX_Original_Cold_Stream'])][str(i['HX_Cold_Stream'])] = {'mcp':i['HX_Cold_Stream_mcp'],'temperature':-1000}

    for i in above_pinch_hx:
        if i['HX_Cold_Stream_T_Hot'] > dict_temperatures[str(i['HX_Original_Cold_Stream'])][str(i['HX_Cold_Stream'])]['temperature']:
            dict_temperatures[str(i['HX_Original_Cold_Stream'])][str(i['HX_Cold_Stream'])]['temperature'] = i['HX_Cold_Stream_T_Hot']

    # hot utilities
    for stream in streams_info:
        write_temperature = 0
        supply_temperature, target_temperature = stream['temperatures']
        mcp_total = stream['mcp']
        stream_y = dict_for_hx[str(stream['id'])]

        if str(stream['id']) in dict_temperatures.keys():

            id_list = [i['id'] for i in stream['above_pinch']]
            if len(list(set(id_list))) > 1:
                no_split_exist = True
            else:
                no_split_exist = False

            if len(stream['above_pinch']) > 1 and no_split_exist == True:
                    # get temperature the stream reaches
                    for key in dict_temperatures[str(stream['id'])].keys():
                        write_temperature += dict_temperatures[str(stream['id'])][key]['temperature'] * dict_temperatures[str(stream['id'])][key]['mcp'] /mcp_total
                    plt.gca().text(diagonal_space_cold_stream_out, stream_y + height_temperature_text, "{:.0f}".format(write_temperature) + 'º',ha='center',va='bottom')
                    # get utility power
                    power_utility = mcp_total * (target_temperature-write_temperature)

                    if power_utility != 0:
                        circle_hot_utility = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y), circle_radius,color='red', zorder=5)
                        circle_hot_utility_small = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y), small_circle_radius, color='white', zorder=10)
                        plt.gca().add_patch(circle_hot_utility)
                        plt.gca().add_patch(circle_hot_utility_small)
                        plt.gca().text(diagonal_space_cold_stream_out/2, stream_y, 'H', weight='bold', ha='center',va='center', zorder=15)
                        plt.gca().text(diagonal_space_cold_stream_out/2, stream_y - circle_radius -1, str(round(power_utility,1)) +'kW',ha='center',va='center')

            elif len(stream['above_pinch']) != 0:
                    power_utility = mcp_total * (target_temperature - dict_temperatures[str(stream['id'])][str(stream['id'])]['temperature'])

                    if power_utility != 0:
                        circle_hot_utility = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y), circle_radius,color='red', zorder=5)
                        circle_hot_utility_small = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y),small_circle_radius, color='white', zorder=10)
                        plt.gca().add_patch(circle_hot_utility)
                        plt.gca().add_patch(circle_hot_utility_small)
                        plt.gca().text(diagonal_space_cold_stream_out / 2, stream_y, 'H', weight='bold', ha='center', va='center', zorder=15)
                        plt.gca().text(diagonal_space_cold_stream_out / 2, stream_y - circle_radius - 1, str(round(power_utility, 1)) + 'kW', ha='center', va='center')

        elif target_temperature > supply_temperature and target_temperature > pinch_cold:

            power_utility = mcp_total * (target_temperature - pinch_cold)

            if power_utility > 0:
                circle_hot_utility = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y), circle_radius, color='red', zorder=5)
                circle_hot_utility_small = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y), small_circle_radius, color='white', zorder=10)
                plt.gca().add_patch(circle_hot_utility)
                plt.gca().add_patch(circle_hot_utility_small)
                plt.gca().text(diagonal_space_cold_stream_out / 2, stream_y, 'H', weight='bold', ha='center', va='center', zorder=15)
                plt.gca().text(diagonal_space_cold_stream_out / 2, stream_y - circle_radius - 1, str(round(power_utility, 1)) + 'kW', ha='center', va='center')

    # cold utilities
    dict_temperatures = {}
    for i in below_pinch_hx:
        dict_temperatures[str(i['HX_Original_Hot_Stream'])] = {}

    for i in below_pinch_hx:
        dict_temperatures[str(i['HX_Original_Hot_Stream'])][str(i['HX_Hot_Stream'])] = {
            'mcp': i['HX_Hot_Stream_mcp'], 'temperature': 100000000000000000000}

    for i in below_pinch_hx:
        if i['HX_Hot_Stream_T_Cold'] < \
                dict_temperatures[str(i['HX_Original_Hot_Stream'])][str(i['HX_Hot_Stream'])]['temperature']:
            dict_temperatures[str(i['HX_Original_Hot_Stream'])][str(i['HX_Hot_Stream'])]['temperature'] = i[
                'HX_Hot_Stream_T_Cold']

    for stream in streams_info:
        write_temperature = 0
        supply_temperature, target_temperature = stream['temperatures']
        mcp_total = stream['mcp']
        stream_y = dict_for_hx[str(stream['id'])]

        if str(stream['id']) in dict_temperatures.keys():

            id_list = [i['id'] for i in stream['below_pinch']]
            if len(list(set(id_list))) > 1:
                no_split_exist = True
            else:
                no_split_exist = False


            if len(stream['below_pinch']) > 1 and no_split_exist == True:
                    for key in dict_temperatures[str(stream['id'])].keys():
                        write_temperature += dict_temperatures[str(stream['id'])][key]['temperature'] * dict_temperatures[str(stream['id'])][key]['mcp'] / mcp_total

                    plt.gca().text(x_max-diagonal_space_hot_stream_out, stream_y + height_temperature_text,
                                   "{:.0f}".format(write_temperature) + 'º', ha='center', va='bottom')

                    power_utility = mcp_total * abs(target_temperature - write_temperature)


                    if power_utility != 0:
                        circle_hot_utility = plt.Circle((x_max-(diagonal_space_hot_stream_out / 2), stream_y), circle_radius,
                                                        color='blue', zorder=5)
                        circle_hot_utility_small = plt.Circle((x_max-(diagonal_space_hot_stream_out / 2), stream_y),
                                                              small_circle_radius, color='white', zorder=10)
                        plt.gca().add_patch(circle_hot_utility)
                        plt.gca().add_patch(circle_hot_utility_small)
                        plt.gca().text(x_max-(diagonal_space_hot_stream_out / 2), stream_y, 'C', weight='bold', ha='center',
                                       va='center', zorder=15)
                        plt.gca().text(x_max-(diagonal_space_hot_stream_out / 2), stream_y - circle_radius - 1,
                                       str(round(power_utility, 1)) + 'kW', ha='center', va='center')

            elif len(stream['below_pinch']) != 0:

                power_utility = mcp_total * abs(target_temperature - dict_temperatures[str(stream['id'])][str(stream['id'])]['temperature'])

                if power_utility != 0:
                    circle_hot_utility = plt.Circle((x_max - (diagonal_space_hot_stream_out / 2), stream_y), circle_radius,
                                                    color='blue', zorder=5)
                    circle_hot_utility_small = plt.Circle((x_max - (diagonal_space_hot_stream_out / 2), stream_y),
                                                          small_circle_radius, color='white', zorder=10)
                    plt.gca().add_patch(circle_hot_utility)
                    plt.gca().add_patch(circle_hot_utility_small)
                    plt.gca().text(x_max - (diagonal_space_hot_stream_out / 2), stream_y, 'C', weight='bold', ha='center',
                                   va='center', zorder=15)
                    plt.gca().text(x_max - (diagonal_space_hot_stream_out / 2), stream_y - circle_radius - 1,
                                   str(round(power_utility, 1)) + 'kW', ha='center', va='center')


        elif supply_temperature > target_temperature and pinch_hot > target_temperature:

            power_utility = mcp_total * pinch_hot

            if power_utility > 0:
                circle_hot_utility = plt.Circle((x_max - (diagonal_space_hot_stream_out / 2), stream_y), circle_radius,
                                                color='blue', zorder=5)
                circle_hot_utility_small = plt.Circle((x_max - (diagonal_space_hot_stream_out / 2), stream_y),
                                                      small_circle_radius, color='white', zorder=10)
                plt.gca().add_patch(circle_hot_utility)
                plt.gca().add_patch(circle_hot_utility_small)
                plt.gca().text(x_max - (diagonal_space_hot_stream_out / 2), stream_y, 'C', weight='bold', ha='center',
                               va='center', zorder=15)
                plt.gca().text(x_max - (diagonal_space_hot_stream_out / 2), stream_y - circle_radius - 1,
                               str(round(power_utility, 1)) + 'kW', ha='center', va='center')

    ########################################################################
    # PINCH LINE AND TEMPERATURES
    plt.plot((pinch, pinch), (y_min+ space_between_splits/2, y_max- space_between_splits/2), 'k--')
    plt.gca().text(pinch, y_max - space_between_splits/2, "{:.1f}".format(pinch_hot) + 'ºC', style='italic', ha='right', va='bottom')
    plt.gca().text(pinch, y_min, "{:.1f}".format(pinch_cold) + 'ºC', style='italic', ha='left', va='top')

    # DRAW MCP
    #plt.gca().text(x_max + 13, y_max+3, 'Original Streams', ha='center', va='center',size='large')#
    #plt.gca().text(x_max + 13, y_max+1, '$mc_p$', weight='bold', ha='center', va='center',size='large')
    #plt.gca().text(x_max + 13, y_max-1, '[kJ/K]', ha='center', va='center')
    #plt.gca().add_patch(plt.Rectangle((x_max+7.5, y_min), 11, (y_max-y_min+5), alpha=0.2, edgecolor='black', facecolor='silver',clip_on=False, linewidth=0.5))#
    #for stream in streams_info:
    #    plt.gca().text(x_max + 13, dict_for_hx[str(stream['id'])], "{:.2f}".format(stream['mcp']), ha='center', va='center',size='large')

    # plot axis limits
    plt.gca().set_xlim(x_min-1, x_max+1)
    plt.gca().set_ylim(y_min, y_max)

    # take off axis numbers and ticks
    plt.gca().set_yticklabels([])
    plt.gca().set_xticklabels([])
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.tight_layout()

    # legend
    blue_line = mlines.Line2D([], [],
                              color='blue',
                              marker='_',
                              markersize=15,
                              label='Cold stream')

    red_line = mlines.Line2D([], [],
                             color='red',
                             marker='_',
                             markersize=15,
                             label='Hot stream')

    circle_hx = mlines.Line2D([0], [0], color='black',
                              markerfacecolor='white',
                              marker='o',
                              markersize=15,
                              label='Heat exchanger')

    circle_hot_utility = mlines.Line2D([0], [0],
                                       color='red',
                                       markerfacecolor='white',
                                       marker='o',
                                       markersize=15,
                                       label='Hot utility')

    circle_cold_utility = mlines.Line2D([0], [0],
                                        markeredgecolor='blue',
                                        markerfacecolor='white',
                                        marker='o',
                                        markersize=15,
                                        label='Cold utility')

    handles = [circle_hx, blue_line, circle_hot_utility, red_line, circle_cold_utility]

    plt.legend(handles=handles, loc="lower right", ncol=3)

    # adjust plot size
    fig = plt.gcf()
    fig.set_size_inches(11, 6)
    ax = plt.gca()
    ax.set_xlim(x_min - 15, x_max + 15)
    ax.set_ylim(y_min - 15, y_max + 5)

    # get HTML
    fig_html = mpld3.fig_to_html(fig)
    plt.close()


    return fig_html






