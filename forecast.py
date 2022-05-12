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