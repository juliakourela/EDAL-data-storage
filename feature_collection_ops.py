import pandas as pd
from datetime import date
from geonames_interface import *


def create_feature(data, name, feature_type,
                   emissions_factor, fuel_use_mix, 
                   eui_residential_multiplier, 
                   eui_commercial_multiplier, source, 
                   valid_start_date, valid_end_date, notes):
    
    geonames_id = get_geonames_id('juliakourela', name)
    if geonames_id == None:
        return
    parent_hierarchy = get_parent_hierarchy('juliakourela', name)
    
    the_feature = {
        'name': name,
        'feature_type': feature_type,
        'parent_hierarchy': parent_hierarchy, 
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
    
    # if field is null,
    # check parent hierarchy for field of interest
    for field in the_feature.keys():
        if the_feature[field] == None:
            the_feature[field] = parent_hierarchy_search(data, the_feature, field)

    return the_feature


# iterates through hierarchy of parent regions
# returns field value if a parent's entry 
# contains such value; otherwise returns None
def parent_hierarchy_search(data, child_feature, field):

    parent_hierarchy = child_feature['parent_hierarchy']

    for x in range(len(parent_hierarchy)):
        parent = parent_hierarchy[x]
        print(parent)
        filtered_data = list(filter(lambda entry: 
                                    entry['name'] == parent, data))
        if len(filtered_data) != 0:
            if filtered_data[0][field] != None:
                return filtered_data[0][field]
        
    return None


# and entry['feature_type'] == feature_types[child_feature_index + x - 1]
#feature_types = ['Municipality', 'Subregion', 'Country', 'Continent']
# child_feature_index = feature_types.index(child_feature['feature_type'])