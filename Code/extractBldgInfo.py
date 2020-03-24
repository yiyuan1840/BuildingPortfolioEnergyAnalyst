# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:52:48 2020

@author: yjia
"""


from shapely.geometry import Point, Polygon
import geopandas as gpd
from area import area
import geojsonio
import json
import os
import pandas as pd

#Set main folder 

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#Set path name for buildng json files 
footPrintJS = os.path.join(
    mainPath, 'Data', 'building_footprints.geojson')
buildingJS = os.path.join(
    mainPath, 'Data', 'building_attributes.json')

buildingArea = []
buildingHeight = []
buildingWWR = []
buildingName = []

#Read geojson file and reproject to WGS84 cordinates system
df_fp = gpd.read_file(footPrintJS)
df_fp = df_fp.to_crs(epsg='4326')

#Convert geo dataframe to json
fp = df_fp.to_json()

#Conver json to Python dict
fp_dict = json.loads(fp)

#Visualize building footprints through geojsonio 
geojsonio.display(fp)

#Extract information from json files for each building
for i in range(len(fp_dict['features'])):
    #Calculate building area using Python area package 
    ar = area(fp_dict['features'][i]['geometry'])
    buildingArea.append(ar)

with open(buildingJS) as bldg:    
    bd_dict = json.load(bldg)

for i in range(len(bd_dict['buildings'])):
    ht = bd_dict['buildings'][i]['height']
    wwr = bd_dict['buildings'][i]['window-to-wall ratio']
    name = bd_dict['buildings'][i]['name']
    buildingHeight.append(ht)
    buildingWWR.append(wwr)
    buildingName.append(name)
    

#Save structured and processed building information to a csv file     
data = {'buildingName':buildingName, 'buildingArea':buildingArea, 'buildingHeight':buildingHeight, 'buildingWWR':buildingWWR}    

df = pd.DataFrame(data, columns = ['buildingName', 'buildingArea', 'buildingHeight','buildingWWR'])

buildingInfo = os.path.join(
    mainPath, 'Data', 'buildingInfo.csv')
df.to_csv(buildingInfo, encoding='utf-8', index=False)