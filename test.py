import os
import sys
import argparse

from .Tests.test_lib import defineArguments, processInput
from .Tests.Sinks.Industry import testIndustry
from .Tests.Sinks.characterization.Building import testBuilding
from .Tests.Sinks.characterization.Greenhouse import testGreenhouse
from .Tests.Sinks.simulation.ConvertSink import testConvertSink
from .Tests.Sources.characterization.GenerateBoiler import testGenerateBoiler
from .Tests.Sources.characterization.GenerateChp import testGenerateChp
from .Tests.Sources.characterization.OutflowSimplified import testOutflowSimplified
from Tests.Sources.characterization.GenerateCoolingEquipment import testGenerateCoolingEquipment
from Tests.Sources.characterization.GenerateBurner import testGenerateBurner
from Tests.Sources.characterization.Process import testProcess
from Tests.Sources.simulation.ConvertSources import testConvertSource
from Tests.Sources.simulation.ConvertOrc import testConvertORC
from Tests.Sources.simulation.ConvertPinch import testConvertPinch


# Write Here all the available tests you want to run
availableTests = {
    "sink:industry": testIndustry,
    "sink:building": testBuilding,
    "sink:greenhouse": testGreenhouse,
    "sink:convert_sinks": testConvertSink,
    "source_detailed:cooling_equipment":testGenerateCoolingEquipment,
    "source_detailed:burner":testGenerateBurner,
    "source_detailed:boiler": testGenerateBoiler,
    'source_detailed:chp': testGenerateChp,
    'source_detailed:process':testProcess,
    'source:outflow_simplified': testOutflowSimplified,
    'source:convert_sources':testConvertSource,
    'source:convert_orc':testConvertORC,
    'source:convert_pinch':testConvertPinch

    }

def init():
    # DO NOT CHANGE FROM THIS POINT BELOW
    # UNLESS YOU KNOW WHAT YOUR DOING
    args = defineArguments(availableTests)

    processInput(args, availableTests)
