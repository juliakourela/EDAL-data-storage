import pandas as pd
import geopandas as gpd
import json
from .feature_collection_ops import *
from .geonames_interface import *
from unidecode import unidecode


# returns {'Municipalities': list of municipality names,
#          'Residential': dict of {'Municipality': Multiplier},
#          'Commercial': dict of {'Municipality': Multiplier}}
def get_country_multipliers(country_of_interest, country_specific_euis):
    country_eui = pd.read_excel(country_specific_euis).dropna()
    country_res_multipliers = dict(
        zip(
            country_eui["City"],
            country_eui["Energy Use Intensity by End Use (kwh/m2/year)"],
        )
    )
    country_comm_multipliers = dict(
        zip(
            country_eui["City"],
            country_eui["Energy Use Intensity by End Use (kwh/m2/year)2"],
        )
    )

    return {
        "Municipalities": list(country_res_multipliers.keys()),
        "Residential Multipliers": country_res_multipliers,
        "Commercial Multipliers": country_comm_multipliers,
    }


def add_features_from_EUI(data, region_of_interest, eui_dataset_filename):
    multipliers = get_country_multipliers(region_of_interest, eui_dataset_filename)

    for municipality in multipliers["Municipalities"]:
        plaintext_municipality = unidecode(municipality)
        feature = create_feature(
            data,
            plaintext_municipality,
            "Municipality",
            None,
            None,
            multipliers["Residential Multipliers"][municipality],
            multipliers["Commercial Multipliers"][municipality],
            "Wikipedia",
            "2000-01-01",
            "2023-01-01",
            "N/A",
        )
        if feature != None:
            data.append(feature)

    return data


def ingest_emissions_factors(ef_dataset):
    ef = pd.read_excel(ef_dataset, sheet_name="Emissions Factors").dropna()[1:]
    ef = ef.rename(
        columns={
            "Carbon Dioxide Emissions Coefficients by Fuel": "Carbon Dioxide (CO2) Factor",
            "Unnamed: 1": "Pounds CO2 (Per Unit of Volume or Mass)",
            "Unnamed: 2": "Kilograms CO2 (Per Unit of Volume or Mass)",
            "Unnamed: 3": "Pounds CO2 Per Million Btu",
            "Unnamed: 4": "Kilograms CO2 Per Million Btu",
        }
    )
    ef_dict = ef.to_dict("records")
    return ef_dict


def add_features_from_ef(data, ef_dataset):
    ef = ingest_emissions_factors(ef_dataset)
    feature = create_feature(
        data,
        "North America",
        "Continent",
        ef,
        None,
        None,
        None,
        "Wikipedia",
        "2000-01-01",
        "2023-01-01",
        "N/A",
    )

    if feature != None:
        data.append(feature)

    return data


def ingest_fuel_mixes(fuel_mix_dataset):
    country_fmix = pd.read_excel(fuel_mix_dataset).dropna()[1:]
    country_fmix = country_fmix.rename(
        columns={
            "Geographic Area Selection:": "Residential Non-Electricity Heating Source",
            "Unnamed: 1": "Percentage Of New Total (less 'Other')",
            "Unnamed: 2": "Kg CO2 emissions/ MMBtu",
            "Unnamed: 3": "CO2 Emissions Weighted by Percentage of Fuel Mix",
        }
    )
    fuel_dict = country_fmix.to_dict("records")
    return fuel_dict


def add_features_from_fuel_mix(data, region_of_interest, fuel_mix_dataset):
    fuel_mix = ingest_fuel_mixes(fuel_mix_dataset)
    feature = create_feature(
        data,
        region_of_interest,
        "Country",
        None,
        fuel_mix,
        None,
        None,
        "Wikipedia",
        "2000-01-01",
        "2023-01-01",
        "N/A",
    )

    if feature != None:
        data.append(feature)

    return data


def ingest_polygon_boundaries(polygon_dataset):
    polygon_ds = gpd.read_file(polygon_dataset).dropna()
    # polygon_ds.set_geometry("geometry").set_index("id")
    # print(polygon_ds)
    feature_index = []
    for x in range(len(polygon_ds.index)):
        if x >= len(polygon_ds.index):
            break
        if "NAME_2" in polygon_ds.columns.tolist():
            geonamesID = unidecode(polygon_ds["NAME_2"][x])
        elif "NAME_1" in polygon_ds.columns.tolist():
            geonamesID = unidecode(polygon_ds["NAME_1"][x])
        else:
            geonamesID = unidecode(polygon_ds["COUNTRY"][x])

        feature = {
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": polygon_ds["geometry"][x]},
            "properties": {"geonamesID": get_geonames_id("juliakourela", geonamesID)},
        }
        feature_index.append(feature)
    return feature_index


def add_polygon_coord(filenames, output_file):

    
    with open(output_file, "r") as output:
        output_data = json.load(output)

    for poly_filename in filenames: 

        with open(poly_filename, "r") as polygon_file:
            polygon_data = json.load(polygon_file)
    
        # Create a dictionary to map geonames_id to polygon features
        geonames_to_polygon = {
            str(feature["properties"]["geonamesID"]): feature
            for feature in polygon_data["features"]
        }

        # Iterate through emissions_data and add polygon coordinates
        for item in output_data:
            # Use geonames_id to find the corresponding polygon feature in the dictionary
            geonames_id = str(item["geonames_id"])
            polygon_feature = geonames_to_polygon.get(geonames_id)

            if polygon_feature:
                # Add the "geometry" key with polygon coordinates to the output data
                item["geometry"] = polygon_feature["geometry"]
    filename = "combined.json"
    # Save the combined data to a new JSON file
    with open(filename, "w") as outfile:
        json.dump(output_data, outfile, sort_keys=True, indent=4)
