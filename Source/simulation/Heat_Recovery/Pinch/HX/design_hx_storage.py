"""
alisboa/jmcunha

##############################
INFO: Compute storage needed for each HX according to hot and cold stream schedules.
      Three situations may occur:
        1) coincident cold and hot streams hours
        2) surplus hours of hot streams
        3) surplus cold stream hours

      For the first case no storage is designed.
      For the second case, since there is a surplus of hot stream hours, it is designed the minimum storage required
      to satisfy 100% the cold stream.
      For the third case, since there is a surplus of cold stream hours, it is designed a storage that can recover
      maximum energy from the hot stream working alone hours


##############################
INPUT:
        # df_profile - DF with all streams schedules (hourly schedule with 1 and 0)
        # info_df_hx - list with all designed options for above or below the pinch
        # above_pinch - if analysis is above or below pinch  [True/False ]


##############################
RETURN:
        # info_df_hx - each df_hx is updated

        Where the updated keys are:
            # Storage [m3]
            # Storage_Satisfies - recovery satisfaction by using storage [%]
            # Storage_Turnkey_Cost - storage turnkey for each HX [€]
            # Total_Turnkey_Cost - total turnkey = hx + storage [€]
            # Recovered_Energy - yearly total recovered energy [kWh]

"""

from ......KB_General.equipment_details import equipment_details
from ......KB_General.fluid_material import fluid_material_cp


