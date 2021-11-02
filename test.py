from Tests.test_lib import defineArguments, processInput
from Tests.Sinks.characterization.Industry import testIndustry
from Tests.Sinks.characterization.Building import testBuilding

# Write Here all the available tests you want to run
availableTests = {
    "sink:industry": testIndustry,
    "sink:building" : testBuilding
}

# DO NOT CHANGE FROM THIS POINT BELOW
# UNLESS YOU KNOW WHAT YOUR DOING
args = defineArguments(availableTests)

processInput(args, availableTests)
