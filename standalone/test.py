from main_cf_standalone import CFModule

# Initialize
cf = CFModule()

# Get files path
dhn_file_path = 'test_files/dhn_data.xlsx'
design_orc_file_path = 'test_files/orc_data.xlsx'
pinch_analysis_file_path = 'test_files/pinch_data.xlsx'

# Run
convert_sinks_results, convert_sources_results = cf.dhn_simulation(dhn_file_path,
                                                                   grid_supply_temperature=80,  # change this
                                                                   grid_return_temperature=40)
orc_data, orc_report = cf.design_orc(design_orc_file_path)
pinch_data, pinch_report = cf.pinch_analysis(pinch_analysis_file_path)