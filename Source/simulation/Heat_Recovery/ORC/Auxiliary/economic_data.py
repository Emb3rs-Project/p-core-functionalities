from KB_General.fuel_properties import fuel_properties
from KB_General.get_interest_rate import get_interest_rate


def economic_data(orc_years_working, country, consumer_type,df_data):

    cashflow_vector = []
    interest_rate = get_interest_rate(country)
    fuel_data = fuel_properties(country,'electricity',consumer_type)
    electricity_price = fuel_data['price']

    # cashflows = - om_var - om_fix + savings_electricity
    for year in range(1,orc_years_working+1):
        savings_electricity = electricity_price*df_data['electrical_generation_yearly'].values()
        cashflow_vector.append((df_data['om_fix'].values()+df_data['om_var'].values()+savings_electricity)/(1+interest_rate)**year)

    # compute npv for 3 time splits
    for years in [orc_years_working/3, orc_years_working*2/3,orc_years_working]:
        print(sum(cashflow_vector[0:5]))
        df_data['npv' + '2'] = df_data['turnkey'].value() + sum(cashflow_vector[0:years])

    # get payback
    find_npv_zero = - df_data['turnkey'].value()
    for year,cash_flow in enumerate(cashflow_vector):
        find_npv_zero +=  cash_flow

        if find_npv_zero > 0:
            df_data['payback'] = year + 1 # since it starts in zero
        else:
            df_data['payback'] = None



    return df_data