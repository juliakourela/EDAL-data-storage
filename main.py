import pandas as pd
from json_interface import *
from ingest_datasets import *

def main():
    filename = 'testoutput.json'
    data = open_json(filename)

    data = add_features_from_ef(data)
    data = add_features_from_fuel_mix(data)
    data = add_features_from_EUI(data)

    data_to_json(data, filename)
  
  
if __name__=="__main__":
    main()