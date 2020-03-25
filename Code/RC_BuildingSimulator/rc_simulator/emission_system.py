"""
Emission System Parameters for Heating and Cooling

Model of different Emission systems. New Emission Systems can be introduced by adding new classes

Note that this is currently in a very basic form, and has been created to allow for more complex expansion 

Supply temperatures are taken from the CEA Toolbox 
https://github.com/architecture-building-systems/CEAforArcGIS/blob/master/cea/databases/CH/Systems/emission_systems.xls

TODO: Validation is still required
TODO: Need to double check supply temperatures, waiting on reply from the CEA team

"""


__author__ = "Prageeth Jayathissa, Michael Fehr"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["CEA Toolbox"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "p.jayathissa@gmail.com"
__status__ = "production"



class EmissionDirector:

    """
    The director sets what Emission system is being used, and runs that set Emission system
    """

    builder = None

    # Sets what Emission system is used
    def set_builder(self, builder):
        #        self.__builder = builder
        self.builder = builder
    # Calcs the energy load of that system. This is the main() fu

    def calc_flows(self):

        # Director asks the builder to produce the system body. self.builder
        # is an instance of the class

        body = self.builder.heat_flows()

        return body


class EmissionSystemBase:

    """ 
    The base class in which systems are built from
    """

    def __init__(self, energy_demand):

        self.energy_demand = energy_demand


    def heat_flows(self): pass
    """
    determines the node where the heating/cooling system is active based on the system used
    Also determines the return and supply temperatures for the heating/cooling system
    """


class OldRadiators(EmissionSystemBase):
    """
    Old building with radiators and high supply temperature
    Heat is emitted to the air node
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 65
        flows.heating_return_temperature = 45
        flows.cooling_supply_temperature = 12
        flows.cooling_return_temperature = 21

        return flows


class NewRadiators(EmissionSystemBase):
    """    
    Newer building with radiators and medium supply temperature
    Heat is emitted to the air node
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 50
        flows.heating_return_temperature = 35
        flows.cooling_supply_temperature = 12
        flows.cooling_return_temperature = 21

        return flows

class ChilledBeams(EmissionSystemBase):
    """
    Chilled beams: identical to newRadiators but used for cooling
    Heat is emitted to the air node
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 50
        flows.heating_return_temperature = 35
        flows.cooling_supply_temperature = 18
        flows.cooling_return_temperature = 21

        return flows


class AirConditioning(EmissionSystemBase):
    """
    All heat is given to the air via an AC-unit. HC input via the air node as in the ISO 13790 Annex C.
    supplyTemperature as with new radiators (assumption)
    Heat is emitted to the air node
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 40
        flows.heating_return_temperature = 20
        flows.cooling_supply_temperature = 6
        flows.cooling_return_temperature = 15

        return flows

class FloorHeating(EmissionSystemBase):
    """
    All HC energy goes into the surface node, supplyTemperature low
    Heat is emitted to the surface node
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = 0
        flows.phi_st_plus = self.energy_demand
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 40
        flows.heating_return_temperature = 5
        flows.cooling_supply_temperature = 12
        flows.cooling_return_temperature = 21

        return flows

class TABS(EmissionSystemBase):
    """
    Thermally activated Building systems. HC energy input into bulk node. Supply Temperature low.
    Heat is emitted to the thermal mass node
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = 0
        flows.phi_st_plus = 0
        flows.phi_m_plus = self.energy_demand

        flows.heating_supply_temperature = 50
        flows.heating_return_temperature = 35
        flows.cooling_supply_temperature = 12
        flows.cooling_return_temperature = 21

        return flows


class Flows:
    """
    A base object to store output variables
    """

    phi_ia_plus = float("nan")
    phi_m_plus = float("nan")
    phi_st_plus = float("nan")

    heating_supply_temperature = float("nan")
    cooling_supply_temperature = float("nan")
    # return temperatures
