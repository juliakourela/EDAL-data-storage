import pandas as pd
from create_feature_collection import *
from unidecode import unidecode

country_of_interest = 'Mexico'
country_specific_eui_dataset = 'MX_EUI_CURB_estimates.xlsx'
ef_dataset = 'Fuel_Mixes.xlsx'
fuel_mix_dataset = 'Fuel_Mixes.xlsx'


# returns {'Municipalities': list of municipality names,
#          'Residential': dict of {'Municipality': Multiplier}, 
#          'Commercial': dict of {'Municipality': Multiplier}}
def get_country_multipliers(country_of_interest, country_specific_euis):
    country_eui = pd.read_excel(country_specific_euis).dropna()

    country_res_multipliers = dict(zip(country_eui['City'], 
                                       country_eui['Energy Use Intensity by End Use (kwh/m2/year)']))
    country_comm_multipliers = dict(zip(country_eui['City'], 
                                        country_eui['Energy Use Intensity by End Use (kwh/m2/year)2']))
    
    return {'Municipalities': list(country_res_multipliers.keys()),
            'Residential Multipliers': country_res_multipliers, 
            'Commercial Multipliers': country_comm_multipliers}


def add_features_from_EUI(data):
    multipliers = get_country_multipliers(country_of_interest, 
                                          country_specific_eui_dataset)
    
    for municipality in multipliers['Municipalities']:
        plaintext_municipality = unidecode(municipality)
        print(plaintext_municipality)
        feature = create_feature(plaintext_municipality, 
               'Municipality', 
               None,
               None,
               multipliers['Residential Multipliers'][municipality],
               multipliers['Commercial Multipliers'][municipality],
               'Wikipedia',
               '2000-01-01',
               '2023-01-01',
               'N/A')
        if feature != None:
            data.append(feature)
    
    return data


def ingest_emissions_factors():
    ef = pd.read_excel(ef_dataset, sheet_name='Emissions Factors').dropna()[1:]
    ef = ef.rename(columns={'Carbon Dioxide Emissions Coefficients by Fuel': 'Carbon Dioxide (CO2) Factor', 
                                      'Unnamed: 1': "Pounds CO2 (Per Unit of Volume or Mass)",
                                      'Unnamed: 2': 'Kilograms CO2 (Per Unit of Volume or Mass)',
                                      'Unnamed: 3': 'Pounds CO2 Per Million Btu',
                                      'Unnamed: 4': 'Kilograms CO2 Per Million Btu'})
    ef_dict = ef.to_dict('records')
    return(ef_dict)


def add_features_from_ef(data):
    ef = ingest_emissions_factors()
    feature = create_feature('North America', 
               'Continent', 
               ef,
               None,
               None,
               None,
               'Wikipedia',
               '2000-01-01',
               '2023-01-01',
               'N/A')
        
    if feature != None:
        data.append(feature)

    return data


def ingest_fuel_mixes(country_of_interest):
    country_fmix = pd.read_excel(fuel_mix_dataset).dropna()[1:]
    country_fmix = country_fmix.rename(columns={'Geographic Area Selection:': 'Residential Non-Electricity Heating Source', 
                                      'Unnamed: 1': "Percentage Of New Total (less 'Other')",
                                      'Unnamed: 2': 'Kg CO2 emissions/ MMBtu',
                                      'Unnamed: 3': 'CO2 Emissions Weighted by Percentage of Fuel Mix',})
    fuel_dict = country_fmix.to_dict('records')
    return fuel_dict


def add_features_from_fuel_mix(data):
    fuel_mix = ingest_fuel_mixes(country_of_interest)
    feature = create_feature(country_of_interest, 
               'Country', 
               None,
               fuel_mix,
               None,
               None,
               'Wikipedia',
               '2000-01-01',
               '2023-01-01',
               'N/A')

    if feature != None:
        data.append(feature)

    return data
