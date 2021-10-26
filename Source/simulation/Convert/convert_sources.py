"""
##############################
INFO: GET SOURCE CONVERTION TECHNOLOGIES TO SEND TEO

##############################
INPUT:  group_of_sources = [source_1,source_2,...] each source with dictionary {source_id,source_location,streams}
        last_iteration_data = [] or output from first iteration
        sink_group_grid_supply_temperature
        sink_group_grid_return_temperature
        grid_losses -> vector with vectors with grid losses for each stream of source  [[source_1_stream_1_loss, source_1_stream_2_loss],...]

        Where in each source of group_of_sources :
            # source_id
            # source_location = [country,latitude,longitude]
            # consumer_type - 'household' or 'non-household'
            # streams -> vector with dictionaries with {stream_id, object_type, stream_type, fluid, capacity, supply_temperature, target_temperature,hourly_generation}


##############################
OUTPUT: vector with multiple dictionaries [{'source_id', 'stream_id', 'hourly_stream_capacity', 'conversion_technologies'},..]
      Where:
         # source_id
         # source_grid_supply_temperature
         # source_grid_return_temperature
         # streams_converted

            Where in streams_converted:
             # stream_id
             # hourly_stream_capacity [kWh]
             # conversion_technologies - multiple dictionaries with technologies possible to implement

              Where in conversion_technologies:
                # conversion_technologies = {
                #         'equipment'
                #         'max_capacity'  [kW]
                #         'turnkey_a' [€/kW]
                #         'turnkey_b' [€]
                #         'conversion_efficiency'  []
                #         'om_fix'   [€/year.kW]
                #         'om_var'  [€/kWh]
                #         'emissions'  [kg.CO2/kWh]
                #         'tecnhologies' - technologies info in details,
                #     }




"""

from General.Convert_Equipments.Auxiliary.source_get_hx_temperatures import source_get_hx_temperatures
from General.Convert_Equipments.Convert_Options.add_boiler import Add_Boiler
from General.Convert_Equipments.Convert_Options.add_hx import Add_HX
from General.Convert_Equipments.Convert_Options.add_solar_thermal import Add_Solar_Thermal
from General.Convert_Equipments.Convert_Options.add_heat_pump import Add_Heat_Pump
from General.Convert_Equipments.Convert_Options.add_chp import Add_CHP
from General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from General.Convert_Equipments.Convert_Options.add_orc_cascaded import Add_ORC_Cascaded
from General.Convert_Equipments.Auxiliary.join_hx_and_technology import join_hx_and_technology
from Source.simulation.Auxiliary.design_orc import design_orc
from copy import copy
import urllib3
from bs4 import BeautifulSoup
import json


