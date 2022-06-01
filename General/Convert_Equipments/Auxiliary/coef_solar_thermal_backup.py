"""
##############################
INFO: Adjust 'om_var' and 'emissions' of backup technology when joined with solar thermal, according to solar thermal
supply capacity


##############################
INPUT:
        # stream_hourly_capacity - list [kWh]
        # solar_thermal_object - solar thermal technology
        # heating_technology - backup technology


##############################
OUTPUT: dictionary with:
        # coef_solar_thermal - percentage of streams yearly capacity fulfilled by solar thermal
        # heating_technology


"""



def coef_solar_thermal_backup(stream_hourly_capacity, solar_thermal_object, heating_technology):
    solar_thermal_hours_production = solar_thermal_object.data_teo['hourly_supply_capacity']  # solar still production
    power_provided_by_solar_thermal = 0

    for index, hour_power in enumerate(stream_hourly_capacity):
        try:
            if solar_thermal_hours_production[index] > 0:
                if hour_power > 0:
                    if hour_power > solar_thermal_hours_production[index]:
                        power_provided_by_solar_thermal += (hour_power - solar_thermal_hours_production[index])
                    else:
                        power_provided_by_solar_thermal += hour_power
        except:
            power_provided_by_solar_thermal += 0

    stream_yearly_power = sum(list(filter(lambda num: num != 0, solar_thermal_hours_production)))

    # update om_var and emissions
    coef_solar_thermal = power_provided_by_solar_thermal / stream_yearly_power
    heating_technology.data_teo['om_var'] = heating_technology.data_teo['om_var'] * (1 - coef_solar_thermal)
    heating_technology.data_teo['emissions'] = heating_technology.data_teo['emissions'] * (1 - coef_solar_thermal)

    return coef_solar_thermal, heating_technology
