"""
##############################
INFO: Generate ORC integration business data.

##############################
INPUT:  orc_years_working - number of expected orc life
        country
        consumer_type - 'household' or 'non-household'
        df_data

        Where in df_data:
            # streams_id - vector with streams ID
            # electrical_generation_nominal [kW]
            # electrical_generation_yearly [kWh]
            # excess_heat_supply_capacity [kW]
            # conversion_efficiency []
            # turnkey - intermediate + orc turnkey [€]
            # om_fix - om fix intermediate + orc turnkey [€/year]
            # om_var  - om var intermediate + orc turnkey [€]
            # electrical_generation_yearly_turnkey

##############################
OUTPUT: df with:
            # streams_id - vector with streams ID
            # electrical_generation_nominal [kW]
            # electrical_generation_yearly [kWh]
            # excess_heat_supply_capacity [kW]
            # conversion_efficiency []
            # turnkey - intermediate + orc turnkey [€]
            # om_fix - om fix intermediate + orc turnkey [€/year]
            # om_var  - om var intermediate + orc turnkey [€]
            # electrical_generation_yearly_turnkey
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
    fuel_data = fuel_properties(country,'electricity',consumer_type)
    electricity_price = fuel_data['price']

    # create cashdlows df
    df_cash_flow = pd.DataFrame()

    # cash_flow = - om_var - om_fix + savings_electricity
    for year in range(1,orc_years_working+1):
        savings_electricity = electricity_price*df_data['electrical_generation_yearly']
        df_cash_flow[str(year)] = (-df_data['om_fix'] + -df_data['om_var'] + savings_electricity)/((1 + interest_rate)**year)

    # compute npv for 3 time splits
    for year in [5,15,orc_years_working]:
        df_data['npv_' + str(year)] = -df_data['turnkey'] + df_cash_flow.iloc[:,0:int(year-1)].sum(axis=1)

    # get payback
    df_merge = pd.concat([-df_data['turnkey'],df_cash_flow], axis=1)
    find_npv_zero = df_merge.cumsum(axis=1)

    df_data['payback'] = None
    for index, row in find_npv_zero.iterrows():
        row = row[row >= 0]

        if row.empty is False:
            if row.iloc[0] > 0:
                df_data.loc[index,'payback'] = int(row.index[0])  # since it starts in zero

    return df_data