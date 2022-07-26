User Guide
==========================================================

The CF module acts as an entry point of data for the whole platform. The CF performs the sources/sinks characterization
according to the user data, and is involved in the DHN simulation, as well as two Internal Heat Recovery simulations.

The characterization routines have always to be run prior to the simulations. From the characterization routines, it is obtained
the attribute "streams" (from any characterization), that should be sent to the simulations routines with the reamining
respective and necessary data. Below you can check, the steps that are performed by the CF according to the intended simulation.

|

**To ease the user works, and have all running as user friendly as possible, it were created the scripts in the "Stand Alone"
folder. You can check the Examples tab, to understand how it works.**

|

District Heating Network
--------------------------------------------
USER ACTION
    1. Sources characterization - Simple Characterization -> user provides csv file
    2. Sinks characterization - Simple Characterization, Building and Greenhouse  -> user provides csv file
AUTOMATED
    3. Sinks Simulation - Convert Sinks -> design Sinks to DHN connection technologies
    4. Sources Simulation - Convert Sources -> design Sources to DHN connection technologies
    5. Data provided to the remaining Modules are run (GIS, TEO, MM, BM)

*CF does not provide report to the user, only the other modules

Pinch Analysis - QUICK INPUTS
--------------------------------------------
USER ACTION
    1. Source characterization - Pinch Analysis - QUICK INPUTS -> user provides csv file
AUTOMATED
    2. Source simulation - Pinch Analysis - QUICK INPUTS -> get best pinch designs
    3. Get report

Design ORC
--------------------------------------------
USER ACTION
    1. Source characterization - Simple Characterization -> user provides csv file
AUTOMATED
    2. Source simulation - Organic Rankine Cycle (ORC) -> get best ORC designs
    3. Get report