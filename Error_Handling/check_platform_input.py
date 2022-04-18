
import os
import json

def check_platform_input(input_data,file_name):

    script_dir = os.path.dirname(__file__)
    file_error_handling = json.load(
        open(os.path.join(script_dir, "labels_var", str(file_name) + ".json"))
    )

    # PLATFORM INPUT
    for data_source in input_data:
        check_values(input_data[data_source],file_error_handling)


def check_values(input_data, file_error_handling):

    for var_name, var_val in input_data.items():
        print(var_name)
        var_type = file_error_handling[var_name]['data type']
        options = file_error_handling[var_name]['options']
        min_range = file_error_handling[var_name]['min_range']
        min_range_included = file_error_handling[var_name]['min_range_included']
        max_range = file_error_handling[var_name]['max_range']
        max_range_included = file_error_handling[var_name]['max_range_included']
        range = file_error_handling[var_name]['range']
        condition = file_error_handling[var_name]['condition']


        # FLOAT/INTEGERS
        if var_type == 'float' or var_type == 'integer':
            check_number(var_val, var_name, options, min_range, max_range, min_range_included, max_range_included)

        # STRING
        elif var_type == 'string':
            check_string(var_val,var_name,options)

        # LIST
        elif var_type == 'list':
            check_list(var_val, var_name, condition, min_range, max_range, min_range_included, max_range_included,range)

        # LIST DICTS SPECIFIC
        elif var_type == 'list_dicts':
            check_list_dicts(var_val, var_name, condition)

        # LIST SCHEDULE SPECIFIC
        elif var_type == 'list_schedule':
            check_list_schedule(var_val,var_name,min_range,max_range,min_range_included,max_range_included,range)

        # DICTIONARIES
        elif var_type == 'dict':
            check_dict(var_val, var_name)


def check_dict(var_val, var_name):
    if isinstance(var_val, dict) is True:
        script_dir = os.path.dirname(__file__)
        file = json.load(
            open(os.path.join(script_dir, "labels_var", str(var_name) + ".json"))
        )

        check_values(var_val, file)

    else:
        raise ValueError(str(var_name) + ' not valid. Insert dictionary. ')


def check_number(var_val,var_name,options,min_range,max_range,min_range_included,max_range_included):
    if isinstance(var_val, bool):
        raise TypeError(var_name + '=' + str(var_val) + ' not valid. Insert a number')
    elif not isinstance(var_val, (float, int)) and options != None:
        raise TypeError(var_name + '=' + str(var_val) + ' not valid. Insert a number')
    elif options != None and options != [] and var_val not in options:
        raise ValueError(var_name + '=' + str(var_val) + ' not valid. Must be one of the following: ' + str(options))
    elif options != None and options != [] and var_val in options:
        pass
    elif options == None and var_val == None:
        pass
    elif var_val < float(min_range) or var_val > float(max_range) or (
            min_range_included == 'no' and var_val == float(min_range)) or (
            max_range_included == 'no' and var_val == float(max_range)):
        raise ValueError(var_name + '=' + str(var_val) + ' not within the range. Must be within ' + range)
    else:
        pass


def check_string(var_val,var_name,options):
    if options != [] and var_val not in options:
        raise ValueError(
            var_name + '=' + str(var_val) + ' not valid. Must be one of the following: ' + str(options))
    elif options != [] and var_val in options:
        pass


def check_list(var_val,var_name, condition, min_range, max_range,min_range_included,max_range_included, range):
    if isinstance(var_val, list) is False:
        raise ValueError(var_name + '=' + str(var_val) + ' not valid. Must be a list')
    else:
        if condition:
            for val in var_val:
                if isinstance(val, bool):
                    raise TypeError(str(val) + ' not valid. Insert only numbers')

                elif not isinstance(val, (float, int)):
                    raise TypeError(str(val) + ' not valid. Insert only numbers')

                elif val < float(min_range) or val > float(max_range) or (
                        min_range_included == 'no' and var_val == float(min_range)) or (
                        max_range_included == 'no' and var_val == float(max_range)):

                    raise ValueError(str(val) + ' not valid. Values must be within ' + range)
        else:
            raise ValueError('Condition not met:' + str(condition))


def check_list_dicts(var_val, var_name, condition):
    if isinstance(var_val, list) is False:
        raise ValueError(var_name + '=' + str(var_val) + ' not valid. Must be a list')
    else:
        if condition:
            for val in var_val:
                check_dict(val, var_name)


def check_list_schedule(var_val,var_name,min_range,max_range,min_range_included,max_range_included,range):
    if isinstance(var_val, list) is False:
        raise ValueError(
            var_name + '=' + str(var_val) + ' not valid. Must be an empty list or list with lists')
    else:
        if var_val == []:
            pass
        else:
            for array in var_val:
                if isinstance(array, list):
                    if len(array) == 2:
                        val_a, val_b = array

                        if isinstance(val_a, bool) or isinstance(val_b, bool):
                            raise TypeError(str(array) + ' not valid. Insert only numbers')

                        elif not isinstance(val_a, (float, int)) or not isinstance(val_b, (float, int)):
                            raise TypeError(str(array) + ' not valid. Insert only numbers')

                        elif val_a < float(min_range) or val_a > float(max_range) or (
                                min_range_included == 'no' and var_val == float(min_range)) or (
                                max_range_included == 'no' and var_val == float(max_range)):

                            raise ValueError(str(array) + ' not valid. Values must be within ' + range)

                        elif val_b < float(min_range) or val_b > float(max_range) or (
                                min_range_included == 'no' and var_val == float(min_range)) or (
                                max_range_included == 'no' and var_val == float(max_range)):

                            raise ValueError(
                                str(array) + ' not valid. Values must be within ' + range)
                    else:
                        raise ValueError(str(array) + ' not valid. Only two values per list. ')
                else:
                    raise ValueError(str(array) + ' not valid. Insert list, not single values. ')