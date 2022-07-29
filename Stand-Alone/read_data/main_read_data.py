import pandas as pd
from .read_data_cf import ReadDataCF
from .read_data_gis import ReadDataGIS
from .read_data_teo import ReadDataTEO
import copy



def main_read_data(file):

    # NOTE: WE NEED EXCEL ERROR HANDLING!

    df_file = pd.read_excel(file, sheet_name=None)


    keys = ['CF - Fuels Data',
            'CF - Sources General Data',
            "CF - Simple Sources' Streams",
            'CF - Grid Connection Point',
            'CF - Sinks General Data',
            "CF - Simple Sinks' Streams",
            'CF - Sinks Buildings',
            'CF - Sinks Greenhouse',
            'GIS',
            'MARKET',
            'TEO',
            'BM']

    cf_inputs_reader = ReadDataCF()
    cf_data = cf_inputs_reader.get_data(copy.deepcopy(df_file))

    gis_inputs_reader = ReadDataGIS()
    gis_data = gis_inputs_reader.get_data(copy.deepcopy(df_file))

    teo_inputs_reader = ReadDataTEO()
    teo_data = teo_inputs_reader.get_data(copy.deepcopy(df_file))

    #bm_data = read_data_bm(df_file)
    #mm_data = read_data_mm(df_file)

    return cf_data, gis_data #,teo_data,mm_data,bm_data