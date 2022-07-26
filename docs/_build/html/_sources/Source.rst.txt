Source
=====================

The CF source submodule is divided into: characterization and simulation. The characterization is responsible for receiving the input data from the user, and, by performing several computations, to assess and estimate the available excess heat streams. The simulation aims to evaluate the recovery of the available excess heat internally, either by integrating it within the source's processes – pinch analysis - or by implementing an Organic Rankine Cycle (ORC); and externally, by converting it to the DHN.

.. figure::  figures/Source_diagram.png
   :align:   center

|

.. toctree::
   :maxdepth: 4
   :caption: Submodules:

   Source Characterization
   Source Simulation


