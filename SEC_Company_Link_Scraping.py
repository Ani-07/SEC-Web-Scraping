# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:39:04 2020

@author: Anirudh Raghavan
"""
from bs4 import BeautifulSoup
import requests
import json
#import pandas as pd

# Objective - To scrape SEC website to find the document links to quarterly - 10Q filings

# Example stock - Apple Inc

cik = comp_list[10]

# base URL for the SEC EDGAR browser
endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

# define our parameters dictionary
param_dict = {'action':'getcompany',
              'owner':'exclude',
              'type':'10-Q',
              'CIK': cik,
              'count':'100'}

# request the url, and then parse the response.
response = requests.get(url = endpoint, params = param_dict)
soup = BeautifulSoup(response.content, 'html.parser')

# Let the user know it was successful.
print('Request Successful')
print(response.url)

# Find all the tables within the url

doc_table = soup.find_all('table', class_='tableFile2')

# define a base url that will be used for link building.
base_url_sec = r"https://www.sec.gov"

master_list = []

# loop through each row in the table.
for row in doc_table[0].find_all('tr'):
    
    # find all the columns
    cols = row.find_all('td')
    
    # if there are no columns move on to the next row.
    if len(cols) != 0:        
        
        # grab the text
        filing_type = cols[0].text.strip()                 
        filing_date = cols[3].text.strip()
        filing_numb = cols[4].text.strip()
        
        # find the links
        filing_doc_href = cols[1].find('a', {'href':True, 'id':'documentsbutton'})       
        
        # grab the the first href
        if filing_doc_href != None:
            filing_doc_link = base_url_sec + filing_doc_href['href'] 
            
            # Edit the document link with the required format
        
            filing_doc_link = filing_doc_link.split('/')
            del filing_doc_link[-1]
            filing_doc_link = "/".join(filing_doc_link)
            filing_doc_link = filing_doc_link + '/index.json'
            
        else:
            filing_doc_link = 'no link'
        
        
        # create and store data in the dictionary
        file_dict = {}
        file_dict['file_type'] = filing_type
        file_dict['file_number'] = filing_numb
        file_dict['file_date'] = filing_date
        file_dict['links'] =  filing_doc_link
        
        # let the user know it's working
        print('-'*100)        
        print("Filing Type: " + filing_type)
        print("Filing Date: " + filing_date)
        print("Filing Number: " + filing_numb)
        print("Document Link: " + filing_doc_link)
        
        # append dictionary to master list
        master_list.append(file_dict)

file1 = open("aapl_links.json","a")
file1.write(json.dumps(master_list))
file1.close()    



