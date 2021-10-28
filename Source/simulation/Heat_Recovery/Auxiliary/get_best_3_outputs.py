
def get_best_3_outputs(all_df,df_optimization):

    output_vector = []

    for index, row in df_optimization.iterrows():
        output_vector.append({
            'total_turnkey': row['turnkey',
            'total_co2_savings': row['co2_savings'],
            'total_energy_recovered': row['energy_recovered'],
            'equipment_detailed_savings':all_df[df_optimization['index'][1].__dict__,
            'pinch_hx_data': all_df[df_optimization['index'][0].__dict__
            })

    return output_vector