# EMB3RS Core functionalities (CF) module

## Introduction
The purpose of the Core Functionalities (CF) module is to allow full characterization of the EMB3Rs platform objects (sinks and sources) and provide technical information to all the analysis modules, namely the graphical information systems (GIS) module, the techno-economic (TEO) module, the market module (MM), and the business module (BM); to run their simulations.   

The CF module divides both sinks and sources submodules into two main sections: characterization and simulation. The characterization focuses on receiving the user inputs and performing the needed computations to characterize the created objects, e.g., when the user creates a sink object, namely a greenhouse, the CF will compute its yearly heating needs according to its location, greenhouse dimensions, and other input parameters. The simulation focuses on performing analysis based on the characterization information, e.g. for a source’s excess heat streams (which were computed in the characterization), the conversion simulation will evaluate the available amount of energy that can be provided to a district heating network (DHN).

## The CF Module

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


## Requirements
A python version of 3.7.7 or higher is required to run the module
- Import os (most recent version) - The OS module in Python provides functions for interacting with the operating system
- Import datetime as dt (most recent version) - Used to display current date and time
- Import logging (most recent version)  - Used for writing status messages to a file or any other output streams.
- Import numpy as np (version  1.16.4 or higher) - used for working with arrays and functions for working in domain of linear algebra, fourier transform, and matrices
- Import pandas as pd version  (0.25.1 or higher) - Pandas will be used to read the in-puts from an excel file and write outputs into an excel/csv file

## Emb3rs project

EMB3Rs (“User-driven Energy-Matching & Business Prospection Tool for Industrial Excess Heat/Cold Reduction, Recovery and Redistribution) is a European project funded under the H2020 Program (Grant Agreement N°847121) to develop an open-sourced tool to match potential sources of excess thermal energy with compatible users of heat and cold.

Users, like industries and other sources that produce excess heat, will provide the essential parameters, such as their location and the available excess thermal energy. The EMB3Rs platform will then autonomously and intuitively assess the feasibility of new business scenarios and identify the technical solutions to match these sources with compatible sinks. End users such as building managers, energy communities or individual consumers will be able to determine the costs and benefits of industrial excess heat and cold utilization routes and define the requirements for implementing the most promising solutions. 

The EMB3Rs platform will integrate several analysis modules that will allow a full exploration of the feasible technical routes to the recovery and use of the available excess thermal energy. 

## Acknowledgments

The EMB3RS project has received funding from the European Union’s Horizon 2020 research and innovation program under grant agreement No 847121. This publication reflects only the views of its authors, and the European Commission cannot be held responsible for its content.

## Licenses

•	All the code developed is licensed under a Creative Commons At-tribution 4.0 International License. Further modifications, and larger works may be distributed under different terms and without source code.

## References

[1]	H. M. S. Office, The future of heating: A strategic framework for low carbon heat in the uk, Tech. rep., Department of Energy and Climate Change at https://www.gov.uk/government/publications/the-future-of-heating-a-strategic-framework-for-low-carbon-heat (2012);

[2]	J. N. Chiu, J. Castro Flores, V. Martin, B. Lacarriere, Industrial surplus heat transportation for use in district heating, Energydoi:10.1016/j.energy.2016.05.003

[3]	I. C. Kemp, Pinch analysis and Process Integration, 2nd editio. Butterworth-Heinemann, 2006.

[4]	E. Bavoux, “Python Eurostat API,” 2021. https://pypi.org/project/eurostatapiclient/

[5]	R. Zhar, A. Allouhi, and A. Jamil, “A comparative study and sensitivity analysis of different ORC configurations for waste heat recovery,” Case Studies in Thermal Engineering, vol. 28, p. 101608, Dec. 2021.

[6]	D. Sartori et al., “Guide to Cost-benefit Analysis of Investment Projects Economic appraisal tool for Cohesion Policy 2014-2020,” Brussels, 2014.

[7]	S. Quoilin, M. van den Broek, S. Declaye, P. Dewallef, and V. Lemort, “Techno-economic survey of Organic Rankine Cycle (ORC) systems,” Renewable and Sustainable Energy Reviews, vol. 22, pp. 168–186, Jun. 2013, doi: 10.1016/J.RSER.2013.01.028.

