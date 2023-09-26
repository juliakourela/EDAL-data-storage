import geocoder
import json
import requests
import xmltodict


# returns geonames identifier for place name
def get_geonames_id(username, placename):
    geocode = geocoder.geonames(placename, key=username)
    return geocode.geonames_id


# returns list of dictionaries in the form
# {'toponymName': 'United States', 'name': 'United States', 
# 'lat': '39.76', 'lng': '-98.5', 'geonameId': '6252001', 
# 'countryCode': 'US', 'countryName': 'United States', 
# 'fcl': 'A', 'fcode': 'PCLI'}
# from largest region (Earth) to smallest region

def get_request(username, placename):
    id = get_geonames_id(username, placename)
    URL = f"http://api.geonames.org/hierarchy?geonameId={id}&username={username}"
    try:
        response = requests.get(URL, timeout=5) 
    except requests.exceptions.Timeout:
        print("Timed out")
        return []
    decoded_response = response.content.decode('utf-8')
    response_json = json.loads(json.dumps(xmltodict.parse(decoded_response)))
    print(response_json)
    return response_json['geonames']['geoname']


# returns list of place names above the region of interest
# in the hierarchy, from smallest region to largest (continent)

def get_parent_hierarchy(username, placename):
    hierarchy = get_request(username, placename)
    if len(hierarchy) <= 2: # region of interest is a continent, or request timed out
        return []
    elif len(hierarchy) == 3: # region of interest is a nation
        return [hierarchy[1]['name']]
    elif len(hierarchy) == 4: # egion of interest is a subregion
        return [hierarchy[2]['name'], hierarchy[1]['name']]
    else: # region of interest is a municipality
        return [hierarchy[3]['name'], hierarchy[2]['name'], hierarchy[1]['name']]
