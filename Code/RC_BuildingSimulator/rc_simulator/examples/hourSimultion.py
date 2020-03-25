"""
Main file to calculate the building loads
EN-13970
"""


import sys
import os

# Set root folder one level up, just for this example
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from building_physics import Building  # Importing Building Class

__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"


# Example Inpiuts
t_air = 10
t_m_prev = 22
internal_gains = 10  # Internal heat gains, in Watts
# Solar heat gains after transmitting through the winow [Watts]
solar_gains = 2000
ill = 44000  # Illuminance after transmitting through the window [Lumens]
occupancy = 0.1  # Occupancy for the timestep [people/hour/square_meter]


# Initialise an instance of the building. Empty brackets take on the
# default parameters. See buildingPhysics.py to see the default values
Office = Building()

# Solve for building energy
Office.solve_building_energy(internal_gains, solar_gains, t_air, t_m_prev)

# Solve for building lighting
Office.solve_building_lighting(ill, occupancy)




print(Office.t_m)  # Printing Room Temperature of the medium

print(Office.lighting_demand)  # Print Lighting Demand
print(Office.energy_demand)  # Print heating/cooling loads

# Example of how to change the set point temperature after running a simulation
Office.theta_int_h_set = 20.0

# Solve again for the new set point temperature
Office.solve_building_energy(internal_gains, solar_gains, t_air, t_m_prev)



print(Office.t_m)  # Print the new internal temperature


# Print a boolean of whether there is a heating demand
print(Office.has_heating_demand)
