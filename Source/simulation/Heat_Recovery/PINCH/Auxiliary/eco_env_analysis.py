
import pandas as pd
from ......KB_General.fuel_properties import fuel_properties

def eco_env_analysis(vector_df_hx,objects,all_objects,all_df):

    for df_hx in vector_df_hx:
        df_economic = pd.DataFrame(columns=['Equipment_ID',
                                            'Recovered_Energy',
                                            'CO2_Savings_Year',
                                            'Savings_Year',
                                            'Total_Turnkey'])
        for index, row in df_hx.iterrows():
            find = True
            while find == True:
                for object in objects:  # processes/equipment
                    for stream in object['streams']:
                        if stream['id'] == row['Original_Cold_Stream']:
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
                if save_object['object_type'] == 'equipment':
                    data = fuel_properties('Portugal', save_object.fuel_type, 'non-household')

                    co2_emission_per_kw = float(data['CO2_emission'])
                    cost = data['price']
                    df_economic = df_economic.append({
                                                         'Equipment_ID':save_object['id'],
                                                         'CO2_Savings_Year':row[
                                                                                'Recovered_Energy'] * co2_emission_per_kw,
                                                         'Recovered_Energy':row['Recovered_Energy'],
                                                         'Savings_Year':row['Recovered_Energy'] * cost,
                                                         'Total_Turnkey':row['Total_Turnkey'], }
                                                     , ignore_index=True)

                elif save_object['object_type'] == 'process':  # object.type = 'process'

                    for equipment in all_objects:
                        if save_object['equipment'] == equipment['id']:  # find equipment that supplies process
                            break
                        else:
                            equipment = 'not found'

                    data = fuel_properties('Portugal', equipment['fuel_type'], 'non-household')
                    cost = data['price']
                    co2_emission_per_kw = data['co2_emissions']

                    df_economic = df_economic.append({
                        'Equipment_ID':save_object['equipment'],
                        'CO2_Savings_Year':row[
                                               'Recovered_Energy'] * co2_emission_per_kw,
                        'Recovered_Energy':row['Recovered_Energy'],
                        'Savings_Year':row['Recovered_Energy'] * cost,
                        'Total_Turnkey':row['Total_Turnkey'], }
                        , ignore_index=True)

                else:  # object.type = 'isolated_stream'
                    #################
                    # manuly flow
                    df_economic = df_economic.append({
                        'Equipment_ID':'isolated_stream',
                        'CO2_Savings_Year':row['Recovered_Energy'] * co2_emission_per_kw,
                        'Recovered_Energy':row['Recovered_Energy'],
                        'Savings_Year':row['Recovered_Energy'] * cost,
                        'Total_Turnkey':row['Total_Turnkey'], }
                        , ignore_index=True)

            # Agreggate same Equipment ID savings in df_equipment_economic
            equipment_id = df_economic['Equipment_ID'].values

            for id in equipment_id:
                df_equipment_economic = pd.DataFrame(
                    columns=['Equipment_ID', 'Recovered_Energy', 'CO2_Savings_Year', 'Savings_Year',
                             'Total_Turnkey'])
                df_equipment_id = df_economic[df_economic['Equipment_ID'] == id]
                total_recovered_heat = df_equipment_id['Recovered_Energy'].sum()
                total_savings_year = df_equipment_id['Savings_Year'].sum()
                total_turnkey = df_equipment_id['Total_Turnkey'].sum()

                for equipment in all_objects:
                    if id == equipment['id']:  # find equipment that supplies process
                        break
                df_equipment_economic = df_equipment_economic.append({
                                                                         'Equipment_ID':id,
                                                                         'CO2_Savings_Year':row['Recovered_Energy'] * co2_emission_per_kw,
                                                                         'Recovered_Energy':total_recovered_heat,
                                                                         'Savings_Year':total_savings_year,
                                                                         'Total_Turnkey':total_turnkey, }
                                                                     , ignore_index=True)

        all_df.append([df_hx, df_equipment_economic])


    return all_df