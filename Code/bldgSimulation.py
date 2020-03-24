"""
Example of an Annual Simulation
"""


import sys
import os

# Set root folder one level up, just for this example
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from building_physics import Building  # Importing Building Class
import supply_system
import emission_system
from radiation import Location
from radiation import Window

matplotlib.style.use('ggplot')
# matplotlib.pyplot.ion()

buidingInfo = buildingInfo = os.path.join(
    mainPath, 'Data', 'buildingInfo.csv')
df = pd.read_csv(buidingInfo)#print(df)

# Simulations Start Here
for i in range(len(df['buildingName'])):    
    name = df['buildingName'][i]
    ar = df['buildingArea'][i]
    ht = df['buildingHeight'][i]
    wwr = df['buildingWWR'][i]
    
    room_depth = math.sqrt(ar)
    room_width = math.sqrt(ar)
    room_height = ht
    
    external_envelope_area = math.sqrt(ar)*room_height*4
    window_area = external_envelope_area*wwr
    
    ach_vent = (0.06*ar/0.092903+5*ar/11)/(ar/0.092903)
    # Empty Lists for Storing Data to Plot
    ElectricityOut = []
    HeatingDemand = []  # Energy required by the zone
    HeatingEnergy = []  # Energy required by the supply system to provide HeatingDemand
    CoolingDemand = []  # Energy surplus of the zone
    CoolingEnergy = []  # Energy required by the supply system to get rid of CoolingDemand
    IndoorAir = []
    OutsideTemp = []
    SolarGains = []
    COP = []
    
    
    # Initialise the Location with a weather file
    Boston = Location(epwfile_path=os.path.join(
        mainPath,'Data','boston.epw'))
    
    # Initialise an instance of the building. Empty spaces take on the default
    # parameters. See buildingPhysics.py to see the default values
    Office = Building(window_area=window_area,
                      external_envelope_area=external_envelope_area,
                      room_depth=room_depth,
                      room_width=room_width,
                      room_height=room_height,
                      lighting_load=11,
                      lighting_control=300.0,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.51,
                      u_windows=2.3,
                      ach_vent=ach_vent,
                      ach_infl=0.1,
                      ventilation_efficiency=0.8,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20.0,
                      t_set_cooling=24.0,
                      max_cooling_energy_per_floor_area=-np.inf,
                      max_heating_energy_per_floor_area=np.inf,
                      heating_supply_system=supply_system.OilBoilerMed,
                      cooling_supply_system=supply_system.HeatPumpAir,
                      heating_emission_system=emission_system.NewRadiators,
                      cooling_emission_system=emission_system.AirConditioning,)
    
    # Define Windows
    SouthWindow = Window(azimuth_tilt=180, alititude_tilt=90, glass_solar_transmittance=0.4,
                          glass_light_transmittance=0.8, area=window_area/4)
    NorthWindow = Window(azimuth_tilt=0, alititude_tilt=90, glass_solar_transmittance=0.4,
                          glass_light_transmittance=0.8, area=window_area/4)
    WestWindow = Window(azimuth_tilt=90, alititude_tilt=90, glass_solar_transmittance=0.4,
                          glass_light_transmittance=0.8, area=window_area/4)
    EastWindow = Window(azimuth_tilt=270, alititude_tilt=90, glass_solar_transmittance=0.4,
                          glass_light_transmittance=0.8, area=window_area/4)
    
    
    # Define constants for the building
    gain_per_person = 73  # W per person
    appliance_gains = 14  # W per sqm
    max_occupancy = ar/11 # Number of people, 11m2/person
    lighting_gains = 11 # W per sqm
    
    
    # Read Occupancy Profile
    occupancyProfile = pd.read_csv(os.path.join(
        mainPath,'Code','RC_BuildingSimulator','rc_simulator', 'auxiliary', 'schedules_el_OFFICE.csv'))
    
    # Starting temperature of the builidng
    t_m_prev = 20
    
    # Loop through all 8760 hours of the year
    for hour in range(8760):
    
        # Occupancy for the time step
        occupancy = occupancyProfile.loc[hour, 'People'] * max_occupancy
        appliance = occupancyProfile.loc[hour, 'People'] * appliance_gains
        lighting = occupancyProfile.loc[hour, 'People'] * lighting_gains
        # Gains from occupancy and appliances
        internal_gains = occupancy * gain_per_person + \
            appliance * Office.floor_area + lighting * Office.floor_area
    
        # Extract the outdoor temperature in Boston for that hour
        t_out = Boston.weather_data['drybulb_C'][hour]
    
        Altitude, Azimuth = Boston.calc_sun_position(
            latitude_deg=42.37, longitude_deg=-71.02, year=2019, hoy=hour)
    
        SouthWindow.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                      normal_direct_radiation=Boston.weather_data[
                                          'dirnorrad_Whm2'][hour],
                                      horizontal_diffuse_radiation=Boston.weather_data['difhorrad_Whm2'][hour])
    
        SouthWindow.calc_illuminance(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                      normal_direct_illuminance=Boston.weather_data[
                                          'dirnorillum_lux'][hour],
                                      horizontal_diffuse_illuminance=Boston.weather_data['difhorillum_lux'][hour])
        NorthWindow.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                      normal_direct_radiation=Boston.weather_data[
                                          'dirnorrad_Whm2'][hour],
                                      horizontal_diffuse_radiation=Boston.weather_data['difhorrad_Whm2'][hour])
    
        NorthWindow.calc_illuminance(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                      normal_direct_illuminance=Boston.weather_data[
                                          'dirnorillum_lux'][hour],
                                      horizontal_diffuse_illuminance=Boston.weather_data['difhorillum_lux'][hour])
        
        WestWindow.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                      normal_direct_radiation=Boston.weather_data[
                                          'dirnorrad_Whm2'][hour],
                                      horizontal_diffuse_radiation=Boston.weather_data['difhorrad_Whm2'][hour])
    
        WestWindow.calc_illuminance(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                      normal_direct_illuminance=Boston.weather_data[
                                          'dirnorillum_lux'][hour],
                                      horizontal_diffuse_illuminance=Boston.weather_data['difhorillum_lux'][hour])
    
        EastWindow.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                      normal_direct_radiation=Boston.weather_data[
                                          'dirnorrad_Whm2'][hour],
                                      horizontal_diffuse_radiation=Boston.weather_data['difhorrad_Whm2'][hour])
    
        EastWindow.calc_illuminance(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                      normal_direct_illuminance=Boston.weather_data[
                                          'dirnorillum_lux'][hour],
                                      horizontal_diffuse_illuminance=Boston.weather_data['difhorillum_lux'][hour])
        solar_gains = SouthWindow.solar_gains+NorthWindow.solar_gains+WestWindow.solar_gains+EastWindow.solar_gains
        Office.solve_building_energy(internal_gains=internal_gains,
                                      solar_gains=solar_gains, t_out=t_out, t_m_prev=t_m_prev)
    
        Office.solve_building_lighting(illuminance=SouthWindow.transmitted_illuminance+NorthWindow.transmitted_illuminance+WestWindow.transmitted_illuminance
                                      +EastWindow.transmitted_illuminance, occupancy=occupancy)
    
        # Set the previous temperature for the next time step
        t_m_prev = Office.t_m_next
    
        HeatingDemand.append(Office.heating_demand)
        HeatingEnergy.append(Office.heating_energy)
        CoolingDemand.append(Office.cooling_demand)
        CoolingEnergy.append(Office.cooling_energy)
        ElectricityOut.append(Office.electricity_out)
        IndoorAir.append(Office.t_air)
        OutsideTemp.append(t_out)
        SolarGains.append(solar_gains)
        COP.append(Office.cop)
    
    annualResults = pd.DataFrame({
        'HeatingDemand': HeatingDemand,
        'HeatingEnergy': HeatingEnergy,
        'CoolingDemand': CoolingDemand,
        'CoolingEnergy': CoolingEnergy,
        'IndoorAir': IndoorAir,
        'OutsideTemp':  OutsideTemp,
        'SolarGains': SolarGains,
        'COP': COP
    })
    
    # Plotting has been commented out as it can not be conducted in a virtual environment over ssh
    # annualResults[['HeatingEnergy', 'CoolingEnergy']].plot()
    # plt.show()
    # ggplot(annualResults)
    buildingOutput = os.path.join(
        mainPath, 'Data', name+' output.csv')
    annualResults.to_csv(buildingOutput, encoding='utf-8', index=False)