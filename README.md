# EMB3RS Core functionalities (CF) module

## Introduction
The purpose of the Core Functionalities (CF) module is to allow full characterization of the EMB3Rs platform objects (sinks and sources) and provide technical information to all the analysis modules, namely the graphical information systems (GIS) module, the techno-economic (TEO) module, the market module (MM), and the business module (BM); to run their simulations.   

The CF module divides both sinks and sources submodules into two main sections: characterization and simulation. The characterization focuses on receiving the user inputs and performing the needed computations to characterize the created objects, e.g., when the user creates a sink object, namely a greenhouse, the CF will compute its yearly heating needs according to its location, greenhouse dimensions, and other input parameters. The simulation focuses on performing analysis based on the characterization information, e.g. for a source’s excess heat streams (which were computed in the characterization), the conversion simulation will evaluate the available amount of energy that can be provided to a district heating network (DHN).

The main CF submodules, and respective items, are: 

Source: 
- Industry’s equipment, processes, and streams characterization (characterization) 
- Excess heat characterization (characterization) 
- Internal heat recovery analysis (simulation) 

Conversion of the source’s excess heat streams to the DHN and evaluation of the technologies to be implemented (simulation) 

Sink: 
- Industry and buildings – greenhouse, hotel, residential, office - heating/cooling demand and streams characterization (characterization) 
- Conversion of the DHN to the sink needs and evaluation of the technologies to be implemented (simulation) 

Looking into more detail at the main platform objects. 

When a user creates a source, there are two methods to perform its characterization. A simple form if the user desires to characterize directly specific excess heat streams and a more detailed form for users who intend an industry complete characterization. These need to introduce in detail their equipment and processes data. In terms of simulation, whether simplified or detailed characterization, the CF module will convert the source´s excess heat to the DHN, estimating the available conversion heat and the technologies that could be implemented. Only for the users who performed the detailed characterization is performed the internal heat recovery analysis – based on a pinch analysis-, in which the CF suggests possible heat exchanger design combinations. 

Detailed information for the source characterization can be found here (https://gitlab.pdmfc.com/emb3rs1/prototypes/cf/module_code/-/blob/master/Source/characterization/readme.md)

Detailed information for the source simulation can be found here (https://gitlab.pdmfc.com/emb3rs1/prototypes/cf/module_code/-/blob/master/Source/simulation/readme.md)

When a user creates a sink, it is prompted to the user to characterize its heating/cooling demand. Similar to the source, there is a simplified form for the user to input directly a specific heat/cold stream demand, and a more detailed form for the users who which to characterize buildings – residential, offices, hotels, and greenhouses. According to the user's buildings specification, the CF will characterize the building by generating the heating/cooling demand. Simulation-wise, the CF will evaluate the technologies that could be implemented on the DHN to meet the heat/cold sink´s needs. 

Detailed information for the sink characterization can be found here:
https://gitlab.pdmfc.com/emb3rs1/prototypes/cf/module_code/-/blob/master/Sink/characterization/readme.md

Detailed information for the sink simulation can be found here:
https://gitlab.pdmfc.com/emb3rs1/prototypes/cf/module_code/-/blob/master/Sink/simulation/readme.md
