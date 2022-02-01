
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def make_pinch_design_draw(streams,streams_info,pinch_temperature,pinch_data,pinch_delta_temperature):

    for stream_info in streams_info:
        if len(stream_info['above_pinch']) > 1:
            i = 0
            for index_above, above_info in enumerate(stream_info['above_pinch']):
                if above_info['id'] == stream_info['id']:
                    i += 1
                    if i == 2:
                        stream_info['above_pinch'].pop(index_above)

        if len(stream_info['below_pinch']) > 1:
            i = 0
            for index_below, below_info in enumerate(stream_info['below_pinch']):
                if below_info['id'] == stream_info['id']:
                    i += 1
                    if i == 2:
                        stream_info['below_pinch'].pop(index_below)


    dict_for_hx = {}
    # Defined vars
    arrow_width = 0.1
    circle_radius = 1.4
    small_circle_radius = 1.2
    height_hx_power = circle_radius + 0.3
    diagonal_space = 5
    mini_space = 3.5
    mini_space_out_stream = 10
    start_putting_streams = 100000
    y_max = start_putting_streams
    space_between_streams = 10
    space_between_splits = 5
    height_temperature_text = 0.9
    how_many_above = 0  # how many total streams are above pinch
    how_many_below = 0  # how many total streams are below pinch

    ######################################################################################
    # Obtain x_min, x_max adn y_min
    add_to_y_max = 0
    number_streams = 0
    for stream in streams_info:
        how_many_above += len(stream['above_pinch'])
        how_many_below += len(stream['below_pinch'])

        if len(stream['above_pinch']) > 1 or len(stream['below_pinch']) > 1:
            if len(stream['above_pinch']) == len(stream['below_pinch']):
                number_streams += (1 + 0.5* (len(stream['above_pinch']) - 1))
            elif len(stream['above_pinch']) > len(stream['below_pinch']):
                number_streams += (1 + 0.5* (len(stream['above_pinch']) - 1))
            else:
                number_streams += (1 + 0.5* (len(stream['below_pinch']) - 1))
        else:
            number_streams += 1

    x_min = 0
    y_max = space_between_streams * (number_streams + 1)
    x_max = y_max*1.5
    y_min = 0
    pinch = x_max/2

    #####################
    # HX INFO

    above_pinch_hx = []
    below_pinch_hx = []
    info_to_design_hx = {}
    for match_data in pinch_data:
        if match_data['HX_Hot_Stream_T_Cold'] >= pinch_temperature:
            above_pinch_hx.append(match_data)
        else:
            below_pinch_hx.append(match_data)

    mini_space_cold_stream_out = (x_max/2)/(len(above_pinch_hx)+2)
    diagonal_space_cold_stream_out = (x_max/2)/(len(above_pinch_hx)+2) +2
    mini_space_hot_stream_out = (x_max/2)/(len(below_pinch_hx)+2)
    diagonal_space_hot_stream_out = (x_max/2)/(len(below_pinch_hx)+2) +2

    ######################################################################################
    # DRAW STREAMS
    y_stream = y_max
    y_stream -= space_between_streams

    left_side_pinch = []
    right_side_pinch = []

    for stream in streams_info:
        supply_temperature, target_temperature = stream['temperatures']

        # hot stream
        if supply_temperature > target_temperature:
            if supply_temperature > pinch_temperature and target_temperature > pinch_temperature:
                left_side_pinch.append(target_temperature)
            elif supply_temperature < pinch_temperature and target_temperature < pinch_temperature:
                right_side_pinch.append(supply_temperature)

        # cold stream
        else:
            if supply_temperature < pinch_temperature and target_temperature < pinch_temperature:
                right_side_pinch.append(target_temperature)
            elif supply_temperature > pinch_temperature and target_temperature > pinch_temperature:
                left_side_pinch.append(supply_temperature)

    if len(left_side_pinch)>0:
        left_side_pinch.sort()
    if len(right_side_pinch) > 0:
        right_side_pinch.sort(reverse=True)

    for stream in streams_info:
        number_splits_above = 0
        number_splits_below = 0
        supply_temperature, target_temperature = stream['temperatures']

        # DRAW ORIGINAL STREAM
        # hot stream
        if supply_temperature > target_temperature:

            # write stream ID
            plt.gca().text(x_min - 4, y_stream, str(stream['id']),size='large', style='normal',bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10}, weight='bold', ha='right', va='center')

            if supply_temperature > pinch_temperature:
                left_temperature = x_min
            elif supply_temperature == pinch_temperature:
                left_temperature = pinch
            else:
                left_temperature = pinch + (right_side_pinch.index(supply_temperature) + 1) * 3

            if target_temperature < pinch_temperature:
                right_temperature = x_max
            elif target_temperature == pinch_temperature:
                right_temperature = pinch
            else:
                right_temperature = pinch-(left_side_pinch.index(target_temperature) + 1) * 3


            plt.gca().text(left_temperature + 0.5 , y_stream+height_temperature_text, str(supply_temperature) + 'º', ha="left", va="bottom")
            plt.gca().text(right_temperature - 2.5, y_stream+height_temperature_text, str(target_temperature)+ 'º', ha="left", va="bottom")
            rectangle = plt.Rectangle((left_temperature-0.1, y_stream-1), 0.2, 2, color='r')
            plt.gca().add_patch(rectangle)

            # plot main stream
            plt.arrow(left_temperature,  # x1
                      y_stream,  # y1
                      (right_temperature - left_temperature)-1.5,  # x2 - x1
                      0, width=arrow_width,  # y2 - y1
                      head_width=1,
                      color='r')

            dict_for_hx[str(stream['id'])] = y_stream

            # DRAW SPLIT ABOVE PINCH
            if len(stream['above_pinch']) > 1:
                i = 0
                for iterator in range(len(stream['above_pinch'])):
                    if stream['above_pinch'][iterator]['id'] != stream['id']:
                        if target_temperature < pinch_temperature:
                            split_closest_pinch_temperature = pinch
                        else:
                            split_closest_pinch_temperature = right_temperature

                        plt.plot((left_temperature + diagonal_space, split_closest_pinch_temperature - diagonal_space), (y_stream-space_between_splits*(i+1), y_stream-space_between_splits*(i+1)), 'r')
                        plt.plot((left_temperature+mini_space, left_temperature + diagonal_space), (y_stream, y_stream-space_between_splits*(i+1)), 'r')
                        plt.plot((split_closest_pinch_temperature-diagonal_space, split_closest_pinch_temperature-mini_space), (y_stream-space_between_splits*(i+1), y_stream), 'r')
                        number_splits_above = len(stream['above_pinch']) - 1
                        dict_for_hx[str(stream['above_pinch'][iterator]['id'])] = y_stream-space_between_splits*(i+1)
                        i += 1

            # DRAW SPLIT BELOW PINCH
            if len(stream['below_pinch']) > 1:
                i = 0
                for iterator in range(len(stream['below_pinch']) - 1):
                    if stream['below_pinch'][iterator]['id'] != stream['id']:
                        if supply_temperature > pinch_temperature:
                            split_closest_pinch_temperature = left_temperature
                        else:
                            split_closest_pinch_temperature = pinch

                        plt.plot((split_closest_pinch_temperature + diagonal_space, right_temperature - diagonal_space_hot_stream_out),(y_stream - space_between_splits * (i + 1), y_stream - space_between_splits * (i + 1)), 'r')
                        plt.plot((split_closest_pinch_temperature + mini_space, split_closest_pinch_temperature + diagonal_space_hot_stream_out),(y_stream, y_stream - space_between_splits * (i + 1)), 'r')
                        plt.plot((right_temperature - diagonal_space_hot_stream_out, right_temperature - mini_space_hot_stream_out),(y_stream - space_between_splits * (i + 1), y_stream), 'r')

                        number_splits_below = len(stream['below_pinch']) - 1
                        dict_for_hx[str(stream['below_pinch'][iterator]['id'])] = y_stream - space_between_splits * (i + 1)
                        i += 1
        else:
            # write stream ID
            plt.gca().text(x_max + 4, y_stream, str(stream['id']),size='large', style='normal',bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 10}, weight='bold', ha='left', va='center')
            dict_for_hx[str(stream['id'])] = y_stream

            if supply_temperature == pinch_temperature-pinch_delta_temperature:
                right_temperature = pinch
            elif supply_temperature < pinch_temperature-pinch_delta_temperature:
                right_temperature = x_max
            else:
                right_temperature = pinch - (left_side_pinch.index(supply_temperature) + 1) * 3

            if target_temperature > pinch_temperature-pinch_delta_temperature:
                left_temperature = x_min
            elif target_temperature == pinch_temperature-pinch_delta_temperature:
                left_temperature = pinch
            else:
                left_temperature = pinch + (right_side_pinch.index(target_temperature) + 1) * 3


            plt.gca().text(left_temperature + 2.4 , y_stream+height_temperature_text, str(target_temperature)+ 'º', ha="right", va="bottom")
            plt.gca().text(right_temperature - 0.8, y_stream+height_temperature_text, str(supply_temperature)+ 'º', ha="right", va="bottom")
            rectangle = plt.Rectangle((right_temperature-0.1, y_stream-1), 0.2, 2, color='b')
            plt.gca().add_patch(rectangle)
            plt.arrow(right_temperature,  # x1
                      y_stream,  # y1
                      (left_temperature-right_temperature)+1,  # x2 - x1
                      0,  # y2 - y1
                      width=arrow_width,
                      head_width=1,
                      color='b')


            # DRAW SPLIT ABOVE PINCH
            if len(stream['above_pinch']) > 1:
                i = 0
                for iterator in range(len(stream['above_pinch'])):
                    if stream['above_pinch'][iterator]['id'] != stream['id']:
                        if supply_temperature < pinch_temperature:
                            split_closest_pinch_temperature = pinch
                        else:
                            split_closest_pinch_temperature = right_temperature

                        plt.plot((left_temperature + diagonal_space_cold_stream_out, split_closest_pinch_temperature - diagonal_space), (y_stream-space_between_splits*(i+1), y_stream-space_between_splits*(i+1)), 'b')
                        plt.plot((left_temperature+mini_space_cold_stream_out, left_temperature + diagonal_space_cold_stream_out), (y_stream, y_stream-space_between_splits*(i+1)), 'b')
                        plt.plot((split_closest_pinch_temperature-diagonal_space, split_closest_pinch_temperature-mini_space), (y_stream-space_between_splits*(i+1), y_stream), 'b')
                        number_splits_above = len(stream['above_pinch']) - 1
                        dict_for_hx[str(stream['above_pinch'][iterator]['id'])] = y_stream-space_between_splits*(i+1)
                        i += 1


            # DRAW SPLIT BELOW PINCH
            if len(stream['below_pinch']) > 1:
                i = 0
                for iterator in range(len(stream['below_pinch'])):
                    if stream['below_pinch'][iterator]['id'] != stream['id']:
                        if target_temperature > pinch_temperature:
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

    # Design HX
    info_to_design_hx['above_pinch'] = above_pinch_hx
    info_to_design_hx['below_pinch'] = below_pinch_hx

    left_movement = (x_max / 2) / (len(above_pinch_hx) + 2)
    go_to_the_left = x_max / 2 - left_movement

    # design HX above pinch
    if len(above_pinch_hx)>0:
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
            plt.gca().text(go_to_the_left, dict_for_hx[str(match['HX_Cold_Stream'])] - height_hx_power, str(round(match['HX_Power'],1)) + 'kW', ha="center", va="top")
            plt.gca().text(go_to_the_left, dict_for_hx[str(match['HX_Hot_Stream'])], str(match['id']), size='large' ,weight='bold', zorder=15, ha="center", va="center")

            # write hot streams hx temperatures
            for stream_info in streams_info:
                if stream_info['id'] == match['HX_Original_Hot_Stream']:
                    if round(pinch_temperature) != round(match['HX_Hot_Stream_T_Cold']) and round(stream_info['temperatures'][1]) != round(match['HX_Hot_Stream_T_Cold']):
                        plt.gca().text(go_to_the_left + 1,
                                       dict_for_hx[str(match['HX_Hot_Stream'])] + height_temperature_text ,
                                       str(round(match['HX_Hot_Stream_T_Cold'])) + 'º', ha="left", va="bottom")
                        break

            # write cold streams hx temperatures
            for stream_info in streams_info:
                if stream_info['id'] == match['HX_Original_Cold_Stream']:
                    if round(stream_info['temperatures'][1]) != round(match['HX_Cold_Stream_T_Hot']):
                        plt.gca().text(go_to_the_left - 1,
                                       dict_for_hx[str(match['HX_Cold_Stream'])] + height_temperature_text ,
                                       str(round(match['HX_Cold_Stream_T_Hot'])) + 'º', ha="right", va="bottom")
                        break

            go_to_the_left -= left_movement


    # design HX below pinch if len(below_pinch_hx)>0:
    right_movement = (x_max / 2) / (len(below_pinch_hx) + 2)
    go_to_the_right = x_max / 2 + right_movement
    if len(below_pinch_hx) > 0:
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
            plt.gca().text(go_to_the_right , dict_for_hx[str(match['HX_Cold_Stream'])] - height_hx_power, str(round(match['HX_Power'],1)) + 'kW', ha="center", va="top")
            plt.gca().text(go_to_the_right , dict_for_hx[str(match['HX_Hot_Stream'])], str(match['id']), size='large',weight='bold', zorder=15, ha="center", va="center")

            # write hot hx temperatures
            for stream_info in streams_info:
                if stream_info['id'] == match['HX_Original_Hot_Stream']:
                    if round(stream_info['temperatures'][1]) != match['HX_Hot_Stream_T_Cold']:
                        plt.gca().text(go_to_the_right + 1,
                                       dict_for_hx[str(match['HX_Hot_Stream'])] + height_temperature_text ,
                                       str(round(match['HX_Hot_Stream_T_Cold'])) +'º', ha="left", va="bottom")

                        break

            # write cold streams hx temperatures
            for stream_info in streams_info:
                if stream_info['id'] == match['HX_Original_Cold_Stream']:
                    print(match['HX_Power'],round(match['HX_Cold_Stream_T_Hot']),round(stream_info['temperatures'][1]))
                    if round(pinch_temperature-pinch_delta_temperature) != round(match['HX_Cold_Stream_T_Hot']) and round(stream_info['temperatures'][1]) != round(match['HX_Cold_Stream_T_Hot']):

                        plt.gca().text(go_to_the_right - 1,
                                       dict_for_hx[str(match['HX_Cold_Stream'])] + height_temperature_text ,
                                       str(round(match['HX_Cold_Stream_T_Hot'])) + 'º', ha="right", va="bottom")
                        break

            go_to_the_right += right_movement


    #######################
    # Hot  Utilities
    dict_temperatures = {}

    for i in above_pinch_hx:
        dict_temperatures[str(i['HX_Original_Cold_Stream'])] = {}

    for i in above_pinch_hx:
        dict_temperatures[str(i['HX_Original_Cold_Stream'])][str(i['HX_Cold_Stream'])] = {'mcp':i['HX_Cold_Stream_mcp'],'temperature':-1000}

    for i in above_pinch_hx:
        if i['HX_Cold_Stream_T_Hot'] > dict_temperatures[str(i['HX_Original_Cold_Stream'])][str(i['HX_Cold_Stream'])]['temperature']:
            dict_temperatures[str(i['HX_Original_Cold_Stream'])][str(i['HX_Cold_Stream'])]['temperature'] = i['HX_Cold_Stream_T_Hot']

    for stream in streams_info:
        write_temperature = 0
        supply_temperature, target_temperature = stream['temperatures']
        mcp_total = stream['mcp']
        stream_y = dict_for_hx[str(stream['id'])]

        if str(stream['id']) in dict_temperatures.keys():

            if len(stream['above_pinch']) > 1:

                    for key in dict_temperatures[str(stream['id'])].keys():
                        write_temperature += dict_temperatures[str(stream['id'])][key]['temperature'] * dict_temperatures[str(stream['id'])][key]['mcp'] /mcp_total

                    plt.gca().text(diagonal_space_cold_stream_out, stream_y + height_temperature_text, str(round(write_temperature,1)) + 'º',ha='center',va='bottom')

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
                        circle_hot_utility = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y), circle_radius,
                                                        color='red', zorder=5)
                        circle_hot_utility_small = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y),
                                                              small_circle_radius, color='white', zorder=10)
                        plt.gca().add_patch(circle_hot_utility)
                        plt.gca().add_patch(circle_hot_utility_small)
                        plt.gca().text(diagonal_space_cold_stream_out / 2, stream_y, 'H', weight='bold', ha='center',
                                       va='center', zorder=15)
                        plt.gca().text(diagonal_space_cold_stream_out / 2, stream_y - circle_radius - 1,
                                       str(round(power_utility, 1)) + 'kW', ha='center', va='center')


        elif  target_temperature > supply_temperature and target_temperature > pinch_temperature - pinch_delta_temperature:

            power_utility = mcp_total * (target_temperature - (pinch_temperature - pinch_delta_temperature))

            if power_utility > 0:
                circle_hot_utility = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y), circle_radius,
                                                color='red', zorder=5)
                circle_hot_utility_small = plt.Circle((diagonal_space_cold_stream_out / 2, stream_y),
                                                      small_circle_radius, color='white', zorder=10)
                plt.gca().add_patch(circle_hot_utility)
                plt.gca().add_patch(circle_hot_utility_small)
                plt.gca().text(diagonal_space_cold_stream_out / 2, stream_y, 'H', weight='bold', ha='center',
                               va='center', zorder=15)
                plt.gca().text(diagonal_space_cold_stream_out / 2, stream_y - circle_radius - 1,
                               str(round(power_utility, 1)) + 'kW', ha='center', va='center')

    #  Cold Utilities
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
            if len(stream['below_pinch']) > 1:
                    for key in dict_temperatures[str(stream['id'])].keys():
                        write_temperature += dict_temperatures[str(stream['id'])][key]['temperature'] * \
                                             dict_temperatures[str(stream['id'])][key]['mcp'] / mcp_total

                    plt.gca().text(x_max-diagonal_space_hot_stream_out, stream_y + height_temperature_text,
                                   str(round(write_temperature, 1)) + 'º', ha='center', va='bottom')

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


        elif supply_temperature > target_temperature and pinch_temperature > target_temperature:

            power_utility = mcp_total * (pinch_temperature - target_temperature)

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

    # plot pinch line and temperatures
    plt.plot((pinch, pinch), (y_min, y_max), 'k--')
    plt.gca().text(pinch, y_max+5, '- PINCH ('+str(pinch_temperature - pinch_delta_temperature/2) + 'ºC) -',weight='bold', ha='center', va='top',size='large')
    plt.gca().text(pinch, y_max, str(pinch_temperature) + 'ºC', style='italic', ha='right', va='bottom')
    plt.gca().text(pinch, y_min - 1, str(pinch_temperature-pinch_delta_temperature) + 'ºC', style='italic', ha='left', va='top')

    # plot cp
    plt.gca().text(x_max + 13, y_max+3, 'Original Streams', ha='center', va='center',size='large')

    plt.gca().text(x_max + 13, y_max+1, '$mc_p$', weight='bold', ha='center', va='center',size='large')
    plt.gca().text(x_max + 13, y_max-1, '[kJ/kg.K]', ha='center', va='center')
    plt.gca().add_patch(plt.Rectangle((x_max+7.5, y_min), 11, (y_max-y_min+5), alpha=0.2, edgecolor='black', facecolor='silver',clip_on=False, linewidth=0.5))

    for stream in streams_info:
        plt.gca().text(x_max + 13, dict_for_hx[str(stream['id'])], str(stream['mcp']), ha='center', va='center',size='large')


    # plot axis limits
    plt.gca().set_xlim(x_min-1, x_max+1)
    plt.gca().set_ylim(y_min, y_max)


    # take off axis numbers and ticks
    plt.gca().set_yticklabels([])
    plt.gca().set_xticklabels([])
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.tight_layout()

    blue_line = mlines.Line2D([], [], color='blue', marker='_',markersize=15, label='Cold stream')
    red_line = mlines.Line2D([], [], color='red', marker='_',markersize=15, label='Hot stream')
    circle_hx = mlines.Line2D([0], [0], color='black', markerfacecolor='white', marker='o',markersize=15, label='Heat exchanger')
    circle_hot_utility = mlines.Line2D([0], [0], color='red', markerfacecolor='white', marker='o',markersize=15, label='Hot utility')
    circle_cold_utility = mlines.Line2D([0], [0], markeredgecolor='blue', markerfacecolor='white', marker='o',markersize=15, label='Cold utility')
    handles = [circle_hx,blue_line,circle_hot_utility,red_line,circle_cold_utility]
    plt.legend(handles=handles,loc="lower right", ncol=3)

    plt.show()



