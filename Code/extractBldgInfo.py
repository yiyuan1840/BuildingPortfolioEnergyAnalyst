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

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

footPrintJS = os.path.join(
    mainPath, 'Data', 'building_footprints.geojson')
buildingJS = os.path.join(
    mainPath, 'Data', 'building_attributes.json')

buildingArea = []
buildingHeight = []
buildingWWR = []
buildingName = []


# fname = r"c:\Users\yjia\Desktop\Building Assignment\Data\building_footprints.geojson"
df_fp = gpd.read_file(footPrintJS)


df_fp = df_fp.to_crs(epsg='4326')

# df.to_file("output.json", driver="GeoJSON")

fp = df_fp.to_json()

fp_dict = json.loads(fp)

geojsonio.display(fp)
for i in range(len(fp_dict['features'])):
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
    
    
data = {'buildingName':buildingName, 'buildingArea':buildingArea, 'buildingHeight':buildingHeight, 'buildingWWR':buildingWWR}    

df = pd.DataFrame(data, columns = ['buildingName', 'buildingArea', 'buildingHeight','buildingWWR'])

buildingInfo = os.path.join(
    mainPath, 'Data', 'buildingInfo.csv')
df.to_csv(buildingInfo, encoding='utf-8', index=False)