def design_hx_storage(df_profile, info_df_hx, above_pinch, storage_delta_T=5):

    # Defined vars
    maximum_water_storage_temperature = 90  # [ºC]

    # Storage design
    if len(info_df_hx) > 0:
        for pinch_case in info_df_hx:
            # get df_hx of each pinch case
            df_hx = pinch_case['df_hx']

            # initialize arrays for each pinch case
            new_volume_max_storage = 0
            vector_storage_volume = []
            vector_storage_satisfies = []
            vector_energy_year = []
            vector_storage_turn_key = []

            if df_hx.empty == False:
                for index, row in df_hx.iterrows():

                    # choose type of thermal storage - fixed values
                    if row['HX_Hot_Stream_T_Hot'] <= maximum_water_storage_temperature + storage_delta_T:
                        fluid = 'water'
                        cp_fluid = fluid_material_cp(fluid, maximum_water_storage_temperature)  # [kJ/(kg.K)]
                        rho_fluid = 1000  # [kg/m3]
                        cost_fluid = 0.0004  # [€/L]
                    else:
                        fluid = 'thermal_oil'
                        cp_fluid = fluid_material_cp(fluid,150)
                        rho_fluid = 920
                        cost_fluid = 0.5  # [€/L]

                    # get streams
                    power_hx = row['HX_Power']  # hx power

                   # if above_pinch == True:
                    #    index_cold_stream = row['Original_Stream_Out']  # original index stream - to get hourly profile
                   #     index_hot_stream = row['Original_Stream_In']
                    #else:
                   #     index_cold_stream = row['Original_Stream_In']
                   #     index_hot_stream = row['Original_Stream_Out']

                    index_cold_stream = row['HX_Original_Cold_Stream']  # original index stream - to get hourly profile
                    index_hot_stream = row['HX_Original_Hot_Stream']

                    profile_cold_stream = df_profile.loc[index_cold_stream]  # hourly profile with 0 and 1
                    profile_hot_stream = df_profile.loc[index_hot_stream]

                    # compute surplus/deficit/coincident hours
                    hours_cold = sum(profile_cold_stream[profile_cold_stream == 1])
                    hours_hot = sum(profile_hot_stream[profile_hot_stream == 1])
                    hours_coincident = profile_hot_stream[
                        profile_hot_stream == profile_cold_stream]  # check when both streams have same schedule
                    hours_coincident = sum(hours_coincident[hours_coincident != 0])  # remove when both not operating

                    # Storage
                    # create 10 days profile to assure correct storage computation
                    profile_cold_stream = profile_cold_stream.head(239)  # get first 240 hours
                    profile_hot_stream = profile_hot_stream.head(239)

                    # check if storage needed
                    if hours_cold == hours_coincident:
                        volume_storage = 0  # [m3]
                        vector_storage_volume.append(volume_storage)  # [m3]
                        vector_storage_satisfies.append(0)  # hours storage satisfies heat needs [%]
                        vector_storage_turn_key.append(0)  # storage turnkey [€]

                    else:
                        # hot stream surplus - satisfaction 100%
                        if hours_hot >= hours_cold:
                            # start with theoretical max storage
                            volume_max_storage = hours_cold * power_hx
                            find_min_storage = True  # find minimum storage needed
                            vector_storage_satisfies.append(100)

                            while find_min_storage == True:
                                power_storage = volume_max_storage  # start with full storage
                                hours_deficit = 0  # hours cold surplus

                                for hour in range(len(profile_cold_stream)):
                                    # deficit
                                    if profile_cold_stream[hour] == 1 and profile_hot_stream[hour] == 0:
                                        power_storage -= power_hx  # remove power from storage
                                        hours_deficit += 1

                                    # surplus
                                    if profile_cold_stream[hour] == 0 and profile_hot_stream[hour] == 1:
                                        if power_storage < volume_max_storage:
                                            power_storage += power_hx  # add power to storage

                                    # storage cannot reach 0 - break cycle. Minimum storage was already saved in
                                    # previous iteration
                                    if power_storage < 0:
                                        find_min_storage = False  # minimum storage found
                                        break

                                # minimum storage not found, continue to decrease initial max storage
                                if find_min_storage == True:
                                    new_volume_max_storage = volume_max_storage  # save previous iteration max storage
                                    volume_max_storage -= power_hx  # next iteration initial max storage

                        # cold stream surplus - satisfaction NOT 100%
                        else:
                            # Find storage as function of maximum hot surplus hours
                            storage_final = 0
                            power_storage = 0  # storage power starting at 0
                            hours_match = 0
                            hours_deficit = 0

                            for hour in range(len(profile_cold_stream)):
                                # deficit
                                if profile_cold_stream[hour] == 1 and profile_hot_stream[hour] == 0:
                                    hours_deficit += 1
                                    if power_storage > 0:
                                        hours_match += 1
                                        power_storage -= power_hx  # remove power from storage

                                # surplus
                                if profile_cold_stream[hour] == 0 and profile_hot_stream[hour] == 1:
                                    power_storage += power_hx  # add power to storage

                                # find storage that can receive has much surplus power as possible
                                if power_storage > storage_final:
                                    storage_final = power_storage

                            new_volume_max_storage = storage_final
                            storage_satisfies = hours_match / hours_deficit * 100
                            vector_storage_satisfies.append(storage_satisfies)

                        # compute storage volume
                        hot_stream_T_hot = row['HX_Hot_Stream_T_Hot']
                        hot_stream_T_cold = row['HX_Hot_Stream_T_Cold']
                        volume_storage = new_volume_max_storage * 3600 / (
                                    cp_fluid * rho_fluid * (hot_stream_T_hot - hot_stream_T_cold))  # [m3]
                        vector_storage_volume.append(volume_storage)

                        # compute turnkey
                        global_conversion_efficiency, om_fix, storage_turn_key = equipment_details('thermal_storage',
                                                                                                   volume_storage)
                        storage_fluid_turn_key = volume_storage * cost_fluid
                        storage_total_turn_key = storage_turn_key + storage_fluid_turn_key
                        vector_storage_turn_key.append(storage_total_turn_key)

                    if hours_cold == hours_coincident:
                        vector_energy_year.append(power_hx * hours_cold)  # [kWh]

                    elif hours_hot >= hours_cold:
                        vector_energy_year.append(power_hx * hours_cold)

                    else:
                        vector_energy_year.append(power_hx * hours_hot)


                ######################################################################
                # OUTPUT
                # update df_hx

                df_hx['Storage'] = vector_storage_volume  # update storage for each HX [m3]
                df_hx['Storage_Satisfies'] = vector_storage_satisfies  # recovery satisfaction by using storage [%]
                df_hx['Storage_Turnkey_Cost'] = vector_storage_turn_key  # storage turnkey for each HX [€]
                df_hx['Total_Turnkey_Cost'] = df_hx['HX_Turnkey_Cost'] + df_hx['Storage_Turnkey_Cost']  # total turnkey [€]
                df_hx['Recovered_Energy'] = vector_energy_year  # yearly total recovered energy [kWh]

    return info_df_hx