#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 22:09:21 2022

@author: jacksondoe-mensah
"""

import pandas as pd

from sodapy import Socrata

import matplotlib.pyplot as plt

import geopandas as gpd

import seaborn as sns

#%%#%% Load nys vehicle registration data

#Define custom token for requesting data 

MyAppToken = "REREg1nOFbFijVX5Q5rvAlPLr"

#Request access to data using my unique app token

request = Socrata("data.ny.gov",
                  MyAppToken,
                  username="jdoemensah@gmail.com",
                  password="Africa2020!")

#Request data, return as JSON from API / convert to Python list of dictionaries by sodapy

results = request.get("w4pv-hbkt", where ="record_type =='VEH'", limit = 100000)

#Save returned data as pandas dataframe

veh = pd.DataFrame.from_records(results)

veh = veh.query("fuel_type =='GAS'")

veh = veh.drop(columns =['vin',
                         'registration_class',
                         'record_type',
                         'state',
                         'model_year',
                         'make',
                         'body_type',
                         'reg_valid_date',
                         'reg_expiration_date',
                         'color',
                         'scofflaw_indicator',
                         'suspension_indicator',
                         'revocation_indicator',
                         'maximum_gross_weight',
                         'passengers'])
                         
#%%#%% CLEAN VEHICLE REGISTRATION DATA for relevant and consistent varibales

# Vehicle Unladen Weight
#Check for missing values, fill NAs, & save variables in appropriate types

veh['unladen_weight'].isnull().value_counts()
#4,160 values missing.

veh['unladen_weight'] = veh['unladen_weight'].astype(float)

#Fill missing values with 0
veh['unladen_weight'].fillna(veh['unladen_weight'].mean(),inplace=True)

#Convert unladen weight to interger
veh['unladen_weight'] = veh['unladen_weight'].astype(float)

#Compute mean weight 

mean_unladen_weight = veh['unladen_weight'].sum()/len(veh['unladen_weight'])

print(mean_unladen_weight)




#%% Clean Vehicle county and zip info.

#ZIP
veh['zip'] = veh['zip'].isnull().value_counts()
#No missing values in zip column

#Convert county and zip to string
veh['zip'] = veh['zip'].astype(str)

#Organize data by county

veh['county'].isnull().value_counts()
#No missing values in county name column

#Convert county to string
veh['county'] = veh['county'].astype(str)

#print(veh['county'].value_counts())
#63 countries reported. Should be 62

#veh_by_county = veh.groupby('county').count()
#print(len(veh_by_county))


#%% Still on cleaning...How much registrations were done by out of state folks?

a = 0
for v in veh['county']:
    if v == 'OUT-OF-STATE':
        a = a + 1
print(a)
# 627 cars registered by folks from out of state


in_state = veh['county'] != 'OUT-OF-STATE'

veh = veh[in_state]

print(len(veh['county'].value_counts()))

                       
#%%Finally, Group car registration by county, and into dataframe

grouped = veh.groupby(['county'])

veh_by_county = grouped.size().to_frame('No_of_Vehicles')

veh_by_county['weight_1/million'] = grouped['unladen_weight'].sum()

veh_by_county['weight_1/million'] = veh_by_county['weight_1/million']/1e6
#veh_by_county = veh.groupby(['county']).size().to_frame('No_of_Vehicles')


#veh_by_county = pd.DataFrame(veh_by_county)


#%% Load nys vehicle miles traveled data 

nys_mt = pd.read_excel("Vehicle_Miles_of_Travel_2017_2018.xlsx")

#ys_mt['FHWA Func Sys'] = nys_mt['FHWA Func Sys'].astype(str)

#nys_mt = nys_mt.query("FHWA Func Sys == '1'")

nys_mt = nys_mt.drop(columns =['UA Code',
                               'NYSDOT Func Class',
                               'FHWA Func Sys',
                               'Urban Area',
                               'Length','Length.1','VMT/1000'])

new_names = {"VMT/1000.1":"VMT/1000","County":"county"}

nys_mt = nys_mt.rename(columns=new_names) 


# Clean VMT values

nys_mt['VMT/1000'].isnull().value_counts()
#No missing values in VMT.

#Convert VMT to interger

nys_mt['VMT/10000']=nys_mt['VMT/1000'].astype(int)

t_counties = nys_mt['county'].value_counts()
print(len(t_counties))
#62 COUNTIES RECORDED. 

#%%Group nys_mt by county to have 62 counties in dataframe

grouped2 = nys_mt.groupby(['county'])

nys_mt_by_county = grouped2.sum()



#%%Merge VEH AND nsy_mt DATA

both =veh_by_county.merge(nys_mt_by_county, 
                 on = "county", 
                 how = "outer",
                 validate = '1:1',
                 indicator =True)

print(both['_merge'].value_counts())

both = both.drop(columns="_merge")

#%%Compute estimate of MPG and GAL without Wood nanomaterials

#Define assumptions for miles per gallon (MPG) and Emission Co-effiecint (EC) 

MPG = 25 #miles per gallon -fuel effcicency -NYDOT

EC = 19.37 #emission coefficient per unit of volume/mass


both['GAL'] = both['VMT/1000']/MPG

both['CO2_1'] = both['GAL'] * (EC * both['weight_1/million'])

      
#%%Compute estimate of MPG and GAL WITH Wood nanomaterials

#define new weight reductions with NANOWOOD COMPOSITES: if nanocomposites use reduced vehicle volume by 60% (caution: big assumption!)

both['weight_2/millions'] = both['weight_1/million']* 0.4


#Define assumptions for miles per gallon (MPG) and Emission Co-effiecint (EC) 

both['GAL'] = both['VMT/1000']/MPG

both['CO2_2'] = both['GAL'] * (EC * both['weight_2/millions'])

#Compute % difference in emissions 

#both['percent_dif'] = (both['CO2_2']-both['CO2_1'])/both['CO2_1']

both.to_csv("both.csv", index=False)




#%% Read and Merge both with county demographic data

geodata = gpd.read_file("cb_2019_us_county_500k_36.zip")

colnames = {"NAME": "county"}
geodata = geodata.rename(columns=colnames)

print(geodata['county'].value_counts())


geodata['county'] = geodata['county'].str.upper()

geodata['county'] = geodata['county'].replace("ST. LAWRENCE", "ST LAWRENCE", regex=True)

all_data = geodata.merge(both,
                        on='county',
                        how='left',
                        validate='1:1',
                        indicator=True)

print( all_data['_merge'].value_counts() )

all_data.drop(columns='_merge',inplace=True)

all_data.reset_index(inplace=True)

all_data.to_file("counties1.gpkg",layer="all_data",index=False)

#%%Plot some visualizations
#create top 10 counties with higest registrations:
top_registrations = both.sort_values(by=['No_of_Vehicles'],ascending=False).iloc[0:10]


#get top emissions
top_emissions = both.sort_values(by=['CO2_1'],ascending=False).iloc[0:10]



#%%Plot top 10 counties with vehicle registration and highest emissions  

top_registrations.reset_index(inplace=True)
top_emissions.reset_index(inplace=True)


#%% plot top ten counties with higest emissions and registrations in business as usual mode
#county_order=list(top_registrations['county'])
fig, (ax1,ax2) = plt.subplots(1,2,dpi=300,figsize=[20,12])
fig.suptitle("Top 10 Vehicle Registrations and CO2 Emissions")
sns.barplot(x='county',y='No_of_Vehicles',data=top_registrations,ax=ax1) #order=
           # ['NASSAU','SUFFOLK','QUEENS','WESTCHESTER','KINGS','ERIE','MUNROE','NEW YORK','RICHMOND','BRONX'])
sns.barplot(x='county',y='CO2_1',data=top_emissions,ax=ax2)
            #['SUFFOLK','NASSAU','QUEENS','WESTCHESTER','ERIE','KINGS','MUNROE','ONONDAGA','NEW YORK','ORANGE'])
ax2.set_xlabel("Counties")
fig.tight_layout()
fig.savefig("top_10.png")

#%%E.N.D