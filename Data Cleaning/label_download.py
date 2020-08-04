# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:36:18 2020

@author: Anirudh Raghavan
"""

from pandas_datareader import data
import pandas as pd
import numpy as np
from datetime import datetime,timedelta

from time import sleep

data_1 = pd.read_csv("Tech companies_data.csv")

features = pd.DataFrame()

features["Ticker"] = data_1.iloc[:,9]
features["Year"] = data_1.iloc[:,15]
features["Quarter"] = data_1.iloc[:,16]
features["Filing Date"] = data_1.iloc[:,18]

features = features.drop(list(range(68,105)))

features = features.drop(list(range(354,394))) #TT Removal

features = features.drop(list(range(394,431))) #IDTI Removal

features = features.drop(list(range(1082,1111))) #IDTI Removal

features = features.drop(list(range(1230,1243))) #UNDT Removal

features = features.drop(list(range(1355,1371))) #MMTC Removal

features = features.drop(list(range(1543,1553))) #EMIS Removal

features = features.drop(list(range(1553,1580))) #BFYT Removal

features = features.drop(list(range(1585,1600))) #LBDT Removal

features = features.drop(list(range(1600,1610))) #LBDT Removal

features = features.drop(list(range(1658,1671))) #LBDT Removal

features = features.drop(list(range(1775,1780))) #LBDT Removal

features = features.drop(list(range(1892,1894))) #LBDT Removal

features = features.drop(list(range(2206,2212))) #LBDT Removal

features = features.drop(list(range(2532,2541))) #LBDT Removal

features = features.drop(list(range(3298,3303))) #LBDT Removal

features = features.drop(list(range(3426,3460))) #LBDT Removal

features = features.drop(list(range(5678,5679))) #LBDT Removal

features = features.drop(list(range(6212,6220))) #LBDT Removal

features = features.drop(list(range(7081,7086))) #LBDT Removal

features = features.drop(list(range(7212,7222))) #LBDT Removal

features = features.drop(list(range(7458,7460))) #LBDT Removal

features = features.drop(list(range(7502,7510))) #LBDT Removal


############################################################################

unq_tick = list(set(features["Ticker"]))

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

#################################################################################


for ticker in avg_tick.keys():
    features = features[features.Ticker != ticker]
    
features = features[features.Ticker != "RTKHQ"]

features = features[features.Ticker != "KTEC"]

features = features[features.Ticker != "KULR"]

features = features[features.Ticker != "EXAC"]

features = features[features.Ticker != "EDGW"]

features = features[features.Ticker != "XPLR"]

features = features[features.Ticker != "SOYL"]

features = features[features.Ticker != "XRM"]

features = features[features.Ticker != "MYOS"]

labels_data = pd.DataFrame(columns = ["Ticker", "Year", "Quart", "1-Day", "2-Day", "4-Day"])


N = features.shape[0]


    for i in range(4963,N):
        
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




