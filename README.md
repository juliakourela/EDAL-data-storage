# EDAL-data-storage
Storage for geospatial emissions and energy usage data.

**Dependencies:** pandas, json, geopy

**Validation Data Format:**

| Property | Description |
| ------------- | ------------- |
| name  | Textual descriptor of municipality (string) |
| country  | Textual descriptor of country (string) |
| region  | Textual descriptor of region/state/province (string) |
| geoname  | GeoNames ID (int) |
| year  | Multiplier used in determining Energy Use Intensity (EUI) factors for commercial areas in region (float) |
| boundary  | Type of area (string) |
| population  | Population of municipality (int) |
| climate  | Climate of municipality (string) |
| latitude  | Latitude of municipality (float) |
| longitude  | Longitude of municipality (float) |
| CATEGORY-fuel_or_activity_type  | Total CO2 emissions produced by a given fuel or activitity type in a given category (float) |
| COMBINED-NON-RESIDENTIAL-fuel_or_activity_type  | Sum of total CO2 emissions produced by a given fuel or activitity type in the Commercial & Institutional categories (float) |
| CATEGORY-total_direct  | Sum ofotal CO2 emissions produced by all direct emissions sources in a given category (float) |
| CATEGORY-total_indirect  | Sum of total CO2 emissions produced by all indirect emissions sources in a given category |
| COMBINED-NON-RESIDENTIAL-total_direct  | Sum of total CO2 emissions produced by all direct emissions in the Commercial & Institutional categories (float) |
| COMBINED-NON-RESIDENTIAL-total_indirect  | Sum of total CO2 emissions produced by all indirect emissions in the Commercial & Institutional categories (float) |

**Direct emissions sources:** coal, diesel, kerosene, lpg, natural_gas, res_fuel_oil 

**Indirect emissions sources:** district_heating, electricity, wood

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
