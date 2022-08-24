from main_cf_standalone import CFModule

# Initialize
cf = CFModule()

# Get files path
dhn_file_path = 'test_files/dhn_data.xlsx'
design_orc_file_path = 'test_files/orc_data.xlsx'
pinch_analysis_file_path = 'test_files/pinch_data.xlsx'

# Run
convert_sinks_results, convert_sources_results = cf.dhn_simulation(dhn_file_path, grid_supply_temperature=80, grid_return_temperature=40)
cf.design_orc(design_orc_file_path)
cf.pinch_analysis(pinch_analysis_file_path)