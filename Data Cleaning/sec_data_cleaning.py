# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:50:04 2020

@author: Anirudh Raghavan
"""

import numpy as np
import pandas as pd

# Description of data

sec_data = pd.read_csv("sec_fin_info_data.csv")

# First understand the dimensions of the data

sec_data.shape

# We have 8158 rows and 395 columns, let us take a look at the column names

sec_data.columns


sec_data["index"] = sec_data["ticker"] + sec_data["Year"].astype(str) + sec_data["Quarter"].astype(str)

# Now we will remove the first 3 columns

sec_data = sec_data.drop(['ticker', 'Year', 'Quarter'], axis=1)

sec_data = sec_data.drop(['Web URL', 'Active/Inactive Status Marker'], axis=1)

# Now we shall remove the columns which have more than 30% NA rows

sec_data = sec_data.dropna(thresh = sec_data.shape[0]*0.5, axis=1)

for name in sec_data.columns[8:163]:
    print(name)
    if sum(sec_data[name] == 0) >= sec_data.shape[0]*0.5:
        print("yes")
        sec_data = sec_data.drop([name], axis=1)

col_type = [str(sec_data[sec_data.columns[i]].dtype) for i in range(sec_data.shape[1]-1)]

all(i == "float64" for i in col_type)

# Thus other than the index column, all columns are numerical

for name in sec_data.columns[8:sec_data.shape[1]-1]:
    sec_data[name] = sec_data[name].replace(np.nan,sec_data[name].mean())

# We shall now go ahead with normalization

def normalize_data (x, max_x, min_x):
    temp = (x - min_x)/(max_x-min_x)
    return temp

# We then write a for loop to go through each column and then use apply on the each column to 
# compute normalized values and these are then replaced in the column   

for name in sec_data.columns[8:105]:
    print(name)
    sec_data[name] = sec_data[name].apply(normalize_data, args = (max(sec_data[name]), min(sec_data[name])))

sec_1 = [105] + list(range(8,105)) + [1]
sec_2 = [105] + list(range(8,105)) + [2]
sec_4 = [105] + list(range(8,105)) + [4]
sec_6 = [105] + list(range(8,105)) + [6]

sec_data_1 = sec_data.iloc[:,sec_1]
sec_data_2 = sec_data.iloc[:,sec_2]
sec_data_4 = sec_data.iloc[:,sec_4]
sec_data_6 = sec_data.iloc[:,sec_6]

sec_data.to_csv("sec_fin_cleaned.csv")
sec_data_1.to_csv("sec_fin_1.csv")
sec_data_2.to_csv("sec_fin_2.csv")
sec_data_4.to_csv("sec_fin_4.csv")
sec_data_6.to_csv("sec_fin_6.csv")



