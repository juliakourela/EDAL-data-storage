import pandas as pd
import os

filenames = {
    "1.csv": [
        "name",
        "country",
        "region",
        "geoname",
        "year",
        "boundary",
        "population",
        "climate",
        "latitute",
        "longitude",
    ],
    "2.csv": [
        "sector",
        "direct_emissions_tco2e",
        #"direct_emissions_notation",
        "indirect_emissions_tco2e",
        #"indirect_emissions_notation",
        #"outside_city_emissions_tco2e",
        #"outside_city_emissions_notation",
        #"notes",
        "geoname",
    ],
    "3.csv": [
        #"Inventory year",
        #"GPC ref. no.",
        #"CRF - Sector",
        "CRF - Sub-sector",
        "Scope",
        "Fuel type or activity",
        #"Notation key",
        #"Activity data - Amount",
        #"Activity data - Unit",
        #"Activity data - Description",
        #"Activity data - Source",
        #"Activity data - Data Quality",
        #"Emission factor - Unit",
        #"Emission factor - CO2",
        #"Emission factor - CH4",
        #"Emission factor - N2O",
        #"Emission factor - Total CO2e",
        #"Emission factor - Biogenic CO2",
        #"Oxidation factor",
        #"Emission factor - Year",
        #"Emission factor - Scale",
        #"Emission factor - Description",
        #"Emission factor - Source",
        #"Emission factor - Data Quality",
        #"GHGs (metric tonnes CO2e) - CO2",
        #"GHGs (metric tonnes CO2e) - CH4",
        #"GHGs (metric tonnes CO2e) - N2O",
        "GHGs (metric tonnes CO2e) - Total CO2e",
        #"GHGs (metric tonnes CO2e) - Biogenic CO2",
        #"Activity data conversion - original activity",
        #"Activity data conversion - original unit",
        #"Activity data conversion - conversion value",
        #"Activity data conversion - override used?",
        "geoname",
    ],
}


def to_df(filename, cols):
    return pd.read_csv(filename, usecols=cols)


def df2_pivot(df):
    # manipulating the second csv file
    df["sector"] = df["sector"].str.split(" > ").str[-1].str.split(" & ").str[0]
    pivot_data = df.pivot_table(
        index="geoname",
        columns="sector",
        values=["direct_emissions_tco2e", "indirect_emissions_tco2e"],
        aggfunc="first",
    )
    pivot_data.reset_index(inplace=True)
    pivot_data.columns = [
        f"{sector}_{col}" if col != "geoname" else col
        for col, sector in pivot_data.columns
    ]
    return pivot_data


def df3_pivot(df):
    # manipulating the third csv file
    headers = {"Residential Buildings": "RESIDENTIAL",
               "Commercial Buildings": "COMMERCIAL",
               "Industry": "INDUSTRY",
               'Institutional Buildings': "INSTITUTIONAL",
               "Electricity": "electricity",
               "Diesel oil": "diesel",
               "Kerosene": "kerosene", 
               "Natural gas": "natural_gas",
               "Residual fuel oil": "res_fuel_oil",
               "Liquefied Petroleum Gas (LPG)": "lpg",
               "Wood or wood waste": "wood",
               'Coal (Bituminous or Black coal)': "coal",
               'District heating - hot water': "district_heating"}

    pivot_data = df.pivot_table(
        index="geoname",
        columns=['CRF - Sub-sector', 'Fuel type or activity'],
        values=["GHGs (metric tonnes CO2e) - Total CO2e"],
        aggfunc="first",
    )
    pivot_data.columns = [headers[c[1]] + "-" + headers[c[2]] for c in pivot_data.columns]

    for val in ["electricity", "diesel", "natural_gas", "kerosene", "res_fuel_oil", "lpg", "wood", "coal", "district_heating"]:
        sum_cols = [col for col in pivot_data.columns if val in col]
        if sum_cols != []:
            pivot_data[f'COMBINED-{val}'] = pivot_data[sum_cols].sum(axis=1)
    
    for val in ["COMMERCIAL", "RESIDENTIAL", "INDUSTRY", "INSTITUTIONAL", "COMBINED"]:
        sum_cols = [col for col in pivot_data.columns if val in col and "electricity" not in col]
        if sum_cols != []:
            pivot_data[f'{val}-total_non_electricity'] = pivot_data[sum_cols].sum(axis=1)

    return pivot_data


def create_dataframes(country):
    dfs = []
    for fn in filenames.keys():
        dfs.append(to_df('energyconsumption/'+country+fn, filenames[fn]))
    return dfs


def aggregate_csvs(dfs, country):
    df1, df2, df3 = dfs[0], dfs[1], dfs[2]
    
    #df2_edited = df2_pivot(df2)

    df3_edited = df3_pivot(df3)

    #df1_and_df2 = pd.merge(df1, df2_edited, on = "geoname", how = "outer")
    #final_df= pd.merge(df1_and_df2, df3_edited, on = "geoname", how = "outer")
    final_df= pd.merge(df1, df3_edited, on = "geoname", how = "outer")
    final_df.rename(columns={"latitute": "latitude"}, inplace=True)

    final_df.to_csv(f'outputfiles/dpfcdata_{country}.csv')


if __name__ == "__main__":

    countries = list(set(map(lambda x: x[:-5], os.listdir('energyconsumption'))))
    if '.DS_' in countries:
        countries.remove('.DS_')

    for country in countries:
        print(country)
        dfs = create_dataframes(country)
        final_csv = aggregate_csvs(dfs, country)