###################################################################

streams = 0
pinch_data = [{'id':1,'HX_Power': 5.5, 'HX_Original_Cold_Stream': 5, 'HX_Original_Hot_Stream': 2, 'HX_Hot_Stream_T_Hot': 238.2, 'HX_Hot_Stream_T_Cold': 183.0, 'HX_Hot_Stream': 2, 'HX_Cold_Stream': 5, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1604.8, 'HX_OM_Fix_Cost': 160.5, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 163.0, 'HX_Cold_Stream_T_Hot': 194.0, 'HX_Cold_Stream_flowrate': 0.089, 'HX_Hot_Stream_flowrate': 0.04999999999999999, 'Cold_Split': None, 'Hot_Split': None, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1604.8, 'Recovered_Energy': 22.0}, {'id':2,'HX_Power': 3.1, 'HX_Original_Cold_Stream': 5, 'HX_Original_Hot_Stream': 3, 'HX_Hot_Stream_T_Hot': 230.7, 'HX_Hot_Stream_T_Cold': 183.0, 'HX_Hot_Stream': 3, 'HX_Cold_Stream': 51050, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1541.7, 'HX_OM_Fix_Cost': 154.2, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 163.0, 'HX_Cold_Stream_T_Hot': 194.0, 'HX_Cold_Stream_flowrate': 0.05, 'HX_Hot_Stream_flowrate': 0.03250000000000001, 'Cold_Split': None, 'Hot_Split': None, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1541.7, 'Recovered_Energy': 12.4}, {'id':3,'HX_Power': 5.5, 'HX_Original_Cold_Stream': 5, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 214.0, 'HX_Hot_Stream_T_Cold': 183.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 521220500, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1672.2, 'HX_OM_Fix_Cost': 167.2, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 163.0, 'HX_Cold_Stream_T_Hot': 194.0, 'HX_Cold_Stream_flowrate': 0.089115, 'HX_Hot_Stream_flowrate': 0.08899999999999997, 'Cold_Split': None, 'Hot_Split': None, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1672.2, 'Recovered_Energy': 22.0}, {'id':4,'HX_Power': 4.5, 'HX_Original_Cold_Stream': 5, 'HX_Original_Hot_Stream': 4, 'HX_Hot_Stream_T_Hot': 225.4, 'HX_Hot_Stream_T_Cold': 183.0, 'HX_Hot_Stream': 4, 'HX_Cold_Stream': 5321661305000, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1601.0, 'HX_OM_Fix_Cost': 160.1, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 163.0, 'HX_Cold_Stream_T_Hot': 194.0, 'HX_Cold_Stream_flowrate': 0.071885, 'HX_Hot_Stream_flowrate': 0.05249999999999999, 'Cold_Split': None, 'Hot_Split': None, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1601.0, 'Recovered_Energy': 18.0}, {'id':5,'HX_Power': 24.0, 'HX_Original_Cold_Stream': 6, 'HX_Original_Hot_Stream': 1, 'HX_Hot_Stream_T_Hot': 349.0, 'HX_Hot_Stream_T_Cold': 214.0, 'HX_Hot_Stream': 1, 'HX_Cold_Stream': 51087948528000, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1809.7, 'HX_OM_Fix_Cost': 181.0, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 189.0, 'HX_Cold_Stream_T_Hot': 279.1, 'HX_Cold_Stream_flowrate': 0.13332000000000002, 'HX_Hot_Stream_flowrate': 0.089, 'Cold_Split': 1.0, 'Hot_Split': 0.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1809.7, 'Recovered_Energy': 72.0}, {'id':6,'HX_Power': 10.3, 'HX_Original_Cold_Stream': 6, 'HX_Original_Hot_Stream': 2, 'HX_Hot_Stream_T_Hot': 341.0, 'HX_Hot_Stream_T_Cold': 238.2, 'HX_Hot_Stream': 2, 'HX_Cold_Stream': 6, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1578.7, 'HX_OM_Fix_Cost': 157.9, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 189.0, 'HX_Cold_Stream_T_Hot': 248.9, 'HX_Cold_Stream_flowrate': 0.08579499999999998, 'HX_Hot_Stream_flowrate': 0.05, 'Cold_Split': 0.0, 'Hot_Split': 0.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1578.7, 'Recovered_Energy': 30.900000000000002}, {'id':7,'HX_Power': 2.4, 'HX_Original_Cold_Stream': 6, 'HX_Original_Hot_Stream': 3, 'HX_Hot_Stream_T_Hot': 268.0, 'HX_Hot_Stream_T_Cold': 230.7, 'HX_Hot_Stream': 3, 'HX_Cold_Stream': 122520, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1464.8, 'HX_OM_Fix_Cost': 146.5, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 189.0, 'HX_Cold_Stream_T_Hot': 220.1, 'HX_Cold_Stream_flowrate': 0.038945, 'HX_Hot_Stream_flowrate': 0.0325, 'Cold_Split': 1.0, 'Hot_Split': 0.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1464.8, 'Recovered_Energy': 7.199999999999999}, {'id':8,'HX_Power': 2.7, 'HX_Original_Cold_Stream': 6, 'HX_Original_Hot_Stream': 4, 'HX_Hot_Stream_T_Hot': 250.9, 'HX_Hot_Stream_T_Cold': 225.4, 'HX_Hot_Stream': 4, 'HX_Cold_Stream': 2501858400, 'HX_Type': 'hx_plate', 'HX_Turnkey_Cost': 1524.7, 'HX_OM_Fix_Cost': 152.5, 'Storage': 0, 'HX_Cold_Stream_T_Cold': 189.0, 'HX_Cold_Stream_T_Hot': 230.9, 'HX_Cold_Stream_flowrate': 0.03194, 'HX_Hot_Stream_flowrate': 0.052499999999999984, 'Cold_Split': 1.0, 'Hot_Split': 0.0, 'Storage_Satisfies': 0, 'Storage_Turnkey_Cost': 0, 'Total_Turnkey_Cost': 1524.7, 'Recovered_Energy': 8.100000000000001}]

