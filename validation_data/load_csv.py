import pandas as pd
import os


#output_filetype = "csv"
output_filetype = "parquet"

input_files_directory = "energyconsumption"

# Any column names commented out will not be loaded 
# in to the initial dataframe.
filenames = {
    # The first input CSV file, containing mostly metadata.
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
    # The second input CSV file, containing summarized statistics
    # of direct/indirect CO2 emissions broken down by sector.
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
    # The third input CSV file, containing emissions broken down 
    # by sector, fuel type, and emission product.
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

# Any fuel types/activities commented out will not be 
# included in the output file, or in the combined
# total of non-electricity emissions for each sector.
valid_fuel_types = ["Electricity",
                    "Diesel oil",
                    "Kerosene",
                    "Natural gas",
                    "Residual fuel oil",
                    "Liquefied Petroleum Gas (LPG)",
                    #"Wood or wood waste",
                    #'Coal (Bituminous or Black coal)',
                    #'District heating - hot water'
                    ]

# Any sectors commented out will not be 
# included in the output file, or in the combined
# total of emissions for each fuel type.
valid_sectors = ["Residential Buildings", 
                 "Commercial Buildings", 
                 "Industry", 
                 'Institutional Buildings'
                 ]


# Manipulating the second csv file
def df2_pivot(df):
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


# Manipulating the third csv file
def df3_pivot(df):
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

    fuel_types_mask = df['Fuel type or activity'].isin(valid_fuel_types)
    sectors_mask = df['CRF - Sub-sector'].isin(valid_sectors)

    # create columns of CO2 emissions for each sector broken down by fuel type
    pivot_data = df[fuel_types_mask & sectors_mask].pivot_table(
        index="geoname",
        columns=['CRF - Sub-sector', 'Fuel type or activity'],
        values=["GHGs (metric tonnes CO2e) - Total CO2e"],
        aggfunc="first",
    )

    pivot_data.columns = [headers[c[1]] + "-" + headers[c[2]] for c in pivot_data.columns]

    # create columns of combined CO2 emissions for all sectors, broken down by fuel type
    for val in ["electricity", "diesel", "natural_gas", "kerosene", "res_fuel_oil", "lpg", "wood", "coal", "district_heating"]:
        sum_cols = [col for col in pivot_data.columns if val in col]
        if sum_cols != []:
            pivot_data[f'COMBINED-{val}'] = pivot_data[sum_cols].sum(axis=1)
    
    # create columns of combined CO2 emissions for all non-electricity fuel types, broken down by sector
    for val in ["COMMERCIAL", "RESIDENTIAL", "INDUSTRY", "INSTITUTIONAL", "COMBINED"]:
        sum_cols = [col for col in pivot_data.columns if val in col and "electricity" not in col]
        if sum_cols != []:
            pivot_data[f'{val}-total_non_electricity'] = pivot_data[sum_cols].sum(axis=1)
    
    cols = pivot_data.columns
    pivot_data = pivot_data[sorted(cols, key=lambda x: x.split("-")[-1])]

    return pivot_data


def to_df(filename, cols):
    return pd.read_csv(filename, usecols=cols)


def create_dataframes(country):
    dfs = []
    for fn in filenames.keys():
        dfs.append(to_df(input_files_directory+'/'+country+fn, filenames[fn]))
    return dfs


def aggregate_csvs(dfs, country, output_filetype):
    df1, df2, df3 = dfs[0], dfs[1], dfs[2]
    
    #df2_edited = df2_pivot(df2)

    df3_edited = df3_pivot(df3)

    #df1_and_df2 = pd.merge(df1, df2_edited, on = "geoname", how = "outer")
    #final_df= pd.merge(df1_and_df2, df3_edited, on = "geoname", how = "outer")
    final_df= pd.merge(df1, df3_edited, on = "geoname", how = "outer")
    final_df.rename(columns={"latitute": "latitude"}, inplace=True)

    if output_filetype == "parquet":
        final_df.to_parquet(f'outputfiles/dpfcdata_{country}.parquet')
    elif output_filetype == "csv":
        final_df.to_csv(f'outputfiles/dpfcdata_{country}new.csv')


if __name__ == "__main__":

    countries = list(set(map(lambda x: x[:-5], os.listdir(input_files_directory))))
    if '.DS_' in countries:
        countries.remove('.DS_')

   #countries=['canada']

    for country in countries:
        print(country)
        dfs = create_dataframes(country)
        aggregate_csvs(dfs, country, output_filetype)