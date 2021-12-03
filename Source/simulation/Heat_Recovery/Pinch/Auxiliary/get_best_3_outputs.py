"""
alisboa/jmcunha

##############################
INFO: Get best 3 design solutions according to inputs.
      Compute all info for the Business module.


##############################
INPUT:
        # info_pinch
        # df_optimization

        Where in df_optimization, the following keys:
            # index - designed solution ID  [ID]
            # co2_savings [kg CO2/year]
            # money_savings [€/year]
            # energy_recovered  [kWh/year]
            # energy_investment  [€/kWh]
            # turnkey - design solution turnkey/capex [€]
            # om_fix - solution om fix  [€/year]


##############################
RETURN:
        # best_3 - list with best 3 design solutions

        Where in each solution:
            # ID - designed solution ID  [ID]
            # streams - streams ID  [ID]
            # capex - solution capex  [€]
            # om_fix - solution om fix  [€/year]
            # hot_utility - solution needed exterior heat supply  [kW]
            # cold_utility - solution needed exterior cold supply  [kW]
            # lifetime - considered lifetime  [year]
            # co2_savings  [kg CO2/kWh]
            # money_savings  [€/kWh]
            # energy_dispatch - heat recovered  [kWh/year]
            # discount_rate  []
            # equipment_detailed_savings - each equipment savings
            # pinch_temperature  [ºC]
            # pinch_hx_data - all pinch design data
            # theo_minimum_hot_utility - theoretical minimum solution needed exterior heat supply  [kW]
            # theo_minimum_cold_utility - theoretical minimum solution needed exterior cold supply  [kW]


"""

def get_best_3_outputs(info_pinch,df_optimization):

    best_3 = []

    for index, row in df_optimization.iterrows():

        best_3.append({
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


    return best_3