# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 21:09:57 2020

@author: Anirudh Raghavan
"""

# Feature Transformation

##############################################################################

# Input: Ticker Filtered Raw Data

# Output: Tranformed Features Data

##############################################################################

# In the earlier script we cleaned the rows of our data by removing the
# rows that were not required

# Now, we analyze the features of our dataset.

# Our objective is to predict stock price movement based on the quarterly 
# financial information. However, it is important to note that rather than
# the financial information as such the change in the values would be a better
# predictor of share price movement.

# Hence, we shall build a dataset where the features shall be the percentage 
# change in the financial feature. Eg: Change in Profit or Change in Earnings
# per share

###############################################################################

# Code

import pandas as pd
import numpy as np

features = pd.read_csv("Tech_data_tickFilt.csv")

features.info()

# Data Cleaning

# We shall first clean the dataset before proceeding with the transformation

# We shall remove features which have NAs and 0s greater than 10%. As these 
# features do not provide us sufficient information to create a model

##############################################################################

features = features.dropna(thresh = features.shape[0]*0.1, axis=1)

for name in features.columns:
    print(name)
    if sum(features[name] == 0) >= features.shape[0]*0.1:
        print("yes")
        features = features.drop([name], axis=1)

#############################################################################

# Cells with 0s and NAs become an issue doing our transformation. We shall
# first summarize the percentage of 0s in each columns to obtain a better 
# picture

features_info = {}
for name in features.columns:
    
    total = sum(features[name] == 0)
    
    features_info[name] = total/features.shape[0]

features_info = {}

# We will place a nan wherever 0s come up in our transformation and we shall 
# impute the average later on while preprocessing our data for model building

##############################################################################

# First create an empty dataframe for our transformed data

columns_names = list(features.columns[20:142])

columns_names.append("Index")

series_features = pd.DataFrame(columns = columns_names)

###############################################################################

# Data Transformation

# In order to create our transformed dataset we would need to ensure the 
# following:
    
# To find the change in the information, the rows should be consecutive in 
# in terms of year and quarter and should follow the same Ticker. Otherwise,
# they cannot be compared to form a transformed dataset and will thus be ignored

#########################################################################

N = features.shape[0]

for i in range(N):
    if i == 0:
        Ticker = "None"
    if features.iloc[i,9] != Ticker:
        prev_year =  features.iloc[i,15]
        prev_quart = features.iloc[i,16]
        Ticker = features.iloc[i,9]
    
    else:
        if features.iloc[i,15] == prev_year:
            if features.iloc[i,16] == prev_quart + 1:
                
                diff_array = []
                for j in range(20,96):
                    prev_item = features.iloc[i-1,j]
                    curr_item = features.iloc[i,j]
                        
                    if curr_item - prev_item == 0:
                        diff_item = 0
                    elif prev_item == 0:
                        diff_item = np.nan
                    else:
                        diff_item = (curr_item - prev_item)/prev_item
                        
                    diff_array.append(diff_item)
                    
                diff_array.append(Ticker + str(prev_year) + str(prev_quart))
                    
                prev_year =  features.iloc[i,15]
                prev_quart = features.iloc[i,16]
                
                row_feat = {}
                for k in range(len(diff_array)):
                    row_feat[series_features.columns[k]] = diff_array[k]
    
                series_features = series_features.append(row_feat, ignore_index = True)
    
                    
            else:
                prev_year =  features.iloc[i,15]
                prev_quart = features.iloc[i,16]
            
        else:
            if features.iloc[i,15] == prev_year + 1 and features.iloc[i-1,16] == 4 and features.iloc[i,16] == 1:
                
                diff_array = []
                for j in range(20,96):
                    prev_item = features.iloc[i-1,j]
                    curr_item = features.iloc[i,j]
                        
                    if curr_item - prev_item == 0:
                        diff_item = 0
                    elif prev_item == 0:
                        diff_item = np.nan
                    else:
                        diff_item = (curr_item - prev_item)/prev_item
                        
                    diff_array.append(diff_item)
                    
                diff_array.append(Ticker + str(prev_year) + str(prev_quart))
                    
                prev_year =  features.iloc[i,15]
                prev_quart = features.iloc[i,16]
                
                row_feat = {}
                for k in range(len(diff_array)):
                    row_feat[series_features.columns[k]] = diff_array[k]
    
                series_features = series_features.append(row_feat, ignore_index = True)
    
                
            else:
                prev_year =  features.iloc[i,15]
                prev_quart = features.iloc[i,16]
                
    
    print(Ticker, features.iloc[i,15],features.iloc[i,16])

##############################################################################

series_features.to_csv("sec_feat_transformed.csv", index = False)



