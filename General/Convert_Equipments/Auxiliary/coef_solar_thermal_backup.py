


def coef_solar_thermal_backup(stream_hourly_capacity,info_join_technologies,solar_thermal_object):
    solar_thermal_hours_production = solar_thermal_object.data_teo['hourly_supply_capacity'] # solar still production

    power_provided_by_solar_thermal = 0
    for index,hour_power in enumerate(stream_hourly_capacity):

        if solar_thermal_hours_production[index] > 0:
            if hour_power > 0:
                print(hour_power,solar_thermal_hours_production[index])
                if hour_power > solar_thermal_hours_production[index]:
                    power_provided_by_solar_thermal += (hour_power - solar_thermal_hours_production[index])
                else:
                    power_provided_by_solar_thermal += hour_power

    stream_yearly_power = sum(list(filter(lambda num: num != 0, solar_thermal_hours_production)))
    # update om_var and emissions
    coef_solar_thermal = power_provided_by_solar_thermal / stream_yearly_power
    info_join_technologies['hourly_supply_capacity_normalize'] = solar_thermal_object.data_teo['hourly_supply_capacity_normalize']  # add solar thermal profile
    info_join_technologies['emissions'] = info_join_technologies['emissions'] * (1 - coef_solar_thermal)
    info_join_technologies['om_var'] = info_join_technologies['om_var'] * (1 - coef_solar_thermal)
    #info_join_technologies['om_fix'] = info_join_technologies['om_fix'] * (1 - coef_solar_thermal)


    return coef_solar_thermal,info_join_technologies
