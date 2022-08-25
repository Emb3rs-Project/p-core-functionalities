Sink Submodule
===================
The CF sink submodule is divided into: characterization and simulation.

The **characterization** is responsible for receiving the input data from the user and estimate the sink
heating and cooling needs. The characterization is divided into simple and detailed. For the simple characterization the industry user needs to characterize the hot water, steam and/or cold water streams. A user that performs the detailed characterization can analyze a building heat and cooling needs by introducing the building characteristics.

    *Simple*: The user directly introduces the streams, its properties and schedule

    *Building/Greenhouse*: The building and greenhouse routines are for users that intend to simulate a climate dependent heating/cooling demand. The functions will generate a quick estimate on the hourly heating/cooling (if existent) demand profile for a full year based on climate data and buildings’ temperature requirements

The **simulation** aims to evaluate and design the technologies needed to convert the DHN heat into the sinks needs

    *CONVERT DHN*: It aims to design and estimate the costs of converting the District Heating Network heat to the demand of the sink's streams.

.. figure::  figures/Sinks_diagram.png
   :align:   center

|

.. toctree::
   :maxdepth: 2
   :caption: Submodules:

   SinkCharacterization
   SinkSimulation


