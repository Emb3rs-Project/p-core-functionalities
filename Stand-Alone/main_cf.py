from mappings.cf.mapping_convert_sinks import mapping_convert_sinks
from mappings.cf.mapping_convert_sources import mapping_convert_sources
from mappings.cf.mapping_building import mapping_building
from mappings.cf.mapping_greenhouse import mapping_greenhouse
from mappings.cf.mapping_simple_user import mapping_simple_user

from module.src.General.Simple_User.simple_user import simple_user
from module.src.Source.simulation.Convert.convert_sources import convert_sources
from module.src.Sink.simulation.convert_sinks import convert_sinks
from module.src.Sink.characterization.building import building
from module.src.Sink.characterization.greenhouse import greenhouse
from module.src.utilities.fuel_data_fill_values import fuel_data_fill_values
from read_user_inputs.main_read_user_inputs import main_read_user_inputs

from module.src.utilities.kb import KB
from src_modules.modules.CF.src.utilities.kb_data import kb


class CF():

    def design_orc(self,file):
        designorc = self.DesignORC
        designorc.read_user_inputs(file)
        simulation_data = designorc.simulation()

        # create file in json

        # create HTML report


    def dhn_simulation(self, ):
        dhn = self.DHNSimulation()
        dhn.read_user_inputs()
        convert_sinks_data, convert_sources_data = dhn.simulation()

        # create file in json
        # jdons.dump


    def pinch_analysis(self,file):
        pinch = self.PinchAnalysis()
        pinch.read_user_inputs(file)
        simulation_data = pinch.simulation()

        # create file in json

        # create HTML report




    class DesignORC:

        def read_user_inputs(self):

        def characterization(self):

        def simulation(self):


    class PinchAnalysis:

        def read_user_inputs(self,file):
            self.streams_data_raw = read_pinch_user_inputs(file)


        def simulation(self):

            pinch_data = convert_pinch_isolated_streams(self.streams_data_raw)

            return pinch_data



    class DHNSimulation:

        def __init__(self):
            self.sources = []
            self.sinks = []

        def read_user_inputs(self,file):

            cf_data_raw = read_dhn_user_inputs(file)
            # self.gis_data, self.teo_data, self.mm_data, self.bm_data

            self.cf_characterization(cf_data_raw)

        def characterization(self,cf_data_raw):

            print("Characterization started!")

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
                        del _sink_raw['info']

                    elif sink_type == "greenhouse":
                        _data = mapping_greenhouse(_sink_raw)
                        _char_streams = greenhouse(_data)
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

            print("Characterization completed!")

        def simulation(self):
            convert_sinks_input = mapping_convert_sinks(self.sinks)
            convert_sinks_data = convert_sinks(convert_sinks_input, KB(kb))

            convert_sources_input = mapping_convert_sources(self.sources)
            convert_sources_data = convert_sources(convert_sources_input, KB(kb))

            return convert_sinks_data, convert_sources_data

