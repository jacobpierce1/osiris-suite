Welcome to the Osiris Suite. The purpose of this repository is to implement classes facilitating data loading, management, and basic plotting for OSIRIS data. To see examples of what can be done, check out the ./examples folder. 

---------
Features 

The purpose of this repo is to implement a lightweight, flexible class for loading data output by and associated with OSIRIS. The most important class implemented is the OsirisDataContainer, which achieves this goal. Data may be loaded, unloaded, inspected, and manipulated without the user ever needed to refer to or keep track of the names of the files output by OSIRIS. 

In addition, there is an input-deck parser. Importantly, this allows the user to generate plots using parameters from a given input deck (for example, the total simulation time corresponding to a particular timestep) without having to hard-code these values into a script. 

The other important utility of the input-deck parser is that it can be used to dynamically modify an input deck and rewrite the file with the desired changes. This feature will be implemented in the near future and will probably make parameter scans significantly easier to run. 


---------
Features that are not implemented

As of July 2020, the following are not implemented, but will be eventually:
* storage of computations  
* parallel data-processing pipelines
* input deck write (the read works as expected)


---------
Philosophy

As mentioned before, the goal of this library is to be as lightweight as possible while still being flexible. In addition, the goal is to implement things in the simplest possible way. In the case for example of the input deck parser, this leads to a somewhat strange data structure.


---------
Development

As of July 2020, this code has been developed on my own. Up to now, I haven't released the code because I wanted to avoid having a situation where people were writing scripts that I would break by changing the OsirisDataContainer implementation. The code is still under development, but the OsirisDataContainer is very close to the final form that I envisioned when I first started writing this code. With that said, I do anticipate that changes will be made in the near-future based on the feedback of others. 

Thus, if you plan to use this code, I would suggest creating a virtual environment with a specific version so that when the time comes to update, you can write new scripts in a new virtual environment while using an older version to run old scripts. 

I am open to collaborating and accomodating basic feature requests that are in line with the above philosophy, but I intend to keep this repository nearly as lightweight as it is now. For example, anything more than the most basic of plotting capabilities which would be useful to nearly everyone should, in my view, be implemented in a separate repository which imports this library. Similarly, data processing pipelines likely to only be of use to a few individuals should be implemented as their own separate project. 


--------
Author 

Jacob Pierce, PhD student at UCLA



