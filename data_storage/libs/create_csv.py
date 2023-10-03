import pandas as pd
from datetime import date
from os import path
from libs.geonames_interface import *


def init_csv(filename, filepath):
    # if output file doesn't exist already, create it
    if path.isfile(filename) is False:
        empty_dataframe = pd.DataFrame(columns=['name','feature_type',
        'geonames_id','emissions_factor','fuel_use_mix','eui_residential_multiplier',
        'eui_commercial_multiplier', 'source', 'acquisition_date', 'valid_start_date',
        'valid_end_date','notes'])
        empty_dataframe.to_csv(filename)

    df = pd.read_csv(filename)
    return df


def add_row(data, name, feature_type,
            emissions_factor, fuel_use_mix, 
            eui_residential_multiplier, 
            eui_commercial_multiplier, source, 
            valid_start_date, valid_end_date, notes):
    
    geonames_id = get_geonames_id('juliakourela', name)
    if geonames_id == None:
        return
    
    new_row = {
        'name': name,
        'feature_type': feature_type,
        'geonames_id': geonames_id,
        'emissions_factor': emissions_factor,
        'fuel_use_mix': fuel_use_mix,
        'eui_residential_multiplier': eui_residential_multiplier,
        'eui_commercial_multiplier': eui_commercial_multiplier,
        'source': source,
        'acquisition_date': str(date.today()),
        'valid_start_date': valid_start_date,
        'valid_end_date': valid_end_date,
        'notes': notes
    }
    
    data.append(new_row)
    return data


def add_rows_from_ef(data, ef_dataset):
    ef = pd.read_excel(ef_dataset, sheet_name='Emissions Factors').dropna()[1:]
    ef = ef.rename(columns={'Carbon Dioxide Emissions Coefficients by Fuel': 'Carbon Dioxide (CO2) Factor', 
                                      'Unnamed: 1': "Pounds CO2 (Per Unit of Volume or Mass)",
                                      'Unnamed: 2': 'Kilograms CO2 (Per Unit of Volume or Mass)',
                                      'Unnamed: 3': 'Pounds CO2 Per Million Btu',
                                      'Unnamed: 4': 'Kilograms CO2 Per Million Btu'})
    ef_dict = ef.to_dict('records')
    data = add_row(data,
               'North America', 
               'Continent', 
               ef_dict,
               None,    
               None,
               None,
               'Wikipedia',
               '2000-01-01',
               '2023-01-01',
               'N/A')


def main():
    filename = 'v3output.csv'
    filepath = 'data/'

    df = init_csv(filename, filepath)
    print("hi")
    df = add_rows_from_ef(df, filepath+'Emissions_Factors.xlsx')
    


if __name__=="__main__":
    main()
