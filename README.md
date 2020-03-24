# BuildingPortfolioEnergyAnalyst
#### Python Code to Analyze Building Portfolio Energy Performance 

This tool is build on top of RC_BuildingSimulator by Architecture and Building Systems of the ETH Zürich
https://github.com/architecture-building-systems/RC_BuildingSimulator
using a simplified 5R-1C buiding simulation model. 

The *extractBldgInfo.py* script parses two files that kept building information from a GIS data source: 
* building_attributes.json
* building_footprints.geojson

The building information in the json files are processed, structured and stored in a csv file:
* buildingInfo.csv

The *bldgSimulation.py* script reads the buildingInfo.csv and performs annual dynamic building energy simulation. The simulation outputs are written as *"building name" output.csv*, such as: 
* building one output.csv

The *bldgVisualization.py* script reads the *building output.csv* and generate two charts for each building:
* Building Hourly Energy Demand
* Buiding Monthly Utility Cost 

#### Limitations
The analysis assumes all buildings are squre shaped 
