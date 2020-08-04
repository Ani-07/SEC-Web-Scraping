# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:07:18 2020

@author: Anirudh Raghavan
"""

# Data Cleaning

##############################################################################
# Summary

# Input: Raw Data from WRDS

# Output: Filtered Data with the required stocks 

##############################################################################

# Being a pilot project, we downloaded data dump of stocks from the technology 
# sector from WRDS

# However, many of the stocks may be penny stocks with very low prices, so we 
# will first try to identify those stocks and remove the respective data

# Further, we shall be using the Yahoo Finance to obtain stock prices data. I 
# shall try to do a test run of a the ticker names and remove those tickers 
# with no stock prices

##############################################################################

# Code

from pandas_datareader import data
import pandas as pd
from datetime import datetime,timedelta

features = pd.read_csv("Tech companies_data.csv")

##############################################################################

# Manually Identified Data

features = features.drop(list(range(68,105)))

features = features.drop(list(range(354,394))) #TT Removal

features = features.drop(list(range(394,431))) #IDTI Removal

features = features.drop(list(range(1082,1111))) #IDTI Removal

features = features.drop(list(range(1230,1243))) #UNDT Removal

features = features.drop(list(range(1355,1371))) #MMTC Removal

features = features.drop(list(range(1543,1553))) #EMIS Removal

features = features.drop(list(range(1553,1580))) #BFYT Removal

features = features.drop(list(range(1585,1600))) #LBDT Removal

features = features.drop(list(range(1600,1610))) 

features = features.drop(list(range(1658,1671))) 

features = features.drop(list(range(1775,1780))) 

features = features.drop(list(range(1892,1894))) 

features = features.drop(list(range(2206,2212))) 

features = features.drop(list(range(2532,2541))) 

features = features.drop(list(range(3298,3303))) 

features = features.drop(list(range(3426,3460))) 

features = features.drop(list(range(5678,5679))) 

features = features.drop(list(range(6212,6220))) 

features = features.drop(list(range(7081,7086))) 

features = features.drop(list(range(7212,7222))) 

features = features.drop(list(range(7458,7460))) 

features = features.drop(list(range(7502,7510)))


############################################################################

#Identify stocks with average stock prices of < USD 1 and remove them

unq_tick = list(set(features["Ticker Symbol"]))

avg_tick = {}
copy = {}
for Ticker in unq_tick:
    
    currentdate = datetime.date(datetime.now())
    days_before = (currentdate-timedelta(days=720)).isoformat()
    prevdate = datetime.date(datetime.strptime(days_before, '%Y-%m-%d'))
    
    try:
        price = data.DataReader(Ticker, "yahoo", prevdate, currentdate).iloc[:,3]
        avg_price = sum(price)/len(price)
    
    except:
        print(Ticker)
        avg_price = 100
    
    avg_tick[Ticker] = avg_price
    copy[Ticker] = avg_price



for tick in copy.keys():
    if copy[tick] >= 1:
        del avg_tick[tick]

for ticker in avg_tick.keys():
    features = features[features["Ticker Symbol"] != ticker]

                        
############################################################################

remove_list = ["RTKHQ", "KTEC", "KULR","EXAC", "EDGW", "XPLR", "SOYL", "XRM", "MYOS"]

for ticker in remove_list:
    features = features[features["Ticker Symbol"] != ticker]

##############################################################################


# We will now save our filtered output data

features.to_csv("Tech_data_tickFilt.csv", index = False)
