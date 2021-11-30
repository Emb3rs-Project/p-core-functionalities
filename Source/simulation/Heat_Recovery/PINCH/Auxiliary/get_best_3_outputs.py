"""
alisboa/jmcunha

##############################
INFO: Get bes 3 outputs according to inputs. Compute all info for the Business module.

##############################


"""

def get_best_3_outputs(info_pinch,df_optimization):

    output_vector = []


    for index, row in df_optimization.iterrows():

        output_vector.append({
            'ID': info_pinch[int(df_optimization['index'].loc[index])]['ID'],
            'streams': info_pinch[int(df_optimization['index'].loc[index])]['streams'],
            'capex': row['turnkey'],  # turnkey hx + storage
            'om_fix': row['om_fix'],
            'hot_utility': info_pinch[int(df_optimization['index'].loc[index])]['hot_utility'],
            'cold_utility': info_pinch[int(df_optimization['index'].loc[index])]['cold_utility'],
            'lifetime': 20,  # considered lifetime
            'co2_savings': row['co2_savings'] / row['energy_recovered'],
            'money_savings': row['money_savings'],
            'energy_dispatch': row['energy_recovered'],
            'discount_rate': 0.02,
             'equipment_detailed_savings': info_pinch[int(df_optimization['index'].loc[index])]['df_equipment_economic'].to_dict(orient='records'),  # each equipment savings
            'pinch_temperature': info_pinch[int(df_optimization['index'].loc[index])]['pinch_temperature'],
            'pinch_hx_data': info_pinch[int(df_optimization['index'].loc[index])]['df_hx'].to_dict(orient='records'),  # all pinch data information
            'theo_minimum_hot_utility': info_pinch[int(df_optimization['index'].loc[index])]['theo_minimum_hot_utility'],
            'theo_minimum_cold_utility': info_pinch[int(df_optimization['index'].loc[index])]['theo_minimum_cold_utility'],
        })


    return output_vector