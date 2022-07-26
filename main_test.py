from module.Tests.Sinks.characterization.SinkSimpleUser import testSinkSimpleUser
from module.Tests.Sources.characterization.SourceSimpleUser import testSourceSimpleUser
testSinkSimpleUser()
testSourceSimpleUser()
from module.Tests.Sinks.characterization.Building import testBuilding
from module.Tests.Sinks.characterization.Greenhouse import testGreenhouse
testBuilding()
testGreenhouse()
from module.Tests.Sinks.simulation.ConvertSink import testConvertSink
testConvertSink()

from module.Tests.Sources.characterization.SourceDetailed import testSourceDetailedUser
from module.Tests.Sources.simulation.ConvertSources import testConvertSource
from module.Tests.Sources.simulation.ConvertOrc import testConvertORC
from module.Tests.Sources.simulation.ConvertPinch import testConvertPinch
testSourceDetailedUser()
testConvertSource()
testConvertORC()
testConvertPinch()
from module.Tests.Sources.simulation.ConvertPinchIsolated import testConvertPinchIsolated
testConvertPinchIsolated()

