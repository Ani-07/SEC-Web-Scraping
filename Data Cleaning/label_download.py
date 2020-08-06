# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:36:18 2020

@author: Anirudh Raghavan
"""

# Downloading Prices

##############################################################################

# Input: Ticker Filtered Raw Data

# Output: Labels for 3 different periods of price movements

##############################################################################

# We will use a similar filtering technique as with the feature transformation
# script to identify the consecutive quarters of data

# We will take the filing date of the later quarter and use Yahoo Finance to 
# obtain the stock prices on that date and the next 4 days

##############################################################################

# Code

from pandas_datareader import data
import pandas as pd
from datetime import datetime,timedelta
from time import sleep

data_1  = pd.read_csv("Tech_data_tickFilt.csv")

features = pd.DataFrame()

features["Ticker"] = data_1.iloc[:,9]
features["Year"] = data_1.iloc[:,15]
features["Quarter"] = data_1.iloc[:,16]
features["Filing Date"] = data_1.iloc[:,18]

features = features[features["Ticker"] != "CMVT"]

features = features[features["Ticker"] != "CYNK"]

features = features.drop(list(range(1925,1926)))

features = features.drop(list(range(4783,4786)))

#############################################################################

# We first create an empty dataframe to store our output

labels_data = pd.DataFrame(columns = ["Ticker", "Year", "Quart", "1-Day", 
                                      "2-Day", "4-Day"])

##############################################################################

N = features.shape[0]

for i in range(N):
        
    sleep(1)
        
    if i == 0:
        Ticker = "None"
    if features.iloc[i,0] != Ticker:
        prev_year =  features.iloc[i,1]
        prev_quart = features.iloc[i,2]
        Ticker = features.iloc[i,0]
        
    else:
        if features.iloc[i,1] == prev_year:
            if features.iloc[i,2] == prev_quart + 1:
    
                start = features.iloc[i,3]
                start = datetime.strptime(start, '%m/%d/%Y')
                start = start.date()
                    
                days_before = (start+timedelta(days=35)).isoformat()
                end = datetime.date(datetime.strptime(days_before, '%Y-%m-%d'))
                price = data.DataReader(Ticker, "yahoo", start, end).iloc[:,3]
    
                one_change = (price.iloc[1] - price.iloc[0])/price.iloc[0]
                two_change = (price.iloc[2] - price.iloc[0])/price.iloc[0]
                four_change = (price.iloc[4] - price.iloc[0])/price.iloc[0]
                    
                prev_year =  features.iloc[i,1]
                prev_quart = features.iloc[i,2]
                    
                labels_data = labels_data.append({"Ticker": Ticker, "Year": prev_year, 
                                                  "Quart": prev_quart, "1-Day": one_change, 
                                                  "2-Day": two_change, "4-Day": four_change }, 
                                                 ignore_index = True)
       
                        
            else:
                prev_year =  features.iloc[i,1]
                prev_quart = features.iloc[i,2]
                
        else:
            if features.iloc[i,1] == prev_year + 1 and features.iloc[i-1,2] == 4 and features.iloc[i,2] == 1:
                    
                start = features.iloc[i,3]
                start = datetime.strptime(start, '%m/%d/%Y')
                start = start.date()
                    
                days_before = (start+timedelta(days=35)).isoformat()
                end = datetime.date(datetime.strptime(days_before, '%Y-%m-%d'))
                price = data.DataReader(Ticker, "yahoo", start, end).iloc[:,3]
                    
                one_change = (price.iloc[1] - price.iloc[0])/price.iloc[0]
                two_change = (price.iloc[2] - price.iloc[0])/price.iloc[0]
                four_change = (price.iloc[4] - price.iloc[0])/price.iloc[0]
                    
                prev_year =  features.iloc[i,1]
                prev_quart = features.iloc[i,2]
                    
                labels_data = labels_data.append({"Ticker": Ticker, "Year": prev_year, 
                                                      "Quart": prev_quart, "1-Day": one_change, 
                                                      "2-Day": two_change, "4-Day": four_change }, 
                                                     ignore_index = True)
       
            else:
                prev_year =  features.iloc[i,1]
                prev_quart = features.iloc[i,2]
                    
            
        if i%100 == 0:
            sleep(100)
                    
        
    print(Ticker, features.iloc[i,1],features.iloc[i,2],i)

##############################################################################

labels_data.to_csv("tech_price_data.csv", index = False)


