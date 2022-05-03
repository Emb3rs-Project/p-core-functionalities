from .Tests.test_lib import defineArguments, processInput
from .Tests.Sinks.characterization.SinkSimpleUser import testSinkSimpleUser
from .Tests.Sinks.characterization.Building import testBuilding
from .Tests.Sinks.characterization.Greenhouse import testGreenhouse
from .Tests.Sinks.simulation.ConvertSink import testConvertSink
from .Tests.Sources.characterization.SourceSimpleUser import testSourceSimpleUser
from .Tests.Sources.simulation.ConvertSources import testConvertSource
from .Tests.Sources.simulation.ConvertOrc import testConvertORC
from .Tests.Sources.simulation.ConvertPinch import testConvertPinch
from .Tests.Sources.characterization.SourceDetailed import testSourceDetailedUser


# Write Here all the available tests you want to run
availableTests = {
    "sink:simple_user": testSinkSimpleUser,
    "sink:building": testBuilding,
    "sink:greenhouse": testGreenhouse,
    "sink:convert_sinks": testConvertSink,
    "source:source_detailed": testSourceDetailedUser,
    "source:simple_user": testSourceSimpleUser,
    "source:convert_sources": testConvertSource,
    "source:convert_orc": testConvertORC,
    "source:convert_pinch": testConvertPinch,
}


def init():
    # DO NOT CHANGE FROM THIS POINT BELOW
    # UNLESS YOU KNOW WHAT YOUR DOING
    args = defineArguments(availableTests)

    processInput(args, availableTests)
