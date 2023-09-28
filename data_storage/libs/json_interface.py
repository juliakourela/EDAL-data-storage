import json
from os import path


# opens JSON of interest
def open_json(filename):

    if path.isfile(filename) is False:
        create_new_json(filename)
    
    with open(filename) as fp:
        data = json.load(fp)
    
    return data


# creates new empty JSON
def create_new_json(filename):
    dictionary = []
    with open(filename, "w") as outfile:
        json.dump(dictionary, outfile)


# returns data to output JSON file
def data_to_json(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)
