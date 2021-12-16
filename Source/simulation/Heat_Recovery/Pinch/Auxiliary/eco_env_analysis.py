"""
alisboa/jmcunha

##############################
INFO: Environment an economical analysis. This analysis is only performed when processes and equipments are given. The
      objective is to compute the monetary, energy, and co2 emissions savings from each equipment, when implementing the
      respective pinch design.


##############################
INPUT:
        # info_pinch - array with dictionaries of pinch cases
        # objects_to_analyze - all objects whose the streams are analyzed
        # all_input_objects - all objects introduced at the main function 'convert_pinch'
        # country


##############################
RETURN: array info_pinch with dictionaries for each pinch case. It is added a the key 'df_equipment_economic' to each
        pinch case:

            Where in df_equipment_economic, the following keys:
                # df_equipment_economic = {
                #                               'Equipment_ID'  [ID]
                #                               'CO2_Savings_Year'  [kg CO2/year]
                #                               'Recovered_Energy'  [kWh/year]
                #                               'Savings_Year'  [€]
                #                               'Total_Turnkey_Cost'  [€]
                #                               }


"""

import pandas as pd
from ......KB_General.fuel_properties import fuel_properties


def eco_env_analysis(info_pinch, objects_to_analyze, all_input_objects, country):

    for pinch_case in info_pinch:

        # get pinch case
        df_hx = pinch_case['df_hx']

        if df_hx is not None:
            # create empty df_economic
            df_economic = pd.DataFrame(columns=['Equipment_ID',
                                                'Recovered_Energy',
                                                'CO2_Savings_Year',
                                                'Savings_Year',
                                                'Total_Turnkey'])

            for index, row in df_hx.iterrows():
                find = True
                while find == True:
                    for object in objects_to_analyze:  # processes/equipment
                        for stream in object['streams']:
                            if stream['id'] == row['HX_Original_Cold_Stream']:
                                save_object = object
                                find = False
                                break
                        if find == False:  # match found
                            break
                    if find == True:  # no match found - may happen with isolated streams
                        break
                if find == True:  # no match found - may happen with isolated streams
                    pass
                else:
                    # compute equipment savings
                    if save_object['object_type'] == 'equipment':

                        data = fuel_properties(country, save_object['fuel_type'], 'non-household')
                        co2_emission_per_kw = float(data['co2_emissions'])
                        price = data['price']
                        df_economic = df_economic.append({
                            'Equipment_ID': save_object['id'],
                            'CO2_Savings_Year': row['Recovered_Energy'] * co2_emission_per_kw,
                            'Recovered_Energy': row['Recovered_Energy'],
                            'Savings_Year': row['Recovered_Energy'] * price,
                            'Total_Turnkey': row['Total_Turnkey_Cost'], }
                            , ignore_index=True)

                    # compute equipment savings which heat/cool respective processes
                    elif save_object['object_type'] == 'process':  # object.type = 'process'

                        for equipment in all_input_objects:
                            if save_object['equipment'] == equipment['id']:  # find equipment that supplies process
                                break
                            else:
                                equipment = 'not found'

                        data = fuel_properties(country, equipment['fuel_type'], 'non-household')
                        price = data['price']
                        co2_emission_per_kw = data['co2_emissions']

                        df_economic = df_economic.append({
                            'Equipment_ID': save_object['equipment'],
                            'CO2_Savings_Year': row['Recovered_Energy'] * co2_emission_per_kw,
                            'Recovered_Energy': row['Recovered_Energy'],
                            'Savings_Year': row['Recovered_Energy'] * price,
                            'Total_Turnkey': row['Total_Turnkey_Cost'], }
                            , ignore_index=True)

                    else:  # object.type = 'isolated_stream'
                        df_economic = df_economic.append({
                            'Equipment_ID': 'isolated_stream',
                            'CO2_Savings_Year': row['Recovered_Energy'] * co2_emission_per_kw,
                            'Recovered_Energy': row['Recovered_Energy'],
                            'Savings_Year': row['Recovered_Energy'] * price,
                            'Total_Turnkey': row['Total_Turnkey'], }
                            , ignore_index=True)


                # aggregate same Equipment ID savings in df_equipment_economic
                equipment_id = df_economic['Equipment_ID'].values

                for id in equipment_id:

                    df_equipment_economic = pd.DataFrame(
                        columns=['Equipment_ID', 'Recovered_Energy', 'CO2_Savings_Year', 'Savings_Year',
                                 'Total_Turnkey'])

                    df_equipment_id = df_economic[df_economic['Equipment_ID'] == id]
                    total_recovered_heat = df_equipment_id['Recovered_Energy'].sum()
                    total_savings_year = df_equipment_id['Savings_Year'].sum()
                    total_turnkey = df_equipment_id['Total_Turnkey'].sum()

                    for equipment in all_input_objects:
                        if id == equipment['id']:  # find equipment that supplies process
                            break

                    df_equipment_economic = df_equipment_economic.append({
                        'Equipment_ID': id,
                        'CO2_Savings_Year': row['Recovered_Energy'] * co2_emission_per_kw,
                        'Recovered_Energy': total_recovered_heat,
                        'Savings_Year': total_savings_year,
                        'Total_Turnkey': total_turnkey, }
                        , ignore_index=True)

            pinch_case['df_equipment_economic'] = df_equipment_economic


    return info_pinch