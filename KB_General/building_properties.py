import json

def building_properties(country,building_type):

    u_wall = 0
    u_roof = 0
    u_glass = 0
    u_floor = 0
    alpha_wall = 0
    alpha_floor = 0
    alpha_glass = 0
    tau_glass = 0
    capacitance_floor = 0
    capacitance_roof = 0
    capacitance_wall = 0
    air_change_per_second = 0

    with open('C:/Users/alisboa/PycharmProjects/emb3rs/KB_General/Json_files/building_properties.json') as f:
        data = json.load(f)

    for dict in data['building_properties']:
        if dict['country'] == country:
            if building_type == 'office' or building_type == 'hotel':
                u_wall = float(dict['residential_u_wall'])  # Wall heat transfer coefficient [W/m2.K]
                u_roof = float(dict['residential_u_roof'])  # Roof heat transfer coefficient [W/m2.K]
                u_glass = float(dict['residential_u_glass'])  # Glass heat transfer coefficient [W/m2.K]
                u_floor = float(dict['residential_u_floor'])  # Floor heat transfer coefficient [W/m2.K]
            else:
                u_wall = float(dict['non-residential_u_wall'])
                u_roof = float(dict['non-residential_u_roof'])
                u_glass = float(dict['non-residential_u_glass'])
                u_floor = float(dict['non-residential_u_floor'])

            alpha_wall = float(dict['alpha_wall'])
            alpha_floor = float(dict['alpha_floor'])
            alpha_glass = float(dict['alpha_glass'])
            tau_glass = float(dict['tau_glass'])
            capacitance_floor = float(dict['capacitance_floor'])  # Floor specific heat capacitance [J/m2.K]
            capacitance_roof = float(dict['capacitance_roof'])  # Roof specific heat capacitance [J/m2.K]
            capacitance_wall = float(dict['capacitance_wall'])  # Wall specific heat capacitance [J/m2.K]
            air_change_hour = float(dict['air_change_hour'])/3600  # [1/s]
            break


    if tau_glass == u_wall == u_roof == u_glass == capacitance_roof == capacitance_wall == air_change_hour == 0:
        dict = data['building_properties'][0]

        if building_type == 'office' or building_type == 'hotel':
            u_wall = float(dict['residential_u_wall'])
            u_roof = float(dict['residential_u_roof'])
            u_glass = float(dict['residential_u_glass'])
            u_floor = float(dict['residential_u_floor'])
        else:
            u_wall = float(dict['non-residential_u_wall'])
            u_roof = float(dict['non-residential_u_roof'])
            u_glass = float(dict['non-residential_u_glass'])
            u_floor = float(dict['non-residential_u_floor'])

        alpha_wall = float(dict['alpha_wall'])
        alpha_floor = float(dict['alpha_floor'])
        alpha_glass = float(dict['alpha_glass'])
        tau_glass = float(dict['tau_glass'])
        capacitance_floor = float(dict['capacitance_floor'])
        capacitance_roof = float(dict['capacitance_roof'])
        capacitance_wall = float(dict['capacitance_wall'])
        air_change_hour = float(dict['air_change_hour'])  # [1/h]

    return u_wall,u_roof,u_glass,u_floor,tau_glass,alpha_wall,alpha_floor,alpha_glass,capacitance_wall,capacitance_floor,capacitance_roof,air_change_hour