[8]	BitzerGroup, “ElectraTherm organic rankine cycle systems technical brochure.” Bitzer Group, 2020.

[9]	G. P. Hammond and J. B. Norman, “Heat recovery opportunities in UK industry,” Applied Energy, vol. 116, pp. 387–397, 2014, doi: 10.1016/j.apenergy.2013.11.008.

[10]	M. Imran, M. Usman, B.-S. Park, H.-J. Kim, and D.-H. Lee, “Multi-objective optimization of evaporator of organic Rankine cycle (ORC) for low temperature geothermal heat source,” Applied Thermal Engineering, vol. 80, pp. 1–9, Apr. 2015, doi: 10.1016/j.applthermaleng.2015.01.034.

[11]	DGEG, “Direcção Geral de Energia e Geologia - Tarifas de referência de Instalações de Cogeração,” 2021. https://www.dgeg.gov.pt/media/pspn4mgv/desp_17_2021.pdf (accessed Jan. 10, 2022).

[12]	A. A. V. Ochoa, J. C. C. Dutra, J. R. G. Henríquez, and C. A. C. dos Santos, “Dynamic study of a single effect absorption chiller using the pair LiBr/H2O,” Energy Conversion and Management, vol. 108, pp. 30–42, Jan. 2016, doi: 10.1016/J.ENCONMAN.2015.11.009.

[13]	Z. Guo-Yan, W. En, and T. Shang-Tung, “Techno-economic study on compact heat exchangers,” International Journal of Energy Research, vol. 32, no. 12, Oct. 2008.

[14]	W. Wagner, VDI Heat Atlas, vol. 2010. Springer Berlin Heidelberg, 2010. doi: 10.1007/978-3-540-77877-6.

[15]	G. Towler and R. Sinnot, Chemical Engineering Design; Principles, Practice and Economics of Plant and Process Design. Elsevier, 2008.

[16]	Ekocoil, “Ekocoil economizers technical datasheet.” Ekocoil, Finnland. [Online]. Available: http://www.ekocoil.fi/

[17]	H. Kauko, D. Rohde, B. R. Knudsen, and T. Sund-Olsen, “Potential of thermal energy storage for a district heating system utilizing industrial waste heat,” Energies, vol. 13, no. 15, 2020, doi: 10.3390/en13153923.

[18]	Grundfos, “Grundfos product center,” 2018. product-selection.grundfos.com

[19]	Thermax, “Thermax absorption chillers budgetary price quotations 2020.” Thermax global, 2020. [Online]. Available: https://www.thermaxglobal.com/

[20]	F. Gamborg and C. Wolter, “Technology Data for Generation of Electricity and District Heating.” Danish Energy Agency, Esbjerg, 2020. Available: https://ens.dk/en/our-services/projections-and-models/technology-data/technology-data-generation-electricity-and

[21]	EuropeanEnvironmentAgency, “Greenhouse gas emission intensity of electricity generation,” 2020. www.eea.europa.eu

[22]	GlobalPetrolPrices, “Diesel prices around the world.” 2021. [Online]. Available: www.globalpetrolprices.com/diesel_prices

[23]	Richi, “How Much Does 1 Ton Of Wood Pellets Cost.” [Online]. Available: https://www.cn-pellet.com/faq/how-much-does-1-ton-of-wood-pellets-cost.html

[24]	Hoval, “Hoval industrial boilers”, [Online]. Available: https://www.hovalpartners.com/products-solutions/solutions/industrial-boiler-solutions

[25]	Bosch, “Bosch industrial hot water boilers 2019 catalogue,” 2020, p. 234. [Online]. Available: www.bosch-industrial.com

[26]	European Commission, “Energy Sources, Production Costs and Performance of Technologies for Power Generation, Heating and Transport,” 2008.

[27]	FENAGY, “FENAGY H600 CO2 heat pumps (https://r744.com/product/fenagy-heat-pump-h600/),” 2022. https://r744.com/product/fenagy-heat-pump-h600/ (accessed Jan. 14, 2022).
