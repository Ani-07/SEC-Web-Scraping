# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 00:08:18 2020

@author: Anirudh Raghavan
"""

import pandas as pd
import json
from SEC_Doc_Info__Scraping_v2 import doc_info

# We shall use this script to track and extract financial Information

with open('aapl_links.json') as json_file:
    aapl_links = json.load(json_file)

df = pd.read_csv('format.csv', index_col = False)

org_format = [i.lower().replace("'", "") for i in list(df['Particulars'])]

a = org_format[-1][-8]

org_format = [i.lower().replace(a, "") for i in org_format]
                   
#df_finance_info = pd.read_csv('Financial_Info.csv', index_col = False)

#print(df_finance_info.columns[-1])

#print(aapl_links[3]['file_date'])

for i in range(1,12):

    aapl = aapl_links[i]['links']

    result = doc_info(aapl,org_format,a)
    
    df[result[1]] = result[0]
  
df.to_csv('format.csv', index = False)
