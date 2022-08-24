from module.standalone.mappings.mapping_convert_sinks import mapping_convert_sinks
from module.standalone.mappings.mapping_convert_sources import mapping_convert_sources
from module.standalone.mappings.mapping_building import mapping_building
from module.standalone.mappings.mapping_greenhouse import mapping_greenhouse
from module.standalone.mappings.mapping_simple_user import mapping_simple_user
from module.src.General.Simple_User.simple_user import simple_user
from module.src.Source.simulation.Convert.convert_sources import convert_sources
from module.src.Source.simulation.Heat_Recovery.ORC.convert_orc import convert_orc
from module.src.Source.simulation.Heat_Recovery.convert_pinch_isolated_streams import convert_pinch_isolated_streams
from module.src.Sink.simulation.convert_sinks import convert_sinks
from module.src.Sink.characterization.building import building
from module.src.Sink.characterization.greenhouse import greenhouse
from module.src.utilities.fuel_data_fill_values import fuel_data_fill_values
from module.src.utilities.kb import KB
from module.src.utilities.kb_data import kb
from module.standalone.read_data.read_data_cf_design_orc import ReadDataCFORC
from module.standalone.mappings.mapping_convert_orc import mapping_convert_orc
from module.standalone.read_data.read_data_cf_pinch import ReadDataCFPinch
from module.standalone.mappings.mapping_pinch_analysis import mapping_pinch_analysis
from module.standalone.read_data.read_data_cf_dhn import ReadDataCFDHN
import os
import pandas as pd

class DesignORC:

    def __init__(self):
        self.sources = []

    def read_user_inputs(self, file):
        df_file = pd.read_excel(file, sheet_name=None)
        cf_orc = ReadDataCFORC()
        self.cf_data = cf_orc.get_data(df_file)
        self.characterization()

    def characterization(self):

        # fuels_data
        self.fuels_data = fuel_data_fill_values(self.cf_data["sources"][0]['location'],
                                                self.cf_data["fuels_data"],
                                                KB(kb))

        # sources
        for _source_raw in self.cf_data["sources"]:
            _data = mapping_simple_user(_source_raw, "source")
            _char_streams = simple_user(_data)

            del _source_raw['raw_streams']
            _source_raw["streams"] = _char_streams["streams"]
            self.sources.append(_source_raw)

    def simulation(self):
        in_var = mapping_convert_orc(self.fuels_data, self.sources, self.cf_data["orc_data"])
        self.convert_orc_results = convert_orc(in_var, kb)

        return self.convert_orc_results

    def get_report(self):
        file = open("orc_report.html", "w")
        file.write(self.convert_orc_results["report"])
        file.close()

        return self.convert_orc_results["report"]

class PinchAnalysis:

    def read_user_inputs(self, file):
        df_file = pd.read_excel(file, sheet_name=None)
        cf_pinch = ReadDataCFPinch()
        self.cf_data = cf_pinch.get_data(df_file)

        # fuels_data
        self.cf_data["fuels_data"] = fuel_data_fill_values(self.cf_data["sources"][0]['location'],
                                                           self.cf_data["fuels_data"],
                                                           KB(kb))

    def simulation(self):
        in_var = mapping_pinch_analysis(self.cf_data)
        self.pinch_data = convert_pinch_isolated_streams(in_var, KB(kb))

        return self.pinch_data

    def get_report(self):
        file = open("pinch_report.html", "w")
        file.write(self.pinch_data["report"])
        file.close()

        return self.pinch_data["report"]


class DHNSimulation:

    def __init__(self):
        self.sources = []
        self.sinks = []

    def read_user_inputs(self, file):
        df_file = pd.read_excel(file, sheet_name=None)
        cf_dhn = ReadDataCFDHN()
        cf_data_raw = cf_dhn.get_data(df_file)
        self.cf_characterization(cf_data_raw)

    def cf_characterization(self, cf_data_raw):
        print("CF Characterization STARTED!")

        # fuels_data
        self.fuels_data = fuel_data_fill_values(cf_data_raw["sources"][0]['location'],
                                                cf_data_raw["fuels_data"],
                                                KB(kb))

        # sources
        for _source_raw in cf_data_raw["sources"]:
            _data = mapping_simple_user(_source_raw, "source")
            _char_streams = simple_user(_data)

            del _source_raw['raw_streams']
            _source_raw["streams"] = _char_streams["streams"]
            _source_raw["fuels_data"] = self.fuels_data
            self.sources.append(_source_raw)


        # sinks
        for sink_type in cf_data_raw["sinks"]:
            for _sink_raw in cf_data_raw["sinks"][str(sink_type)]:
                if sink_type == "building":
                    _data = mapping_building(_sink_raw)
                    _char_streams = building(_data, KB(kb))
                    _sink_raw["name"] = _sink_raw["name"]
                    del _sink_raw['info']

                elif sink_type == "greenhouse":
                    _data = mapping_greenhouse(_sink_raw)
                    _char_streams = greenhouse(_data)
                    _sink_raw["name"] = _sink_raw["info"]["name"]
                    del _sink_raw['info']

                elif sink_type == "simple_sink":
                    _data = mapping_simple_user(_sink_raw, "sink")
                    _char_streams = simple_user(_data)
                    del _sink_raw['raw_streams']

                else:
                    raise Exception("Sink type not valid")

                _sink_raw["streams"] = _char_streams["streams"]
                _sink_raw["fuels_data"] = self.fuels_data

                self.sinks.append(_sink_raw)

        print("CF Characterization COMPLETED!")

    def simulation(self, grid_supply_temperature, grid_return_temperature):
        convert_sinks_input = mapping_convert_sinks(self.sinks, grid_supply_temperature, grid_return_temperature)
        convert_sinks_data = convert_sinks(convert_sinks_input, KB(kb))

        convert_sources_input = mapping_convert_sources(self.sources)
        convert_sources_results = convert_sources(convert_sources_input, KB(kb))

        return convert_sinks_data, convert_sources_results


class CFModule():
    '''
    Run  main features of CF:
        - District Heating Network computations
        - Organic Rankine Cycle design
        - Pinch Analysis and heat exchangers design

    '''

    def design_orc(self, file_path):
        file = os.path.abspath(file_path)
        platform_orc = DesignORC()
        platform_orc.read_user_inputs(file)
        orc_data = platform_orc.simulation()
        report = platform_orc.get_report()

        return orc_data, report

    def dhn_simulation(self, file_path, grid_supply_temperature, grid_return_temperature):
        file = os.path.abspath(file_path)
        platform_dhn = DHNSimulation()
        platform_dhn.read_user_inputs(file)
        convert_sinks_results, convert_sources_results = platform_dhn.simulation(grid_supply_temperature, grid_return_temperature)

        return convert_sinks_results, convert_sources_results

    def pinch_analysis(self,file_path):

        file = os.path.abspath(file_path)
        platform_pinch_analysis = PinchAnalysis()
        platform_pinch_analysis.read_user_inputs(file)
        pinch_data = platform_pinch_analysis.simulation()
        report = platform_pinch_analysis.get_report()

        return pinch_data, report
