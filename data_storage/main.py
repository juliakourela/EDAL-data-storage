import pandas as pd
import geojson
from shapely.geometry import mapping, MultiPolygon  # Import mapping function

from libs.json_interface import *
from libs.ingest_datasets import *

<<<<<<< HEAD


def create_json(filename, filepath):
    #geojson_data = []
    #geojson_data += ingest_polygon_boundaries(filepath+'gadm41_MEX_0.json')
    #geojson_data += ingest_polygon_boundaries(filepath+'gadm41_MEX_1.json')

    #data_to_json(geojson_data, 'polygon_boundaries.json')
=======

def main():
    filename = "output.json"
    filepath = "data/"

    geojson_data = []
    raw_geojson_data = []
    raw_geojson_data += ingest_polygon_boundaries(filepath + "gadm41_MEX_0.json")
    # geojson_data += ingest_polygon_boundaries(filepath+'gadm41_MEX_1.json')
    print("Raw GeoJSON Data:")
    print(raw_geojson_data)

    # Construct GeoJSON features directly from the raw GeoJSON data
    for feature in raw_geojson_data:
        geojson_data.append(feature)

    print("GeoJSON Data After Conversion:")
    print(geojson_data)

    # Convert MultiPolygon objects to JSON-serializable format
    for feature in geojson_data:
        if "geometry" in feature and "coordinates" in feature["geometry"]:
            coords = feature["geometry"]["coordinates"]
            if isinstance(coords, MultiPolygon):
                # Convert MultiPolygon to a JSON-serializable format
                feature["geometry"]["coordinates"] = mapping(coords)

    # Construct GeoJSON FeatureCollection
    geojson_features = {"type": "FeatureCollection", "features": geojson_data}

    print("Final GeoJSON:")
    print(geojson_features)
    filename = "polygon_boundaries.json"
    data = geojson_features
    with open(filename, "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)

    # data_to_json(geojson_features, "polygon_boundaries.json")
    return
>>>>>>> 097ed0e (Changes to main script to add polygon coordinates)

    data = open_json(filename)

    data = add_features_from_ef(data, filepath + "Emissions_Factors.xlsx")

    data = add_features_from_fuel_mix(data, "Mexico", filepath + "MX_Fuel_Mixes.xlsx")
    data = add_features_from_fuel_mix(
        data, "Indonesia", filepath + "ID_Fuel_Mixes.xlsx"
    )

    data = add_features_from_EUI(
        data, "Mexico", filepath + "MX_EUI_CURB_estimates.xlsx"
    )
    data = add_features_from_EUI(
        data, "Indonesia", filepath + "ID_EUI_CURB_estimates.xlsx"
    )

    data_to_json(data, filename)


<<<<<<< HEAD
#def create_csv(filename, filepath):
   # print()


def main():
    json_filename = 'output.json'
    filepath = 'data/'
    create_json(json_filename, filepath)
    

    
  
  
if __name__=="__main__":
=======
if __name__ == "__main__":
>>>>>>> 097ed0e (Changes to main script to add polygon coordinates)
    main()
