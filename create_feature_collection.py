import pandas as pd
from datetime import date
from geonames_interface import *


def create_feature(name, feature_type,
                   emissions_factor, fuel_use_mix, 
                   eui_residential_multiplier, 
                   eui_commercial_multiplier, source, 
                   valid_start_date, valid_end_date, notes):
    
    geonames_id = get_geonames_id('juliakourela', name)
    if geonames_id == None:
        return
    parent_hierarchy = get_parent_hierarchy('juliakourela', name)
    
    return {
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