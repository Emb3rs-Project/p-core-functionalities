User Guide - STANDALONE
==========================================================

The CF can also be used as STANDALONE. It were developed scripts with the main features of the CF that read data from
excel files and provide routines the results to the user. You can check below to understand how it works.

**After cloning the CF repository, check the folder "standalone"-> "test.py". Running the standalone is as simple as this:**

.. code-block:: python

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
    convert_sinks_results, convert_sources_results = cf.dhn_simulation(dhn_file_path,
                                                                       grid_supply_temperature=80,
                                                                       grid_return_temperature=40)
    orc_data, orc_report = cf.design_orc(design_orc_file_path)
    pinch_data, pinch_report = cf.pinch_analysis(pinch_analysis_file_path)



For each one of the simulations you can find an example for the `INPUTS <https://github.com/Emb3rs-Project/p-core-functionalities/tree/master/standalone/test_files>`_ data
and `RESULTS <https://github.com/Emb3rs-Project/p-core-functionalities/tree/master/standalone/test_files/results>`_  in
the "standalone" folder. Below, you can find a step-by-step for each simulation.

District Heating Network
--------------------------------------------
INPUTS -> user provides excel file
    1. Sources characterization - Simple Characterization
    2. Sinks characterization - Simple Characterization, Building and Greenhouse
    3. Fuels data
RUN CODE
    4. Sinks Simulation - Convert Sinks
    5. Sources Simulation - Convert Sources
OUTPUT -> user can fetch the data
    6. User can get the outputs of the simulations (Convert Sources and Convert Sinks)

Pinch Analysis - Isolated Streams (QUICK INPUTS)
--------------------------------------------
INPUTS -> user provides excel file
    1. Source and streams characterization
    2. Pinch analysis data
    3. Fuels data
RUN CODE
    4. Source simulation - Pinch Analysis - QUICK INPUTS -> get best pinch designs
OUTPUT -> user can fetch the data
    5. User can get the outputs of the simulation and the HTML report


Design ORC
--------------------------------------------
INPUTS -> user provides excel file
    1. Source and streams characterization
    2. ORC design data
    3. Fuels data
RUN CODE
    4. Source simulation - Organic Rankine Cycle (ORC) -> get best ORC designs
OUTPUT -> user can fetch the data
    5. User can get the outputs of the simulation and the HTML report

