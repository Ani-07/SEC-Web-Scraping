# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 21:09:57 2020

@author: Anirudh Raghavan
"""

import pandas as pd
import numpy as np

features = pd.read_csv("Tech companies_data.csv")

features = features.drop(list(range(68,105)))

features.info()

features = features.dropna(thresh = features.shape[0]*0.1, axis=1)

for name in features.columns:
    print(name)
    if sum(features[name] == 0) >= features.shape[0]*0.1:
        print("yes")
        features = features.drop([name], axis=1)


features_info = {}
for name in features.columns:
    
    total = sum(features[name] == 0)
    
    features_info[name] = total/features.shape[0]


#################################################################################

N = features.shape[0]

columns_names = list(features.columns[20:96])

columns_names.append("Index")

series_features = pd.DataFrame(columns = columns_names)

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


