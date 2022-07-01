from module.Tests.Sinks.characterization.SinkSimpleUser import testSinkSimpleUser
from module.Tests.Sinks.characterization.Building import testBuilding
from module.Tests.Sinks.characterization.Greenhouse import testGreenhouse
from module.Tests.Sinks.characterization.BuildingAdjustCapacity import testBuildingAdjustCapacity
from module.Tests.Sinks.simulation.ConvertSink import testConvertSink
testBuildingAdjustCapacity()
testSinkSimpleUser()
testBuilding()
testGreenhouse()
testConvertSink()

from module.Tests.Sources.characterization.SourceDetailed import testSourceDetailedUser
from module.Tests.Sources.characterization.SourceSimpleUser import testSourceSimpleUser
from module.Tests.Sources.simulation.ConvertSources import testConvertSource
from module.Tests.Sources.simulation.ConvertOrc import testConvertORC
from module.Tests.Sources.simulation.ConvertPinch import testConvertPinch
testSourceDetailedUser()
testSourceSimpleUser()
testConvertSource()
testConvertORC()
testConvertPinch()

from module.Tests.Sources.simulation.ConvertPinchIsolated import testConvertPinchIsolated
testConvertPinchIsolated()

#from module.Tests.Sources.characterization.SUAdjustCapacity import testSUAdjustCapacity
#
#testSUAdjustCapacity()
#
