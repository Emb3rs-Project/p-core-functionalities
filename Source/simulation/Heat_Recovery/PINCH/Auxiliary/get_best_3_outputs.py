"""
alisboa/jmcunha

##############################
INFO: Get bes 3 outputs according to inputs. Compute all info for the Business module.

##############################


"""

def get_best_3_outputs(all_df,df_optimization):

    output_vector = []

    for index, row in df_optimization.iterrows():

        output_vector.append({
            'capex': row['turnkey'],  # turnkey hx + storage
            'lifetime': 20,  # considered lifetime
            'om_fix':row['om_fix'],
            'discount_rate': 0.02,
            'co2_savings': row['co2_savings']/row['energy_recovered'],
            'money_savings': row['money_savings'] ,
            'energy_dispatch': row['energy_recovered'],
            'equipment_detailed_savings': all_df[int(df_optimization['index'].loc[index])][1].to_dict(orient='records'),  # each equipment savings
            'pinch_hx_data': all_df[int(df_optimization['index'].loc[index])][0].to_dict(orient='records')  # all pinch data information
            })

    return output_vector