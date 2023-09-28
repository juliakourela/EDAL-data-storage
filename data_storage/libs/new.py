import pandas as pd
import geopandas as gpd
from geonames_interface import *
from unidecode import unidecode

def ingest_polygon_boundaries(polygon_dataset):
    polygon_ds = gpd.read_file(polygon_dataset).dropna()
    print(polygon_ds)
    feature_index = []
    for x in range(len(polygon_ds.index)):
        if x >= len(polygon_ds.index): break
        if 'NAME_1' in polygon_ds.columns.tolist():
            geonamesID = unidecode(polygon_ds['NAME_1'][x])
        else:
            geonamesID = unidecode(polygon_ds['COUNTRY'][x])

        feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",  
                    "coordinates": polygon_ds['geometry'][x]
                },
                "properties": {

                    "geonamesID": get_geonames_id('juliakourela', 
                                                geonamesID)
                }}
        feature_index.append(feature)
    return feature_index

ingest_polygon_boundaries('gadm41_MEX_0.json')
ingest_polygon_boundaries('gadm41_MEX_1.json')