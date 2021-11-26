
from ......KB_General.equipment_details import equipment_details
from ......KB_General.fluid_material import fluid_material_cp

def hx_storage(df_profile, vector_df_hx,above_pinch):

    # Init arrays
    storage_delta_T = 5
    new_volume_max_storage = 0

    if len(vector_df_hx) > 0:
        for df_hx in vector_df_hx:
            vector_storage_volume = []
            vector_storage_satisfies = []
            vector_energy_year = []
            vector_storage_turn_key = []
            vector_max_energy_year = []

            if df_hx.empty == False:

                for index, row in df_hx.iterrows():

                    # choose type of thermal storage
                    if row['Hot_Stream_T_Hot'] <= 90 + storage_delta_T:
                        fluid = 'water'
                        cp_fluid = fluid_material_cp(fluid,90) # kJ/(kg.K)
                        rho_fluid = 1000  # kg/m3
                        cost_fluid = 0.0004 # €/L
                    else:
                        fluid = 'thermal_oil'
                        cp_fluid = fluid_material_cp(fluid,150)
                        rho_fluid = 920
                        cost_fluid = 0.5 # €/L

                    # Get Streams
                    power_hx = row['Power']  # hx power
                    if above_pinch == True:
                        index_cold_stream = row['Original_Stream_Out']  # original index stream - to get hourly profile
                        index_hot_stream = row['Original_Stream_In']
                    else:
                        index_cold_stream = row['Original_Stream_In']  # original index stream - to get hourly profile
                        index_hot_stream = row['Original_Stream_Out']


                    profile_cold_stream = df_profile.loc[index_cold_stream]  # hourly profile with 0 and 1
                    profile_hot_stream = df_profile.loc[index_hot_stream]

                    # Compute surplus/deficit hours
                    hours_cold = sum(profile_cold_stream[profile_cold_stream == 1])
                    hours_hot = sum(profile_hot_stream[profile_hot_stream == 1])

                    hours_coincident = profile_hot_stream[
                        profile_hot_stream == profile_cold_stream]  # check when both streams have same schedule
                    hours_coincident = sum(hours_coincident[hours_coincident != 0])  # remove when both not operating

                    # Storage Water
                    # Create 2 days profile - to assure correct storage computation
                    profile_cold_stream = profile_cold_stream.head(47) # get first 48 hours
                    profile_hot_stream = profile_hot_stream.head(47)

                    # Check if storage needed
                    if hours_cold == hours_coincident:
                        volume_storage = 0
                        vector_storage_volume.append(volume_storage)
                        vector_storage_satisfies.append(100)  # % hours storage_satisfies
                        vector_storage_turn_key.append(0)

                    else:
                        # HOT SURPLUS - satisfaction 100%
                        if hours_hot >= hours_cold:
                            # start with theoretical max storage
                            volume_max_storage = hours_cold * power_hx
                            find_min_storage = True # find minimum storage
                            vector_storage_satisfies.append(100) # % hours storage_satisfies

                            while find_min_storage == True:
                                power_storage = volume_max_storage # start with full storage
                                hours_deficit = 0 # hours cold surplus

                                for hour in range(len(profile_cold_stream)):

                                    # deficit
                                    if profile_cold_stream[hour] == 1 and profile_hot_stream[hour] == 0:
                                        power_storage -= power_hx # remove power from storage
                                        hours_deficit += 1

                                    # surplus
                                    if profile_cold_stream[hour] == 0 and profile_hot_stream[hour] == 1:
                                        if power_storage < volume_max_storage:
                                            power_storage += power_hx # add power to storage

                                    # storage cannot reach 0 - break cycle. Minimum storage was already saved in previous iteration
                                    if power_storage < 0:
                                        find_min_storage = False # minimum storage found
                                        break

                                # minimum storage not found, continue to decrease initial max storage
                                if find_min_storage == True:
                                    new_volume_max_storage = volume_max_storage # save previous iteration initial max storage
                                    volume_max_storage -= power_hx # next iteration initial max storage

                        # COLD SURPLUS - satisfaction NOT 100%
                        else:
                            # Find storage as function of maximum surplus hours
                            storage_final = 0
                            power_storage = 0 # storage starting at 0
                            hours_match = 0
                            hours_deficit = 0

                            for hour in range(len(profile_cold_stream)):

                                # deficit
                                if profile_cold_stream[hour] == 1 and profile_hot_stream[hour] == 0:
                                        hours_deficit += 1
                                        if power_storage > 0:
                                                hours_match += 1
                                                power_storage -= power_hx # remove power from storage

                                # surplus
                                if profile_cold_stream[hour] == 0 and profile_hot_stream[hour] == 1:
                                        power_storage += power_hx # add power to storage

                                # find storage that can receive has much surplus power as possible
                                if power_storage > storage_final:
                                        storage_final = power_storage

                            new_volume_max_storage = storage_final
                            storage_satisfies = hours_match / hours_deficit * 100
                            vector_storage_satisfies.append(storage_satisfies)  # hours storage_satisfies [%]

                        # Storage in volume
                        T_hot_hot_stream = row['Hot_Stream_T_Hot']
                        T_cold_hot_stream = row['Hot_Stream_T_Cold']
                        volume_storage = new_volume_max_storage * 3600 /(cp_fluid * rho_fluid * (T_hot_hot_stream - T_cold_hot_stream)) # [m3]
                        vector_storage_volume.append(volume_storage)

                        global_conversion_efficiency,om_fix,storage_turn_key = equipment_details('thermal_storage',volume_storage)
                        storage_fluid_turn_key = volume_storage * cost_fluid
                        storage_total_turn_key = storage_turn_key + storage_fluid_turn_key

                        vector_storage_turn_key.append(storage_total_turn_key)


                    if hours_cold == hours_coincident:
                        vector_energy_year.append(power_hx * hours_cold) # [kWh]

                    elif hours_hot >= hours_cold:
                        vector_energy_year.append(power_hx * hours_cold)

                    else:
                        vector_energy_year.append(power_hx * hours_hot)


                    if hours_cold == hours_coincident:
                        vector_max_energy_year.append(power_hx * hours_cold)

                    elif hours_hot >= hours_cold:
                        vector_max_energy_year.append(power_hx * hours_cold)

                    else:
                        vector_max_energy_year.append(power_hx * hours_hot)

                # OUTPUT
                df_hx['Storage'] = vector_storage_volume  # update storage for each HX [m3]
                df_hx['Storage_Satisfies'] = vector_storage_satisfies  # update recovery satisfaction by using storage for each HX [%]
                df_hx['Storage_Turnkey_Cost'] = vector_storage_turn_key  # update storage for each HX [€]
                df_hx['Total_Turnkey_Cost'] = df_hx['HX_Turnkey_Cost'] + df_hx['Storage_Turnkey_Cost']  # update total turnkey (hx+storage)  [€]
                df_hx['Recovered_Energy'] = vector_energy_year  # yearly total recoverd energy [kWh]

    return vector_df_hx