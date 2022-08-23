import pandas as pd
import numpy as np
import ast

class ReadDataCFPinch:

    def get_data(self, df_file_excel):

        for sheet in df_file_excel.keys():
            df_file_excel[sheet] = self.clean_df(df_file_excel[sheet])
            df_file_excel[sheet] = df_file_excel[sheet].replace({np.nan:None})

        fuels_data = self.get_fuels_data(df_file_excel["CF - Fuels Data"])
        simple_sources_data = self.get_simple_sources_data(df_file_excel["CF - Sources General Data"],df_file_excel["CF - Simple Sources' Streams"])
        pinch_data = self.get_pinch_data(df_file_excel["CF - Pinch Data"])

        cf_data = {}
        cf_data['fuels_data'] = fuels_data
        cf_data['sources'] = simple_sources_data
        cf_data['pinch_data'] = pinch_data

        return cf_data

    def get_fuels_data(self, df_sheet):
        df_sheet = df_sheet.set_index('fuel')

        df_sheet["price"] = df_sheet["price"].apply(lambda x: x/1000 if x!=None else None)

        df_sheet.index.name = None
        df_sheet = df_sheet.transpose()
        df_sheet = df_sheet.where(pd.notnull(df_sheet), None)
        return df_sheet.to_dict()

    def get_simple_sources_data(self, df_sources_general_data, df_sources_streams):

        sources_data = []

        if df_sources_streams.empty == False:

            # get sources general data
            df_sources_general_data['source_id'] = df_sources_general_data['source_id'].apply(int)
            df_sources_streams['source_id'] = df_sources_streams['source_id'].apply(int)

            df_sources_general_data["id"] = df_sources_general_data['source_id'].copy()
            df_sources_general_data = df_sources_general_data.set_index('source_id')

            # create dict with keys=source_id, followed by source data
            df_sources_general_data['location'] = df_sources_general_data.apply(lambda row: [row['latitude'],row['longitude']], axis=1)
            df_sources_general_data = df_sources_general_data.drop(['latitude','longitude'], axis=1)
            df_sources_general_data = df_sources_general_data.transpose()

            general_data = df_sources_general_data.to_dict()

            # put streams on the respective source
            for source_id in general_data.keys():
                general_data[source_id]["raw_streams"] = []
                df_data = df_sources_streams[df_sources_streams["source_id"] == source_id]
                df_data = df_data.drop('source_id', axis=1)
                df_data.rename(columns={'stream_id': 'id'}, inplace=True)

                data = df_data.transpose().to_dict()

                for key in data.keys():
                    data[key] = {key_stream: self.get_parameters_values(key_stream, value_stream) for (key_stream, value_stream) in data[key].items() if value_stream != None}

                general_data[source_id]["raw_streams"] = [data[key] for key in data] # convert to list
                sources_data.append(general_data[source_id])

        return sources_data


    def get_pinch_data(self, df_data):

        df_data['streams_to_analyse'] = df_data['streams_to_analyse'].apply(lambda x: ast.literal_eval(str(x)))
        pinch_data = df_data.to_dict('records')

        return pinch_data[0]



    def get_parameters_values(self, key, val):
        import ast
        new_val = {
            "saturday_on": {"yes": 1, "no": 0},
            "sunday_on": {"yes": 1, "no": 0},
            "space_heating_type": {"Conventional": 1, "Low temperature": 2},
            "building_orientation": {
                                    "North": "N",
                                    "South": "S",
                                    "East": "E",
                                    "West": "W"},
        }

        if key == "real_hourly_capacity" or key == "real_monthly_capacity":
            val = ast.literal_eval(val)
            return val

        elif key in new_val:
            return new_val[key][val]
        else:
            return val

    def clean_df(self,df_sheet):

        df_sheet.rename(columns=df_sheet.iloc[0], inplace=True)
        df_sheet = df_sheet.iloc[2:]

        return df_sheet
