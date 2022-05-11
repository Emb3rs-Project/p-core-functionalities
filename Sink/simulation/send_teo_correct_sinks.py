"""
alisboa/jmcunha


##############################
INFO: Gets convert_sink output and GIS data about the sinks to consider. Return convert_sink output updated, with the
sinks data for the TEO to analyze.


##############################
INPUT:
    all_info = {
        "all_sinks_info": all_sinks_info,
        "n_grid_specific": n_grid_specific,
        "n_demand_list": n_demand_list,
        "teo_demand_factor_group": teo_group_of_sinks_demand_factor
    }


##############################
OUTPUT:
    info_to_teo_analyze = {
        "all_sinks_info": all_sinks_info,
        "n_grid_specific": n_grid_specific,
        "n_demand_list": n_demand_list,
        "teo_demand_factor_group": teo_group_of_sinks_demand_factor
    }

"""

from ...Error_Handling.error_send_teo_correct_sinks import GISCorrectSinks
from ...Error_Handling.runtime_error import ModuleRuntimeException

def send_teo_correct_sinks(in_var):

    ####################################################
    # INPUT
    cf_convert_sinks_output = in_var['cf-module']['convert_sinks_output']
    gis_data = GISCorrectSinks(**in_var['gis-module'])
    gis_sink_info = gis_data.sinks

    ####################################################
    # COMPUTE
    if gis_sink_info is not None:
        #########################
        # all_sinks_info
        all_sinks_info = cf_convert_sinks_output["all_sinks_info"]
        all_sinks_id = [sink for sink in all_sinks_info['sinks']]

        # get sinks ID to analyze
        gis_sinks = [sink['sink_id'] for sink in gis_sink_info]

        # get sinks data to send TEO
        teo_sinks_to_analyze = [sink for sink in all_sinks_info['sinks'] if sink['id'] in gis_sinks]
        sinks_id_to_be_considered = [sink["id"] for sink in teo_sinks_to_analyze]

        if teo_sinks_to_analyze == []:
            raise ModuleRuntimeException(
                code="1",
                type="send_teo_correct_sinks.py",
                msg="GIS must provide None - 1st iteration - or at least one available sink ID to be analyzed - 2nd iteration onwards."
            )

        cf_convert_sinks_output["all_sinks_info"]["sinks"] = teo_sinks_to_analyze

        #################
        # teo_demand_factor_group
        sink_streams_id_not_to_be_analized = [sink_id['demand_fuel'] for sink_id in all_sinks_id if sink_id not in sinks_id_to_be_considered]
        for sink_stream_id in sink_streams_id_not_to_be_analized:
            for hour in cf_convert_sinks_output["teo_demand_factor_group"]:
                hour.pop(str(sink_stream_id))

        #################
        # n_demand_list
        gis_sinks_to_analyze = [sink for sink in all_sinks_info['n_demand_list'] if sink['id'] in gis_sinks]
        cf_convert_sinks_output["all_sinks_info"]["n_demand_list"] = gis_sinks_to_analyze


    ####################################################
    # OUTPUT
    info_to_teo_analyze = cf_convert_sinks_output

    return info_to_teo_analyze