def convert_sources(in_var):

    # INPUT --------------
    group_of_sources = in_var.group_of_sources
    last_iteration_data = in_var.last_iteration_data  # data output from this function from first iteration
    sink_group_grid_supply_temperature = in_var.sink_group_grid_supply_temperature
    sink_group_grid_return_temperature = in_var.sink_group_grid_return_temperature
    grid_losses = in_var.grid_losses  # vector with losses for each source

    # Initialize array
    output = []

    output_converted = []
    conversion_technologies = []

    # Defined vars -----------------------
    ambient_temperature = 15
    max_grid_temperature = 120  # defined maximum hot water grid temperature [ºC]
    safety_temperature = 100  # if heat stream above this temperature, use intermediate oil circuit [ºC]

    # Grid Characteristics
    grid_fluid = 'water'
    grid_delta_T = sink_group_grid_supply_temperature - sink_group_grid_return_temperature
    intermediate_fluid = 'thermal_oil'

    # HX Characteristics
    hx_efficiency = 0.95
    hx_delta_T = 5

    # ORC Cascaded Characteristics
    orc_intermediate_fluid = 'water'
    orc_T_evap = 140  # defined var [ºC]
    orc_T_cond_out = 90  # defined var [ºC]
    orc_T_cond_in = 60  # defined var [ºC]

    # Convert_Options Characteristics
    power_fraction = 0.05  # Defined as 5%


    for source_index,source in enumerate(group_of_sources):

        latitude, longitude = source['location']

        try:
            urlcountr = 'https://nominatim.openstreetmap.org/reverse.php?format=json&3153965&accept-language=en'
            urlcountry = urlcountr + '&lat=' + str(latitude) + '&lon=' + str(longitude)
            urlcountry = json.loads(BeautifulSoup(urllib3.PoolManager().request('GET', urlcountry).data, "html.parser").text)
            country = urlcountry['address']['country']

        except:
            country = 'Portugal'


        consumer_type = source['consumer_type']

        # get conversion technologies for each stream
        for stream_index,stream in enumerate(source['streams']):

            # first iteration - grid losses not considered
            if grid_losses == []:
                power_last_iteration = 0
                delta_T_supply = 0
                delta_T_return = 0

            # second iteration - grid losses not considered
            else:
                # get source grid losses
                grid_losses_power = grid_losses[source_index][stream_index]

                # 1st step - Compute grid supply/return at source correction coefficients, considering average pipe supply/return temperatures as sink supply/return temperatures
                hot_pipe_delta_T = sink_group_grid_supply_temperature - ambient_temperature  # delta T, grid supply temperature pipe
                cold_pipe_delta_T = sink_group_grid_return_temperature - ambient_temperature  # delta T, grid return temperature pipe

                supply_coef = hot_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)  # correction coefficient
                return_coef = cold_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)

                # get source max power supplied on last iteration
                power_last_iteration = last_iteration_data[source_index]['streams_converted'][stream_index]['conversion_technologies'][0]['max_capacity'] * last_iteration_data[source_index]['streams_converted'][stream_index]['conversion_technologies'][0]['conversion_efficiency']
                #  TEO chooses power supplied by the stream?

                # 2nd step - Compute and converge temperatures of grid supply/return at source
                add_delta_T = (grid_delta_T) / (1 - grid_losses_power / power_last_iteration) - grid_delta_T
                delta_T_supply = add_delta_T * supply_coef
                delta_T_return = add_delta_T * return_coef

                converge = False
                while converge == False:
                    hot_pipe_T_average = ((sink_group_grid_supply_temperature + delta_T_supply) + sink_group_grid_supply_temperature) / 2
                    cold_pipe_T_average = ((sink_group_grid_return_temperature - delta_T_return) + sink_group_grid_return_temperature) / 2

                    hot_pipe_delta_T = hot_pipe_T_average - ambient_temperature  # grid supply temperature pipe
                    cold_pipe_delta_T = cold_pipe_T_average - ambient_temperature  # grid return temperature pipe

                    supply_coef = hot_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)
                    return_coef = cold_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)

                    add_delta_T = (grid_delta_T) / (1 - grid_losses_power / power_last_iteration) - grid_delta_T
                    new_delta_T_supply = add_delta_T * supply_coef
                    new_delta_T_return = add_delta_T * return_coef

                    if abs(new_delta_T_supply - delta_T_supply) < 0.001 and abs(new_delta_T_supply - delta_T_supply) < 0.001:
                        delta_T_supply = copy(new_delta_T_supply)
                        delta_T_return = copy(new_delta_T_return)
                        converge = True

                    else:
                        delta_T_supply = copy(new_delta_T_supply)
                        delta_T_return = copy(new_delta_T_return)


            source_grid_return_temperature = sink_group_grid_return_temperature - delta_T_return
            source_grid_supply_temperature = sink_group_grid_supply_temperature + delta_T_supply

            # only convert sources where grid supply temperature is inferior to max_grid_temperature
            if source_grid_supply_temperature <= max_grid_temperature:
                    # design/cost equipment
                    if stream['stream_type'] == 'excess_heat' or stream['stream_type'] == 'outflow':
                        # get stream hourly generation capacity
                        hourly_stream_capacity = stream['hourly_generation']

                        # get stream nominal capacity
                        stream_nominal_capacity = max(hourly_stream_capacity)  # [kW]

                        # design technologies
                        if stream['supply_temperature'] > stream['target_temperature']:
                            # get HX grid temperatures
                            hx_source_supply_temperature = source_grid_supply_temperature + hx_delta_T
                            hx_source_target_temperature = source_grid_return_temperature + hx_delta_T

                            if stream['supply_temperature'] >= safety_temperature:
                                hx_number = 2
                                intermediate_circuit = True
                            else:
                                hx_number = 1
                                intermediate_circuit = False



                            # heating technologies not needed
                            if stream['supply_temperature'] >= hx_source_supply_temperature + hx_delta_T*hx_number:
                                #  check if intermediate circuit is needed
                                if intermediate_circuit == True:
                                    # get intermediate circuit temperatures
                                    hx_intermediate_supply_temperature = source_grid_supply_temperature + hx_delta_T
                                    hx_intermediate_return_temperature = source_grid_return_temperature + hx_delta_T

                                    # add HX intermediate
                                    hx_intermediate_supply_temperature, hx_intermediate_return_temperature,hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(hx_intermediate_supply_temperature, hx_intermediate_return_temperature,stream['supply_temperature'], stream['target_temperature'], hx_delta_T)
                                    hx_power = stream_nominal_capacity * (abs(hx_stream_supply_temperature - hx_stream_target_temperature) / abs(stream['supply_temperature'] - stream['target_temperature']))
                                    stream_available_capacity = copy(hx_power)
                                    info_hx_intermediate = Add_HX(hx_stream_supply_temperature, hx_stream_target_temperature, stream['fluid'], hx_intermediate_supply_temperature, hx_intermediate_return_temperature,intermediate_fluid,  hx_power,power_fraction)

                                    # add intermediation circulation pumping
                                    info_pump_intermediate = Add_Pump(country, consumer_type,intermediate_fluid, info_hx_intermediate.available_power, power_fraction,hx_intermediate_supply_temperature, hx_intermediate_return_temperature)

                                    # add HX to grid
                                    hx_power = info_hx_intermediate.available_power
                                    info_hx_grid = Add_HX(hx_intermediate_supply_temperature, hx_intermediate_return_temperature, intermediate_fluid, source_grid_supply_temperature, source_grid_return_temperature,grid_fluid, hx_power,power_fraction)

                                    # add circulation pumping to grid
                                    info_pump_grid = Add_Pump(country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction,source_grid_supply_temperature, source_grid_return_temperature)

                                    info = join_hx_and_technology([info_hx_intermediate.data_teo,info_pump_intermediate.data_teo,info_hx_grid.data_teo,info_pump_grid.data_teo],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                    conversion_technologies.append(info)

                                else:
                                    # add HX to grid
                                    hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature = source_get_hx_temperatures(stream['supply_temperature'], stream['target_temperature'], source_grid_supply_temperature,source_grid_return_temperature, hx_delta_T)
                                    hx_power = stream_nominal_capacity / (abs(stream['target_temperature'] - stream['supply_temperature'])) * abs(hx_stream_supply_temperature - hx_stream_target_temperature)
                                    stream_available_capacity = copy(hx_power)
                                    info_hx_grid = Add_HX(hx_stream_supply_temperature, hx_stream_target_temperature, stream['fluid'], source_grid_supply_temperature, source_grid_return_temperature, grid_fluid, hx_power,power_fraction)

                                    # add circulation pumping to grid
                                    info_pump_grid = Add_Pump(country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction, hx_grid_supply_temperature, hx_grid_return_temperature)

                                    info = join_hx_and_technology([info_hx_grid.data_teo,info_pump_grid.data_teo],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                    conversion_technologies.append(info)


                                # add orc cascaded
                                orc_type,stream_available_capacity,orc_electrical_generation,overall_thermal_capacity,hx_stream_target_temperature,intermediate_circuit,hx_intermediate_supply_temperature,hx_intermediate_return_temperature = design_orc(stream['capacity'],stream['fluid'], stream['supply_temperature'],stream['target_temperature'], hx_delta_T,orc_T_cond_out, orc_T_evap, hx_efficiency)
                                if intermediate_circuit == True:
                                    hx_number = 1
                                else:
                                    hx_number = 0

                                if stream['supply_temperature'] >= (orc_T_evap + hx_delta_T*hx_number):
                                    info_technology = Add_ORC_Cascaded(orc_type, overall_thermal_capacity, orc_electrical_generation,power_fraction)

                                    # get intermediate circuit
                                    if intermediate_circuit == True:
                                        # add HX intermediate
                                        hx_stream_supply_temperature = stream['supply_temperature']
                                        hx_power = copy(stream_available_capacity)
                                        info_hx_intermediate = Add_HX(hx_stream_supply_temperature,hx_stream_target_temperature, stream['fluid'],hx_intermediate_supply_temperature,hx_intermediate_return_temperature,intermediate_fluid, hx_power, power_fraction)

                                        # add circulation pumping to intermediate circuit
                                        info_pump_intermediate = Add_Pump(country, consumer_type,orc_intermediate_fluid, info_hx_intermediate.available_power, power_fraction,hx_intermediate_supply_temperature,hx_intermediate_return_temperature)

                                    if orc_T_cond_out < (source_grid_supply_temperature + hx_delta_T):
                                        ################################################
                                        boiler_supply_capacity = info_technology.supply_capacity * (hx_source_supply_temperature - orc_T_cond_out)/(orc_T_cond_out - orc_T_cond_in)
                                        info_boiler = Add_Boiler(country, consumer_type, boiler_supply_capacity, power_fraction, hx_source_supply_temperature,orc_T_cond_out)
                                    else:
                                        boiler_supply_capacity = 0

                                    # add circulation pumping to grid
                                    if intermediate_circuit == True and orc_T_cond_out < (source_grid_supply_temperature + hx_delta_T) and orc_T_cond_in > (source_grid_return_temperature + hx_delta_T):
                                        info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,info_technology.supply_capacity ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                        info = join_hx_and_technology([info_hx_intermediate.data_teo,info_pump_intermediate.data_teo, info_technology.data_teo,info_boiler.data_teo, info_pump_grid.data_teo],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                    elif intermediate_circuit == True and orc_T_cond_out < (source_grid_supply_temperature + hx_delta_T):
                                        info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,info_technology.supply_capacity * (orc_T_cond_out - (source_grid_return_temperature + hx_delta_T))/(source_grid_supply_temperature-source_grid_return_temperature) ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                        info = join_hx_and_technology([info_hx_intermediate.data_teo,info_pump_intermediate.data_teo, info_technology.data_teo,info_pump_grid.data_teo],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                    elif orc_T_cond_out < (source_grid_supply_temperature + hx_delta_T) and orc_T_cond_in > (source_grid_return_temperature + hx_delta_T):
                                        info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,info_technology.supply_capacity,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                        info = join_hx_and_technology([info_technology.data_teo, info_boiler.data_teo, info_pump_grid.data_teo],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                    elif orc_T_cond_out < (source_grid_supply_temperature + hx_delta_T):
                                        info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,(info_technology.supply_capacity + boiler_supply_capacity) * (hx_source_supply_temperature -(source_grid_return_temperature + hx_delta_T))/(hx_source_supply_temperature - orc_T_cond_in) ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                        info = join_hx_and_technology([info_technology.data_teo, info_boiler.data_teo, info_pump_grid.data_teo],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')
                                    else:
                                        info_pump_grid = Add_Pump(country, consumer_type, grid_fluid,info_technology.supply_capacity ,power_fraction, source_grid_supply_temperature,source_grid_return_temperature)
                                        info = join_hx_and_technology([info_technology.data_teo, info_pump_grid.data_teo],power_fraction, stream_available_capacity,info_pump_grid.supply_capacity, 'source')

                                    conversion_technologies.append(info)


                            # grid may not supply enough heat to the source
                            # add heating technologies
                            else:
                                # get heat extra needed to be supplied
                                needed_supply_capacity = stream['capacity'] * (hx_source_supply_temperature - stream['supply_temperature']) / (stream['supply_temperature'] - stream['target_temperature'])

                                # add HX to grid
                                hx_grid_supply_temperature, hx_grid_return_temperature, hx_stream_supply_temperature, hx_stream_target_temperature, = source_get_hx_temperatures(source_grid_supply_temperature, source_grid_return_temperature, hx_source_supply_temperature, stream['target_temperature'], hx_delta_T)
                                hx_power = stream_nominal_capacity * (abs(hx_stream_supply_temperature - hx_stream_target_temperature)) / abs(stream['supply_temperature'] - stream['target_temperature'])
                                info_hx_grid = Add_HX(hx_stream_supply_temperature,hx_stream_target_temperature, stream['fluid'], source_grid_supply_temperature, source_grid_return_temperature,grid_fluid, hx_power, power_fraction)
                                needed_yearly_capacity = sum([i - info_hx_grid.available_power for i in hourly_stream_capacity])  # [kWh]
                                stream_available_capacity = stream_nominal_capacity * (abs(stream['supply_temperature'] - hx_stream_target_temperature)) / abs(stream['supply_temperature'] - stream['target_temperature'])

                                # add circulation pumping to grid
                                info_pump_grid = Add_Pump(country, consumer_type,grid_fluid, info_hx_grid.available_power, power_fraction, source_grid_supply_temperature, source_grid_return_temperature)

                                # add boiler
                                info_technology = Add_Boiler(country, consumer_type,needed_supply_capacity, power_fraction, hx_source_supply_temperature, stream['supply_temperature'])

                                info = join_hx_and_technology([info_hx_grid.data_teo,info_pump_grid.data_teo,info_technology.data_teo],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                conversion_technologies.append(info)

                                # add solar thermal
                                info_technology = Add_Solar_Thermal(country, latitude, longitude, needed_yearly_capacity, power_fraction,hx_source_supply_temperature, stream['supply_temperature'])
                                info = join_hx_and_technology([info_hx_grid.data_teo,info_pump_grid.data_teo,info_technology.data_teo],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                info['hourly_supply_capacity_normalize'] = info_technology.data_teo['hourly_supply_capacity_normalize']  # add solar thermal profile
                                conversion_technologies.append(info)

                                # add heat pump
                                info_technology = Add_Heat_Pump(country, consumer_type,needed_supply_capacity, power_fraction, hx_source_supply_temperature, stream['supply_temperature'])
                                info = join_hx_and_technology([info_hx_grid.data_teo,info_pump_grid.data_teo,info_technology.data_teo],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                conversion_technologies.append(info)

                                # add chp
                                info_technology = Add_CHP(country, consumer_type,needed_supply_capacity, power_fraction, hx_source_supply_temperature, stream['supply_temperature'])
                                info = join_hx_and_technology([info_hx_grid.data_teo,info_pump_grid.data_teo,info_technology.data_teo],power_fraction,stream_available_capacity,info_pump_grid.supply_capacity,'source')
                                conversion_technologies.append(info)



                            output_converted.append({
                                            'stream_id': stream['stream_id'],
                                            'hourly_stream_capacity': hourly_stream_capacity,  # [kWh]
                                            'conversion_technologies': conversion_technologies,  # [€/kW]
                                        })

            output.append({
                'source_id':source['id'],
                'source_grid_supply_temperature':source_grid_supply_temperature,
                'source_grid_return_temperature':source_grid_return_temperature,
                'streams_converted':output_converted
                })


    #output = json.dumps(output, indent=2)

    return output


class VAR():
    def __init__(self):
        self.a = 1
        self.grid_losses =[]
        self.last_iteration_data =[]
        self.sink_group_grid_supply_temperature = 85
        self.sink_group_grid_return_temperature = 55


invar = VAR()


stream_1 = {'stream_id':1,
            'object_type':'stream',
            'stream_type':'excess_heat',
            'fluid':'flue_gas',
            'capacity':434,
            'supply_temperature': 220,
            'target_temperature':120,
            'hourly_generation':[1000,1000,1000]}


invar.group_of_sources = [ {'id':1,
                            'consumer_type': 'non-household',
                             'location':[10,10],
                             'streams':[stream_1]
                                }]

out = convert_sources(invar)
print(out)

invar.last_iteration_data = out
invar.grid_losses = [[200],[150]]
new_out = convert_sources(invar)
