# EDAL-data-storage
A Jupyter Notebook for storage of geospatial emissions and energy usage data in GeoJSON form.

**Dependencies:** pandas, json

**Properties:**

| Property | Description |
| ------------- | ------------- |
| region  | Textual descriptor of region (string) |
| Residential_Multiplier  | Multiplier used in determining Energy Use Intensity (EUI) factors for residential areas in region (float) |
| Commercial_Multiplier  | Multiplier used in determining Energy Use Intensity (EUI) factors for commercial areas in region (float) |
| Source  | Source from which data was acquired (string) |
| Acquisition_Date  | Date data was acquired (MM-DD-YYYY) (string) |
| Notes  | Additional notes regarding the data (string) |

**Sample format:**
```
{ "type": "FeatureCollection", 
  "features": [
    { "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]]
    },
  "properties": {
    "region": "massachusetts",
    "Residential_Multiplier": 193.84,
    "Commercial_Multiplier": 190.07,
    "Source": "Your Source",
    "Acquisition_Date": "Date",
    "Notes": "Additional Notes"}
    }
 ]}
```
