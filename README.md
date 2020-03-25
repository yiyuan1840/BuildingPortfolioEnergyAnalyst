# BuildingPortfolioEnergyAnalyst
## Python Program to Analyze Building Portfolio Energy Performance 

#### Dependencies
* shapely
* geopandas
* area
* geojsonio
* matplotlib
* datetime
* pandas

#### Workflow
This tool is built on top of RC_BuildingSimulator by Architecture and Building Systems of the ETH Zürich
https://github.com/architecture-building-systems/RC_BuildingSimulator
using a simplified 5R-1C building simulation model. 

The *extractBldgInfo.py* script parses two files that kept building information from a GIS data source: 
* building_attributes.json
* building_footprints.geojson

The building information in the json files are processed, structured and stored in a csv file:
* buildingInfo.csv

The *bldgSimulation.py* script reads the buildingInfo.csv and performs annual dynamic building energy simulation. The simulation outputs are written as *"building name" output.csv*, such as: 
* building one output.csv

The *bldgVisualization.py* script reads the *building output.csv* and calculates building utility cost, and generate two charts for each building:
* Building Hourly Energy Demand
* Building Monthly Utility Cost 

#### Building Assumptions
* Office utilization schedules adopted from from ASHREA 90.1 User Manual 
* Window U-value = 2.3 W/m2-K
* Window SHGC = 0.4 
* Wall U-value = 0.51 W/m2-k
* LPD = 11 W/m2
* EPD = 14 W/m2
* Infiltration = 0.1 ACH
* Ventilation =0.06 cfm/sf *Area+ 5 cfm * Number-of-Occupants (per ASHRAE 62.1) 

#### To-dos
Current building energy models assumes all buildings are square shaped, building footprint area are calculated with the geojson file, building width and depth are assumed to be the square root of building footprint area. 
Energy simulation results using the RC_BuilsingSimulator is roughly compared with EPC (an excel implementation of ISO-13790 standards), further comparisons and calibration are needed.  
