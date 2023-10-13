# EDAL-data-storage
Storage for geospatial emissions and energy usage data.



# Validation Data Format

**Dependencies:** pandas

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

# Data Storage Format

**Dependencies:** pandas, unidecode, geopy, xmltodict

| Property | Description |
| ------------- | ------------- |
| name  | Textual descriptor of region (string) |
| feature_type  | Type of region: continent, country, subregion, or municipality (string) |
| geonames_id  | GeoNames ID (int) |
| emissions_factor  | Multiplier used in determining Energy Use Intensity (EUI) factors for commercial areas in region (float) |
| fuel_use_mix  | Fuel use mix of region (string) |
| eui_residential_multiplier  | Residential energy use intensity multiplier of region (float) |
| eui_commercial_multiplier  | Commercial energy use intensity multiplier of region (float) |
| source  | Source of data (string) |
| acquisition_date  | Data data acquired (MM-DD-YYYY) |
| valid_start_date  | First date data is valid for (MM-DD-YYYY) |
| valid_end_date  | Final date data is valid for (MM-DD-YYYY) |
| notes  | Additional notes on entry (string) |

