from main_cf_standalone import CFModule
import json

# Initialize
cf = CFModule()

# Get files path
dhn_file_path = 'test_files/dhn_data.xlsx'
design_orc_file_path = 'test_files/orc_data.xlsx'
pinch_analysis_file_path = 'test_files/pinch_data.xlsx'

#############################
# Run DHN
convert_sinks_results, convert_sources_results = cf.dhn_simulation(dhn_file_path,
                                                                   grid_supply_temperature=80,  # change this
                                                                   grid_return_temperature=40)

# save data
with open("test_files/results/convert_sinks_results.json", "w") as outfile:
    json.dump(convert_sinks_results, outfile)

with open("test_files/results/convert_sources_results.json", "w") as outfile:
    json.dump(convert_sources_results, outfile)

#############################
# Run ORC
orc_data, orc_report = cf.design_orc(design_orc_file_path)

# save data
with open("test_files/results/orc_data.json", "w") as outfile:
    json.dump(orc_data, outfile)

file = open("test_files/results/orc_report.html", "w")
file.write(orc_report)
file.close()

#############################
# Run PINCH
pinch_data, pinch_report = cf.pinch_analysis(pinch_analysis_file_path)

# save data
file = open("test_files/results/pinch_report.html", "w")
file.write(pinch_report)
file.close()

with open("test_files/results/pinch_data.json", "w") as outfile:
    json.dump(pinch_data, outfile)
