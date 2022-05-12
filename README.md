# Forecasting Carbon Benefits/Demand for Wood Nanomaterials in Electric Vehicles 
Forecasts carbon benefits and demand for wood-based nano materials as bio fillers in automotive composite applications 

# Background
Wood and natural fiber-based nanomaterials have gained considerable attention as promising alternatives to pretroluem-derived products in automotive applications. Wood-based nanomaterials are abundant, readily available and exhibit high strength properties as bio-based fillers in composites. Adoption of new materials and technology in the automotive industry is challenging. While techincal factors such as product property, market demand and profitability are important for adoptability, information on product sustainability and environmental stewardship has also become critical. Here, U.S. vehicle use and emissions data is used to forecast carbon benefits and demand of wood-based nanomaterials as sustainable alternatives in automobile application.

![image](https://user-images.githubusercontent.com/97989922/164337724-873c5ae2-a008-490c-ad0a-68feb9a8b4ca.jpeg)

Link to image source/article: 
https://www.bioplasticsmagazine.com/en/news/meldungen/20160411-BASF-binder-makes-all-natural-fiber-roof-frame-possible.php

![image](https://user-images.githubusercontent.com/97989922/164337847-660d7ed7-134f-4f8f-ba2c-a083354b1e57.png)

Link to Powerpoint Presentation:

# Repository Contents
This repository contains the foollowing:
1. Input files folder which contains raw and uncleaned data. 
    1.1 _Vehicle_Miles_of_Travel_2017_2018.xlsx_ : an axcell database of vehicle miles traveled in New York State by county
    1.2 _cb_2019_us_county_500k_36.zip_ " a zip shapefile of New York State counties
2. A python script(forecast.py) which cleans data, runs analysis and generate output files. 
3. An output folder which contains cleaned data and result outputs
    3.1 _both.csv_ : clean data which is a merged data on vehicle registrations and vehicle miles travelled by county
    3.2 _counties.gpkg_ :geopackage file with vehicle registration and miles travelled and shapefile for each county
    3.3 _top_10.png_ : barplot of top ten vehicle registrations and CO2 emissions by county 
    3.4 _vehicles_by_county_ : heatmap of vehilce registrations by county
    3.5 _CO2_1_ : Heatmap of carbon emissons by county
    3.6._CO2_2_ : Heatmap of carbon emissons by county at 60% volume reduction (assumped from natural fiber composites ultimum use)



# How to Use This Repository
1. Download appropriate data from web.
2. Clone and run python script (forecast.py) to generate outputs
3. Refer to appropriate literature to interprete output results

# Vehicle Registrations and Emissions Analysis

# The US national MPG average of 25 milesper gallon was used as baseline for this analysis.
Additionally, the CO2 federal emissions constant of EC = 19.37 per unit of volume/mass of vehicle was used to estimate Co2 emissions base on reported vehicle's unladen weight and volume for counties in New York State. 
IMPORTANT: These results are based on only 100,000 queried "gas" "VEH" vehciles as classified by the NY DMV in New York State as at 05/11/2022. This will be expanded to capture true results for gasoline vehiles in all 12.4 Million vehicle registrations reported in New York State in April, 2022.


# Findings
Top Ten Vehicle Registrations and CO2 Emissions by county in NYS
As shown in the figure below, the results show that out of the queried 100,000 gasoline vehicles queried in New York State, Nassau county recorded the higest vehicle registrations. Bronx county had the 10th higehst vehicle registrations. On emissions however, Suffulk county recorded highest with Orange county in the 10th highest C02 emissions based on this estimates. It is also noteworthy that Onondaga county was not among the top vehicle registrations in the state but is among the top ten counties with higest emissions. 
![image](https://user-images.githubusercontent.com/97989922/167980046-b7999b1f-22ec-44d3-b8a0-1e99f8f84e3e.png)

Heatmap of Emission by County
QGIS was used to create a heatmap of vehicle registrations and CO2 emissions by county. this was possible by merging vehicles miles travelled data and vehilce registrations data onto NYS county shapefiles. Using a heatmap of 5 classes, the heatmap trends look similar for both registations and emissions.
![CO2_1](https://user-images.githubusercontent.com/97989922/167983461-4083c443-e4ae-4046-be2b-3eb457c2039d.png)

# Future Work

1. Extend query to account for all gasoline "VEH" veicles in all 12.4 million vehicle registrations in New York State.
2. Reduce C02 emission estimate assumptions by including more parameters to make better estimates

# Data Sources

Vehicle Registrations in NYS: 
https://data.ny.gov/Transportation/Vehicle-Snowmobile-and-Boat-Registrations/w4pv-hbkt 

Vehicle Miles Traveled in NYS (NYS Department of Transportation): 
https://www.dot.ny.gov/divisions/engineering/technical-services/hds-respository

C02 Emissions Coefficients (US Energy Information Administration): 
https://www.eia.gov/environment/emissions/co2_vol_mass.php
