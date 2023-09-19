# EDAL-data-storage
A Jupyter Notebook for storage of geospatial emissions and energy usage data in GeoJSON format.

**Dependencies:** pandas, json, geopy

**Properties:**

| Property | Description |
| ------------- | ------------- |
| city  | Textual descriptor of city (string) |
| region  | Textual descriptor of region/state/province (string) |
| country  | Textual descriptor of country (string) |
| residential_multiplier  | Multiplier used in determining Energy Use Intensity (EUI) factors for residential areas in region (float) |
| commercial_multiplier  | Multiplier used in determining Energy Use Intensity (EUI) factors for commercial areas in region (float) |
| source  | Source from which data was acquired (string) |
| date_acquired  | Date data was acquired (MM-DD-YYYY) (string) |
| notes  | Additional notes regarding the data (string) |

**Sample format:**
```
{ "type": "FeatureCollection", 
  "features": [
    { "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [21.1619, 86.8515]
    },
  "properties": {
    "city": "Cancun",
    "region": "Quintana Roo",
    "country": "Mexico",
    "residential_multiplier": 12.03125,
    "commercial_multiplier": 6.94361,
    "source": "Your Source",
    "date_acquired": "Date",
    "notes": "Additional Notes"}
    }
 ]}
```

**Sample output:**

![mxgeojson](https://github.com/juliakourela/EDAL-data-storage/assets/89415089/21218cf5-b702-4afc-8685-dbe15aa7ee55)
