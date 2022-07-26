def get_best_x_outputs(info_pinch, df_optimization, lifetime, pinch_delta_T_min, stream_table,stream_combination_not_feasible,interest_rate):
    """Get best options

    Get best x (depends on the number of options desired) design solutions according to inputs.
    Compute all info for the Business module.

    Parameters
    ----------
    info_pinch : df
        Designed heat exchangers data

    df_optimization : df
        Techno economical parameters to evaluate best options

    lifetime : int

    pinch_delta_T_min : float

    stream_table : df
        All streams characterization data

    stream_combination_not_feasible : list
        Streams ID

    interest_rate : float
        []

    Returns
    -------
    best_x_options : list
        Best options detailed data

    """


    best_x_options = []

    solution_order = 1

    for index, row in df_optimization.iterrows():

       _info_pinch = info_pinch[int(df_optimization['index'].loc[index])-1]


       best_x_options.append({
            "stream_table":stream_table,
            "stream_combination_not_feasible":stream_combination_not_feasible,
            "_info_pinch": _info_pinch,
            'ID': _info_pinch['ID'],
            'streams': _info_pinch['streams'],
            'streams_info': _info_pinch['streams_info'],
            'capex': row['capex'],  # turnkey hx + storage
            'om_fix': row['om_fix'],
            'hot_utility': _info_pinch['hot_utility'],
            'cold_utility': _info_pinch['cold_utility'],
            'lifetime': lifetime,  # considered lifetime
            'co2_savings': row['co2_savings'] / row['energy_recovered'],
            'money_savings': row['money_savings'] / row['energy_recovered'],
            'energy_dispatch': row['energy_recovered'],
            'discount_rate': interest_rate,
            #'equipment_detailed_savings': _info_pinch['df_equipment_economic'].to_dict(orient='records'),  # each equipment savings
            'pinch_temperature': _info_pinch['pinch_temperature'] - pinch_delta_T_min,
            'pinch_hx_data': _info_pinch['df_hx'].to_dict(orient='records'),  # all pinch data information
            'theo_minimum_hot_utility': _info_pinch['theo_minimum_hot_utility'],
            'theo_minimum_cold_utility': _info_pinch['theo_minimum_cold_utility'],
        })

       solution_order += 1

    return best_x_options