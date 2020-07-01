# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:39:04 2020

@author: Anirudh Raghavan
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Objective - To scrape SEC website to find the document links to quarterly - 10Q filings

# Example stock - Apple Inc

def get_url(cik):
    
    # base URL for the SEC EDGAR browser
    endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"
    
    # define our parameters dictionary
    param_dict = {'action':'getcompany',
              'owner':'exclude',
              'type':'10-K',
              'CIK': cik,
              'count':'100'}

    # request the url, and then parse the response.

    response = requests.get(url = endpoint, params = param_dict)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Let the user know it was successful.
    print('Request Successful')
    print(response.url)
    
    return soup

def quart_extract(date):
    month = date.month
    if month in [1,2,3]:
        quart = 4
    elif month in [4,5,6]:
        quart = 1
    elif month in [7,8,9]:
        quart = 2
    elif month in [10,11,12]:
        quart = 3
    else:
        quart = 0
    
    return quart




def table_find(soup, cik):
    
    master_list = pd.DataFrame(columns = ['CIK','Type','Date','Year','Quarter'])
    
    file_dict = {}
    file_dict['CIK'] = cik
    
    # Find all the tables within the url

    doc_table = soup.find_all('table', class_='tableFile2')
        
    if len(doc_table) == 0:
        print('doc-table')
        master_list = master_list.append(file_dict, ignore_index = True)
        
        return master_list
    
    elif len(doc_table[0].find_all('tr')) == 0:
        print('row')
        master_list = master_list.append(file_dict, ignore_index = True)
        
        return master_list
        
    
    print(len(doc_table[0].find_all('tr')))
    
    # loop through each row in the table.
    for row in doc_table[0].find_all('tr'):
        
        # find all the columns
        cols = row.find_all('td')
        
        
        # if there are no columns move on to the next row.
        if len(cols) != 0:
            print('info')
    
            # grab the text
            filing_type = cols[0].text.strip()                 
            filing_date = cols[3].text.strip()
            
            # Convert date object
            converted = datetime.strptime(filing_date, '%Y-%m-%d')
            converted = datetime.date(converted)
            
            # Extract Year
            
            year = converted.year
            quarter = quart_extract(converted)

           # create and store data in the dictionary
            file_dict = {}
            
            file_dict['CIK'] = cik
            file_dict['Type'] = filing_type
            file_dict['Date'] = converted
            file_dict['Year'] = year
            file_dict['Quarter'] = quarter
            
            # let the user know it's working
            print('-'*100)        
            print("Filing Type: " + filing_type)
            print("Filing Date: " + filing_date)
            print(cik)
            
            # append dictionary to master list
            master_list = master_list.append(file_dict, ignore_index = True)
            
    return master_list
         


#########################################################

#Opening text file and converting to list

file = open("Tech Company list.txt","r")
comp_list = file.readlines()
comp_list[0]

comp_list = [x.replace("\n","") for x in comp_list]
comp_list = [x.replace(" ","") for x in comp_list]

######################################################

#master_dates = pd.DataFrame(columns = ['CIK','Type','Date','Year','Quarter'])

for cik in comp_list:
#    cik = comp_list[12]
    soup = get_url(cik)
    date_list = table_find(soup, cik)
    master_dates = master_dates.append(date_list, ignore_index = True)



#Steps

# Take 1 Company
# IDentify whether 10-Q available - if no mark as not available
# Find all 10-K and 10-Q
# Extract Year and Q No from date
# Match with company name and Year and Q
# Add date if available

master_dates.to_csv("Comp_dates.csv")

