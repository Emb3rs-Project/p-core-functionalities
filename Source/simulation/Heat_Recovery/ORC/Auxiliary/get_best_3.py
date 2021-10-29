


def get_best_3(df):

    output_vector = []

    for index, row in df.iterrows():
        output_vector.append( {
            'electrical_generation_nominal':row['electrical_generation_nominal'],  # [kW]
            'electrical_generation_yearly':row['electrical_generation_yearly'],  # [kW]
            'excess_heat_supply_capacity':row['excess_heat_supply_capacity'],  # [kW]
            'conversion_efficiency':row['conversion_efficiency'],  # [%]
            'turnkey':row['turnkey'],  # [€]
            'om_fix':row['om_fix'],  # [€/year]
            'om_var':row['om_var']  #
            }
            )
    return output_vector