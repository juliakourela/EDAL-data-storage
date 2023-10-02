import pandas as pd


filenames = {
    "canada1.csv": [
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
    "canada2.csv": [
        "sector",
        "direct_emissions_tco2e",
        "direct_emissions_notation",
        "indirect_emissions_tco2e",
        "indirect_emissions_notation",
        "outside_city_emissions_tco2e",
        "outside_city_emissions_notation",
        "notes",
        "geoname",
    ],
    "canada3.csv": [
        "Inventory year",
        "GPC ref. no.",
        "CRF - Sector",
        "CRF - Sub-sector",
        "Scope",
        "Fuel type or activity",
        "Notation key",
        "Activity data - Amount",
        "Activity data - Unit",
        "Activity data - Description",
        "Activity data - Source",
        "Activity data - Data Quality",
        "Emission factor - Unit",
        "Emission factor - CO2",
        "Emission factor - CH4",
        "Emission factor - N2O",
        "Emission factor - Total CO2e",
        "Emission factor - Biogenic CO2",
        "Oxidation factor",
        "Emission factor - Year",
        "Emission factor - Scale",
        "Emission factor - Description",
        "Emission factor - Source",
        "Emission factor - Data Quality",
        "GHGs (metric tonnes CO2e) - CO2",
        "GHGs (metric tonnes CO2e) - CH4",
        "GHGs (metric tonnes CO2e) - N2O",
        "GHGs (metric tonnes CO2e) - Total CO2e",
        "GHGs (metric tonnes CO2e) - Biogenic CO2",
        "Activity data conversion - original activity",
        "Activity data conversion - original unit",
        "Activity data conversion - conversion value",
        "Activity data conversion - override used?",
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


def create_dataframe(filenames):
    return None


if __name__ == "__main__":
    df2 = to_df("canada2.csv", filenames["canada2.csv"])
    df2_pivot = df2_pivot(df2)
    print(df2_pivot.head())