pinch_temperature = 183
pinch_delta_temperature = 20
streams_info = [{
                    'id': 2, 'temperatures': [341, 183], 'above_pinch': [{'id': 2, 'flowrate': 0.04999999999999999}],
                    'below_pinch': []}, {
                    'id': 3, 'temperatures': [268, 183], 'above_pinch': [{'id': 3, 'flowrate': 0.03250000000000001}],
                    'below_pinch': []}, {
                    'id': 1, 'temperatures': [349, 183], 'above_pinch': [{'id': 1, 'flowrate': 0.08899999999999997}],
                    'below_pinch': []}, {
                    'id': 4, 'temperatures': [251, 183], 'above_pinch': [{'id': 4, 'flowrate': 0.05249999999999999}],
                    'below_pinch': []}, {
                    'id': 5, 'temperatures': [163, 194],
                    'above_pinch': [{'id': 5, 'flowrate': 0.089}, {'id': 51050, 'flowrate': 0.05},
                                    {'id': 521220500, 'flowrate': 0.089115},
                                    {'id': 5321661305000, 'flowrate': 0.071885}], 'below_pinch': []}, {
                    'id': 6, 'temperatures': [189, 368],
                    'above_pinch': [{'id': 51087948528000, 'flowrate': 0.13332000000000002},
                                    {'id': 6, 'flowrate': 0.08579499999999998}, {'id': 122520, 'flowrate': 0.038945},
                                    {'id': 2501858400, 'flowrate': 0.03194}], 'below_pinch': []}]



#make_pinch_design_draw(streams,streams_info,pinch_temperature,pinch_data,pinch_delta_temperature)




