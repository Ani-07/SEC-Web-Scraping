# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 00:08:18 2020

@author: Anirudh Raghavan
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from SEC_Doc_Info_Scraping import doc_info

# We shall use this script to track and extract financial Information

with open('aapl_links.json') as json_file:
    aapl_links = json.load(json_file)

df_finance_info = pd.read_csv('Financial_Info.csv', index_col = False)

print(df_finance_info.columns[-1])

print(aapl_links[3]['file_date'])

aapl = aapl_links[3]['links']

result = doc_info(aapl)
    
df_finance_info[result[1]] = result[0]
  
df_finance_info.to_csv('Financial_Info.csv', index = False)
