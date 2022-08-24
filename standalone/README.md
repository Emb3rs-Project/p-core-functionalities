Main features of the CF can be use with the CF Standalone.
By using excel files, as presented in the "test" folder, any user can easily use and obtain reports of the main features of the CF Module.

```python

from main_cf_standalone import CFModule

#############################################################################################
#############################################################################################
# USER INTERACTION -> Create a folder inside "test" folder with your input data

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

```
