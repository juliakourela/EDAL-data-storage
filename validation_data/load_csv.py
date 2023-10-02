import pandas as pd


filenames = {'canada1.csv': 
             ['name', 
              'country',
              'region', 
              'geoname', 
              'year',
              'boundary', 
              'population', 
              'climate', 
              'latitute',
              'longitude'], 

             'canada2.csv': 
             ['sector', 
              'direct_emissions_tco2e',
              'direct_emissions_notation', 
              'indirect_emissions_tco2e',
              'indirect_emissions_notation', 
              'outside_city_emissions_tco2e',
              'outside_city_emissions_notation', 
              'notes', 
              'geoname'], 
              
             'canada3.csv': 
             ['Inventory year', 
              'GPC ref. no.', 
              'CRF - Sector',
              'CRF - Sub-sector', 
              'Scope', 
              'Fuel type or activity', 
              'Notation key',
              'Activity data - Amount', 
              'Activity data - Unit',
              'Activity data - Description', 
              'Activity data - Source',
              'Activity data - Data Quality', 
              'Emission factor - Unit',
              'Emission factor - CO2', 
              'Emission factor - CH4',
              'Emission factor - N2O', 
              'Emission factor - Total CO2e',
              'Emission factor - Biogenic CO2', 
              'Oxidation factor',
              'Emission factor - Year', 
              'Emission factor - Scale',
              'Emission factor - Description', 
              'Emission factor - Source',
              'Emission factor - Data Quality', 
              'GHGs (metric tonnes CO2e) - CO2',
              'GHGs (metric tonnes CO2e) - CH4', 
              'GHGs (metric tonnes CO2e) - N2O',
              'GHGs (metric tonnes CO2e) - Total CO2e',
              'GHGs (metric tonnes CO2e) - Biogenic CO2',
              'Activity data conversion - original activity',
              'Activity data conversion - original unit',
              'Activity data conversion - conversion value',
              'Activity data conversion - override used?', 
              'geoname']}

def to_df(filename, cols):
    return pd.read_csv(filename, usecols=cols)

def create_dataframe(filenames):
    dfs = []
    for filename, cols in filenames.items():
        df = to_df(filename, cols)
        dfs.append(df)

    final_df = pd.concat(dfs, axis=1)
    return final_df



