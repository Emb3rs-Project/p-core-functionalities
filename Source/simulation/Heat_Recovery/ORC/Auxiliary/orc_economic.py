"""
alisboa/jmcunha


##############################
INFO: Generate ORC economic data estimate.


##############################
INPUT:
        # orc_years_working - number of expected orc life
        # country
        # consumer_type - 'household' or 'non-household'
        # df_data

        Where in df_data:
            # streams_id - vector with streams ID
            # electrical_generation_nominal [kW]
            # electrical_generation_yearly [kWh]
            # excess_heat_supply_capacity [kW]
            # conversion_efficiency []
            # capex - intermediate + orc capex [€]
            # om_fix - om fix intermediate + orc capex [€/year]
            # om_var  - om var intermediate + orc capex [€]
            # electrical_generation_yearly_capex


##############################
OUTPUT: df with:
            # streams_id - vector with streams ID
            # electrical_generation_nominal [kW]
            # electrical_generation_yearly [kWh]
            # excess_heat_supply_capacity [kW]
            # conversion_efficiency []
            # capex - intermediate + orc capex [€]
            # om_fix - om fix intermediate + orc capex [€/year]
            # om_var  - om var intermediate + orc capex [€]
            # electrical_generation_yearly_capex
            # npv_5 - NPV 5 years
            # npv_15 - NPV 15 years
            # npv_25 - NPV 25 years
            # payback - number of years to reach NPV = 0


"""

from ......KB_General.fuel_properties import fuel_properties
from ......KB_General.get_interest_rate import get_interest_rate
import pandas as pd


def economic_data(orc_years_working, country, consumer_type,df_data):

    interest_rate = get_interest_rate(country)
    fuel_data = fuel_properties(country, 'electricity', consumer_type)
    electricity_price = fuel_data['price']


    # cash_flow = - om_var - om_fix + savings_electricity
    for year in range(1, orc_years_working + 1):
        savings_electricity = electricity_price * df_data['electrical_generation_yearly']
        df_cash_flow[str(year)] = (-df_data['om_fix'] + -df_data['om_var'] + savings_electricity) / ((1 + interest_rate) ** year)



    # update columns for Business Module
    df_data['discount_rate'] = interest_rate
    df_data['lifetime'] = orc_years_working


    return df_data

