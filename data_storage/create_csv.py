import pandas as pd
from datetime import date
from os import path
from unidecode import unidecode
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
    #print(data.columns)
    if (data['geonames_id'] == geonames_id).any():
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

    if new_row != None:
        data.loc[len(data.index)] = new_row

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
    return data


def add_rows_from_fuel_mix(data, region_of_interest, fuel_mix_dataset):
    country_fmix = pd.read_excel(fuel_mix_dataset).dropna()[1:]
    country_fmix = country_fmix.rename(columns={'Geographic Area Selection:': 'Residential Non-Electricity Heating Source', 
                                      'Unnamed: 1': "Percentage Of New Total (less 'Other')",
                                      'Unnamed: 2': 'Kg CO2 emissions/ MMBtu',
                                      'Unnamed: 3': 'CO2 Emissions Weighted by Percentage of Fuel Mix',})
    fuel_mix = country_fmix.to_dict('records')
    data = add_row(data,
               region_of_interest, 
               'Country', 
               None,
               fuel_mix,
               None,
               None,
               'Wikipedia',
               '2000-01-01',
               '2023-01-01',
               'N/A')

    return data


def get_country_multipliers_for_csv(country_of_interest, country_specific_euis):
    country_eui = pd.read_excel(country_specific_euis).dropna()
    country_res_multipliers = dict(zip(country_eui['City'], 
                                       country_eui['Energy Use Intensity by End Use (kwh/m2/year)']))
    country_comm_multipliers = dict(zip(country_eui['City'], 
                                        country_eui['Energy Use Intensity by End Use (kwh/m2/year)2']))
    
    return {'Municipalities': list(country_res_multipliers.keys()),
            'Residential Multipliers': country_res_multipliers, 
            'Commercial Multipliers': country_comm_multipliers}


def add_rows_from_EUI(data, region_of_interest, eui_dataset_filename):
    multipliers = get_country_multipliers_for_csv(region_of_interest, 
                                          eui_dataset_filename)
    
    for municipality in multipliers['Municipalities']:
        plaintext_municipality = unidecode(municipality)
        data = add_row(data,
                plaintext_municipality, 
               'Municipality', 
               None,
               None,
               multipliers['Residential Multipliers'][municipality],
               multipliers['Commercial Multipliers'][municipality],
               'Wikipedia',
               '2000-01-01',
               '2023-01-01',
               'N/A')
        
    return data


def main():
    filename = 'v3output.csv'
    filepath = 'data/'

    df = init_csv(filename, filepath)
    print(df)
    df = add_rows_from_ef(df, filepath+'Emissions_Factors.xlsx')
    df = add_rows_from_fuel_mix(df, 'Mexico', filepath+'MX_Fuel_Mixes.xlsx')
    df = add_rows_from_fuel_mix(df, 'Indonesia', filepath+'ID_Fuel_Mixes.xlsx')
    #df = add_rows_from_EUI(df, 'Mexico', filepath+'MX_EUI_CURB_estimates.xlsx')
    #df = add_rows_from_EUI(df, 'Indonesia', filepath+'ID_EUI_CURB_estimates.xlsx')

    df.to_csv(filename)
    


if __name__=="__main__":
    main()
