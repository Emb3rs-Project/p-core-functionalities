"""
alisboa/jmcunha

##############################
INFO: Get best x (depends on the number of options desired) design solutions according to inputs.
      Compute all info for the Business module.


##############################
INPUT:
        # info_pinch
        # df_optimization
        # country
        # lifetime

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
        # best_x_options - list with best x design solutions, e.g. best_x_options=[best_option_1,best_option_2,...]

        Where in each solution, for example:
        # best_option_1 = {
        #                 'ID' - designed solution ID  [ID]
        #                 'streams' - streams in pinch design ID [ID]
        #                 'capex'  [€]
        #                 'om_fix' - yearly om fix costs [€/year]
        #                 'hot_utility' - power of the hot utility needed, so that the cold streams reach their target_temperature  [kW]
        #                 'cold_utility' - power of the cold utility needed, so that the hot streams reach their target_temperature  [kW]
        #                 'lifetime' - considered lifetime  [year]
        #                 'co2_savings' - annualized co2 savings by implementing the pinch design [kg CO2/kWh]
        #                 'money_savings' - annualized energy savings by implementing the pinch design  [€/kWh]
        #                 'energy_dispatch' - yearly energy recovered by implementing the pinch design [kWh/year]
        #                 'discount_rate'  []
        #                 'pinch_temperature' - design pinch temperature [ºC]
        #                 'theo_minimum_hot_utility' - theoretical power of the hot utility needed, so that the cold streams reach their target_temperature  [kW]
        #                 'theo_minimum_cold_utility' - theoretical power of the cold utility needed, so that the hot streams reach their target_temperature  [kW]
        #                 'equipment_detailed_savings', - list with equipment details saving when implementing the pinch design
        #                 'pinch_hx_data' - list with pinch design data
        #                 }


"""

from ......KB_General.get_interest_rate import get_interest_rate
from ..make_pinch_design_draw import make_pinch_design_draw


def get_best_x_outputs(info_pinch,df_optimization,country,lifetime,pinch_delta_T_min,kb):

    best_x_options = []

    interest_rate = get_interest_rate(country,kb)

    for index, row in df_optimization.iterrows():

        make_pinch_design_draw(info_pinch[int(df_optimization['index'].loc[index])]['streams'],
                               info_pinch[int(df_optimization['index'].loc[index])]['streams_info'],
                               info_pinch[int(df_optimization['index'].loc[index])]['pinch_temperature'],
                               info_pinch[int(df_optimization['index'].loc[index])]['df_hx'].to_dict(orient='records'),
                              info_pinch[int(df_optimization['index'].loc[index])]['pinch_delta_T_min']
                               )


        best_x_options.append({
            'ID': info_pinch[int(df_optimization['index'].loc[index])]['ID'],
            'streams': info_pinch[int(df_optimization['index'].loc[index])]['streams'],
            'streams_info': info_pinch[int(df_optimization['index'].loc[index])]['streams_info'],
            'capex': row['turnkey'],  # turnkey hx + storage
            'om_fix': row['om_fix'],
            'hot_utility': info_pinch[int(df_optimization['index'].loc[index])]['hot_utility'],
            'cold_utility': info_pinch[int(df_optimization['index'].loc[index])]['cold_utility'],
            'lifetime': lifetime,  # considered lifetime
            'co2_savings': row['co2_savings'] / row['energy_recovered'],
            'money_savings': row['money_savings'] / row['energy_recovered'],
            'energy_dispatch': row['energy_recovered'],
            'discount_rate': interest_rate,
            'equipment_detailed_savings': info_pinch[int(df_optimization['index'].loc[index])]['df_equipment_economic'].to_dict(orient='records'),  # each equipment savings
            'pinch_temperature': info_pinch[int(df_optimization['index'].loc[index])]['pinch_temperature'] - pinch_delta_T_min,
            'pinch_hx_data': info_pinch[int(df_optimization['index'].loc[index])]['df_hx'].to_dict(orient='records'),  # all pinch data information
            'theo_minimum_hot_utility': info_pinch[int(df_optimization['index'].loc[index])]['theo_minimum_hot_utility'],
            'theo_minimum_cold_utility': info_pinch[int(df_optimization['index'].loc[index])]['theo_minimum_cold_utility'],
        })


    return best_x_options