The Core Functionalities module will allow a full characterization of the main objects of the EMB3Rs platform and prepare the data for the simulation process by the analysis modules.

For sources, the CF module is divided into 2 submodules: characterization and simulation.

The CF source characterization submodule receives input data from the user and generates streams for each source available (inflows, excess heat and supply heat). It has 6 main functions (outflow_simplified, generate_process, generate_boiler, generate_burner generate_cooling_equipment and generate_chp), and 5 auxiliary functions (schedule_hour; T_flue_gas; combustion_mass_flows; compute_flow_rate and stream). These are the main functionalities to analyse user data input for sources.

Detailed information for the source characterization can be found here:

https://gitlab.pdmfc.com/emb3rs1/prototypes/cf/module_code/-/blob/master/Source/characterization/readme.md

Whenever a user performs a simulation on the platform, the CF source simulation submodule will retrieve the required data from the platform and calculate the end use. The submodule has 2 main functions (convert_sources and generate_heat_recovery), and 17 auxiliary functions. 

Detailed information for the source simulation can be found here:
https://gitlab.pdmfc.com/emb3rs1/prototypes/cf/module_code/-/blob/master/Source/simulation/readme.md



For sinks, the CF module is also divided into 2 submodules, charaterization and simulation.

To characterize sinks, the CF has 3 main functions and 16 auxiliary functions. There is the industry function for simplified users that wish to manually add a heat/cold demand.
The building and greenhouse functions is for users that intend to add a climate dependent heating/cooling demand. The functions will then generate an hourly heating/cooling demand profile for a full year based on climate data and indoor temperature requirements.

Detailed information for the sink characterization can be found here:
https://gitlab.pdmfc.com/emb3rs1/prototypes/cf/module_code/-/blob/master/Sink/characterization/readme.md

On the simulation subgroup, there is 1 main function (convert_sinks),

Detailed information for the sink simulation can be found here:
https://gitlab.pdmfc.com/emb3rs1/prototypes/cf/module_code/-/blob/master/Sink/simulation/readme.md
