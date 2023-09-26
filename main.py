import pandas as pd
from libs.json_interface import *
from libs.ingest_datasets import *



def main():
    filename = 'output.json'
    filepath = 'data/'

    data = open_json(filename)

    data = add_features_from_ef(data, filepath+'Emissions_Factors.xlsx')

    data = add_features_from_fuel_mix(data, 'Mexico', filepath+'MX_Fuel_Mixes.xlsx')
    data = add_features_from_fuel_mix(data, 'Indonesia', filepath+'ID_Fuel_Mixes.xlsx')

    data = add_features_from_EUI(data, 'Mexico', filepath+'MX_EUI_CURB_estimates.xlsx')
    data = add_features_from_EUI(data, 'Indonesia', filepath+'ID_EUI_CURB_estimates.xlsx')
    
    data_to_json(data, filename)
  
  
if __name__=="__main__":
    main()
