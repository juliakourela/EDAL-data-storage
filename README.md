# EDAL-data-storage
A Jupyter Notebook for storage of geospatial emissions and energy usage data in GeoJSON format.

**Dependencies:** pandas, json

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
        "coordinates": [42.3601, 71.0589]
    },
  "properties": {
    "city": "boston",
    "region": "massachusetts",
    "country": "united states",
    "residential_multiplier": 193.84,
    "commercial_multiplier": 190.07,
    "source": "Your Source",
    "date_acquired": "Date",
    "notes": "Additional Notes"}
    }
 ]}
```
