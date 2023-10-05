import pandas as pd
import geojson
from shapely.geometry import mapping, MultiPolygon  # Import mapping function

from libs.json_interface import *
from libs.ingest_datasets import *


def main():
    filename = "output.json"
    filepath = "data/"

    read_file = [
        "data/gadm41_MEX_0.json",
        "data/gadm41_MEX_1.json",
        "data/gadm41_MEX_2.json",
    ]

    for idx, file in enumerate(read_file):
        raw_geojson_data = []
        raw_geojson_data = ingest_polygon_boundaries(file)
        for feature in raw_geojson_data:
            if "geometry" in feature and "coordinates" in feature["geometry"]:
                coords = feature["geometry"]["coordinates"]
                if isinstance(coords, MultiPolygon):
                    # Convert MultiPolygon to a JSON-serializable format
                    feature["geometry"]["coordinates"] = mapping(coords)
        # Construct GeoJSON FeatureCollection
        geojson_features = {"type": "FeatureCollection", "features": raw_geojson_data}
        filename = f"polygon_boundaries_{idx}.json"
        data_to_json(geojson_features, filename)
    return

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

    return


if __name__ == "__main__":
    main()
