import pandas as pd
import numpy as np

class ReadDataCF:

    def get_data(self, df_file_excel):

        for sheet in df_file_excel.keys():
            df_file_excel[sheet] = self.clean_df(df_file_excel[sheet])
            df_file_excel[sheet] = df_file_excel[sheet].replace({np.nan:None})

        fuels_data = self.get_fuels_data(df_file_excel["CF - Fuels Data"])
        simple_sources_data = self.get_simple_sources_data(df_file_excel["CF - Sources General Data"],df_file_excel["CF - Simple Sources' Streams"])
        simple_sinks_data = self.get_simple_sinks_data(df_file_excel["CF - Sinks General Data"],df_file_excel["CF - Simple Sinks' Streams"] )

        building_data = self.get_building_data(df_file_excel["CF - Sinks General Data"], df_file_excel["CF - Sinks Buildings"])
        greenhouse_data = self.get_greenhouse_data(df_file_excel["CF - Sinks General Data"], df_file_excel["CF - Sinks Greenhouse"])

        cf_data = {}
        cf_data['fuels_data'] = fuels_data
        cf_data['sources'] = simple_sources_data
        cf_data['sinks'] = {
                            "building": building_data,
                            "greenhouse": greenhouse_data,
                            "simple_sink": simple_sinks_data
                            }

        return cf_data


    def get_fuels_data(self, df_sheet):
        df_sheet = df_sheet.set_index('fuel')
        df_sheet.index.name = None
        df_sheet = df_sheet.transpose()

        return df_sheet.to_dict()


    def get_simple_sources_data(self, df_sources_general_data, df_sources_streams):

        sources_data = []

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
            data = df_data.transpose().to_dict()

            for key in data.keys():
                data[key] = {key_stream: self.get_parameters_values(key_stream, value_stream) for (key_stream, value_stream) in data[key].items() if value_stream != None}

            general_data[source_id]["raw_streams"] = [data[key] for key in data] # convert to list
            sources_data.append(general_data[source_id])


        return sources_data


    def get_simple_sinks_data(self, df_sinks_general_data, df_sinks_streams):

        sinks_data = []

        # get  general data
        df_sinks_general_data['sink_id'] = df_sinks_general_data['sink_id'].apply(int)
        df_sinks_streams['sink_id'] = df_sinks_streams['sink_id'].apply(int)

        df_sinks_general_data["id"] = df_sinks_general_data['sink_id'].copy()
        df_sinks_general_data = df_sinks_general_data.set_index('sink_id')

        # get simple sinks general data
        df_simple_sinks = df_sinks_general_data.loc[df_sinks_general_data['sink_type'] == "simple sink"]
        df_simple_sinks = df_simple_sinks.drop('sink_type', axis=1)
        df_simple_sinks['location'] = df_simple_sinks.apply(lambda row: [row['latitude'], row['longitude']], axis=1)
        df_simple_sinks = df_simple_sinks.drop(['latitude','longitude'], axis=1)
        df_simple_sinks = df_simple_sinks.transpose()

        # create dict with keys=sink_id, followed by source data
        general_data = df_simple_sinks.to_dict()

        # put streams on the respective sink
        for sink_id in general_data.keys():
            general_data[sink_id]["raw_streams"] = []
            df_data = df_sinks_streams[df_sinks_streams["sink_id"] == sink_id]
            df_data = df_data.drop('sink_id', axis=1)
            data = df_data.transpose().to_dict()

            for key in data.keys():
                data[key] = {key_stream: self.get_parameters_values(key_stream, value_stream) for (key_stream, value_stream) in data[key].items() if value_stream != None}


            general_data[sink_id]["raw_streams"] = [data[key] for key in data] # convert to list
            sinks_data.append(general_data[sink_id])

        return sinks_data


    def get_building_data(self, df_sinks_general_data, df_buildings):
        buildings_data = []

        if df_buildings.empty == False:
            # get  general data
            df_sinks_general_data['sink_id'] = df_sinks_general_data['sink_id'].apply(str)
            df_buildings['sink_id'] = df_buildings['sink_id'].apply(str)


            df_sinks_general_data["id"] = df_sinks_general_data['sink_id'].copy()
            df_sinks_general_data = df_sinks_general_data.set_index('sink_id')
            df_simple_sinks = df_sinks_general_data.loc[df_sinks_general_data['sink_type'] == "building"]
            if df_simple_sinks.shape[0] != df_buildings.shape[0]:
                raise Exception('Each building must have a unique Sink ID')

            df_simple_sinks = df_simple_sinks.drop('sink_type', axis=1)
            df_simple_sinks['location'] = df_simple_sinks.apply(lambda row: [row['latitude'], row['longitude']], axis=1)
            df_simple_sinks = df_simple_sinks.drop(['latitude','longitude'], axis=1)
            df_simple_sinks = df_simple_sinks.transpose()

            # create dict with keys=sink_id, followed by source data
            general_data = df_simple_sinks.to_dict()
            # put streams on the respective sink
            for sink_id in general_data.keys():
                general_data[sink_id]["info"] = []
                df_data = df_buildings[df_buildings["sink_id"] == sink_id]
                if df_data.shape[0] > 1:
                    raise Exception('Each building must have a unique Sink ID')

                df_data = df_data.drop('sink_id', axis=1)
                data = df_data.transpose().to_dict()

                for key in data.keys():
                    data[key] = {key_stream: self.get_parameters_values(key_stream, value_stream) for (key_stream, value_stream) in data[key].items() if value_stream != None}



                general_data[sink_id]["info"] = data[int(sink_id)]  # convert to list
                buildings_data.append(general_data[sink_id])

        return buildings_data


    def get_greenhouse_data(self,df_sinks_general_data, df_greenhouses):
        greenhouses_data = []

        if df_greenhouses.empty == False:
            # get  general data
            df_sinks_general_data['sink_id'] = df_sinks_general_data['sink_id'].apply(str)
            df_greenhouses['sink_id'] = df_greenhouses['sink_id'].apply(str)

            df_sinks_general_data["id"] = df_sinks_general_data['sink_id'].copy()
            df_sinks_general_data = df_sinks_general_data.set_index('sink_id')
            df_simple_sinks = df_sinks_general_data.loc[df_sinks_general_data['sink_type'] == "greenhouse"]
            df_simple_sinks = df_simple_sinks.drop('sink_type', axis=1)
            df_simple_sinks['location'] = df_simple_sinks.apply(lambda row: [row['latitude'], row['longitude']], axis=1)
            df_simple_sinks = df_simple_sinks.drop(['latitude','longitude'], axis=1)
            df_simple_sinks = df_simple_sinks.transpose()

            # create dict with keys=sink_id, followed by source data
            general_data = df_simple_sinks.to_dict()

            # put streams on the respective sink
            for sink_id in general_data.keys():
                general_data[sink_id]["info"] = []
                df_data = df_greenhouses[df_greenhouses["sink_id"] == sink_id]

                if df_data.empty == False:
                    if df_data.shape[0] > 1:
                        raise Exception('Each greenhouse must have a unique Sink ID')

                    df_data = df_data.drop('sink_id', axis=1)
                    data = df_data.transpose().to_dict()

                    for key in data.keys():
                        data[key] = {key_stream: self.get_parameters_values(key_stream, value_stream) for (key_stream, value_stream) in data[key].items() if value_stream != None}


                    general_data[sink_id]["info"] = data[int(sink_id)]  # convert to list
                    greenhouses_data.append(general_data[sink_id])
                else:
                    greenhouses_data = []

        return greenhouses_data

    def get_grid_connection_point_data(self,df_sinks_general_data, df_greenhouses):
        data = 1
        return data

    def clean_df(self,df_sheet):

        df_sheet.rename(columns=df_sheet.iloc[0], inplace=True)
        df_sheet = df_sheet.iloc[2:]

        return df_sheet


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

