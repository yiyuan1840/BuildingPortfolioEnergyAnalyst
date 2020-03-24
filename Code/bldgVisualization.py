# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:15:16 2020

@author: yjia
"""



import sys
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import datetime as dt


# Set root folder one level up, just for this example
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)


buidingOne =  os.path.join(
    mainPath, 'Data', 'building one output.csv')
# buidingTwo =  os.path.join(
#     mainPath, 'Data', 'building two output.csv')
# buidingThree =  os.path.join(
#     mainPath, 'Data', 'building three output.csv')

df_bldg_1 = pd.read_csv(buidingOne)
# df_bldg_2 = pd.read_csv(buidingTwo)
# df_bldg_3 = pd.read_csv(buidingThree)

timeIndex = pd.date_range(start=pd.datetime(2019,1,1),freq='H',periods=8760)

# Average Retail Price for Electricity in MA is $0.185/kWh
# Source: https://www.eia.gov/electricity/state/
# Average Retail Price for Natural Gas in MA is $12.56/thousand cubic feet or $(12.26/1.036)/MMBtu
# Source: https://www.eia.gov/dnav/ng/ng_pri_sum_dcu_SMA_m.htm
bldg_1_area = df_info['buildingArea'][0]

df_bldg_1['FuelConsumption_MMBtu'] = df_bldg_1['HeatingEnergy']*3.412142/1000000
# df_bldg_2['FuelConsumption_MMBtu'] = df_bldg_2['HeatingEnergy']*3.412142/1000000
# df_bldg_3['FuelConsumption_MMBtu'] = df_bldg_3['HeatingEnergy']*3.412142/1000000

df_bldg_1['ElectriciyConsumption_kWh'] = df_bldg_1['CoolingEnergy']/1000
# df_bldg_2['ElectriciyConsumption_kWh'] = df_bldg_2['HeatingEnergy']/1000
# df_bldg_3['ElectriciyConsumption_kWh'] = df_bldg_3['HeatingEnergy']/1000
bldg_1_fuelCost = df_bldg_1['FuelConsumption_MMBtu']*12.26/1.036
bldg_1_elecCost = df_bldg_1['ElectriciyConsumption_kWh']*0.185

df_bldg_1['UtilityCost_$'] = df_bldg_1['FuelConsumption_MMBtu']*12.26/1.036 + df_bldg_1['ElectriciyConsumption_kWh']*0.185
# df_bldg_2['UtilityCost_$'] = df_bldg_2['FuelConsumption_MMBtu']*12.26/1.036 + df_bldg_2['ElectriciyConsumption_kWh']*0.185
# df_bldg_3['UtilityCost_$'] = df_bldg_3['FuelConsumption_MMBtu']*12.26/1.036 + df_bldg_3['ElectriciyConsumption_kWh']*0.185

bldgOneUtilCost = df_bldg_1['UtilityCost_$'].sum()
# bldgTwoUtilCost = df_bldg_2['UtilityCost_$'].sum()
# bldgThreeUtilCost = df_bldg_3['UtilityCost_$'].sum()
# bldgPortfolioCost = bldgOneUtilCost + bldgTwoUtilCost + bldgThreeUtilCost

# print(bldgPortfolioCost,bldgOneUtilCost)

bldg_1_heatDemand = pd.Series(df_bldg_1['HeatingDemand'].values, index=timeIndex)
bldg_1_heatDemand = bldg_1_heatDemand/bldg_1_area # Heating Demand in W/m2



bldg_1_coolDemand = pd.Series(df_bldg_1['CoolingDemand'].values, index=timeIndex)
bldg_1_coolDemand = bldg_1_coolDemand/bldg_1_area # Cooling Demand in W/m2

##### PLot Hourly Heating and Cooling Demand

fig = plt.figure(figsize=[25,10], dpi=100)
plt.rc('font', size=22)
fig.subplots_adjust(top=0.8)
ax1 = fig.add_subplot(111)
ax1.set_ylabel('Heating/Cooling Demand, W/m2')
ax1.set_title('Building One Heating and Cooling Demand')
bldg_1_heatDemand.plot()
bldg_1_coolDemand.plot()
plt.legend(['Heating Demand','Cooling Demand'])

# plt.show()
plt.savefig('bldg1_Houly_Energy_Demand.png')




##### Plot Monthly Utility Cost $

# bldg_1_Cost = pd.Series(df_bldg_1['UtilityCost_$'].values, index=timeIndex)
# bldg_1_fuelCost = pd.Series(bldg_1_fuelCost.values, index=timeIndex)
# bldg_1_elecCost = pd.Series(bldg_1_elecCost.values, index=timeIndex)

# plt.figure(figsize=[25,10], dpi=100)
# plt.rc('font', size=22)
# plt.bar(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
#         bldg_1_fuelCost.resample('M').sum(), color='red',edgecolor='black')

# plt.bar(range(len(bldg_1_elecCost.resample('M').sum())), bldg_1_elecCost.resample('M').sum(), 
#         bottom=bldg_1_fuelCost.resample('M').sum(), color='royalblue',edgecolor='black')
# plt.ylabel('Energy Utility Cost, $')
# plt.title('Buiding Three Monthly Utility Cost')
# plt.legend(['Natural Gas','Electricity'])
# plt.savefig('bldg3_Monthly_Util_Cost.png')





