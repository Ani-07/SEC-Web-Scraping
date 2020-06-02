# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 09:06:25 2020

@author: Anirudh Raghavan
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd

# We shall use Apple Inc as an example for this exercise

# Objective - Download Balance Sheet and Profit and Loss Account of the Apple 
# for the previous two quarters


aapl1 = "https://www.sec.gov/Archives/edgar/data/320193/000032019320000010/index.json"
aapl2 = "https://www.sec.gov/Archives/edgar/data/320193/000032019320000052/index.json"


content = requests.get(aapl1).json()

for file in content['directory']['item']:
    
    base_url = r"https://www.sec.gov"
    
    # Grab the filing summary and create a new url leading to the file so we can download it.
    if file['name'] == 'FilingSummary.xml':

        xml_summary = base_url + content['directory']['name'] + "/" + file['name']
        
        print('-' * 100)
        print('File Name: ' + file['name'])
        print('File Path: ' + xml_summary)

base_url = xml_summary.replace('FilingSummary.xml', '')

# request and parse the content
content = requests.get(xml_summary).content
soup = BeautifulSoup(content, 'lxml')

# find the 'myreports' tag because this contains all the individual reports submitted.
reports = soup.find('myreports')

balance_sheet ='CONSOLIDATED BALANCE SHEETS'
wrong_name = '(Parenthetical)'
income = 'CONSOLIDATED STATEMENTS OF OPERATIONS'

master_reports = []


for report in reports.find_all('report')[:-1]:

    # let's create a dictionary to store all the different parts we need.
    
    if balance_sheet in report.shortname.text and wrong_name not in report.shortname.text:
        print(report.shortname.text)
    
        report_dict = {}
        report_dict['name_short'] = report.shortname.text
        report_dict['name'] = 'Balance_Sheet'
        report_dict['position'] = report.position.text
        report_dict['category'] = report.menucategory.text
        report_dict['url'] = base_url + report.htmlfilename.text
    
        # append the dictionary to the master list.
        master_reports.append(report_dict)
        
    elif income in report.shortname.text:
        print(report.shortname.text)
    
        report_dict = {}
        report_dict['name_short'] = report.shortname.text
        report_dict['name'] = 'Income'
        report_dict['position'] = report.position.text
        report_dict['category'] = report.menucategory.text
        report_dict['url'] = base_url + report.htmlfilename.text
    
        # append the dictionary to the master list.
        master_reports.append(report_dict)
        

# loop through each statement url

df_dict = {}

for report in master_reports:
    statement = report['url']
    print(statement)
    df = pd.read_html(statement)
    
    df_dict[report['name']] = df[0]



df_dict["Balance_Sheet"] = df_dict["Balance_Sheet"].columns.to_frame().T.append(df_dict["Balance_Sheet"], ignore_index=True)
df_dict["Income"] = df_dict["Income"].columns.to_frame().T.append(df_dict["Income"], ignore_index=True)

df_dict['Income'].columns = ['Particulars','Year1','Year2']
df_dict['Balance_Sheet'].columns = ['Particulars','Year1','Year2']

df_dict['Income'] = df_dict['Income'].drop('Year2', axis = 1)
df_dict['Balance_Sheet'] = df_dict['Balance_Sheet'].drop('Year2', axis = 1)

df_dict['Income'].columns = ['Particulars','Year']
df_dict['Balance_Sheet'].columns = ['Particulars','Year']

df_finance_info = pd.DataFrame(columns = ('Particulars','Year'))

df_finance_info = df_finance_info.append(df_dict['Income'], ignore_index=True)
df_finance_info = df_finance_info.append(df_dict['Balance_Sheet'],ignore_index=True)

df_finance_info = df_finance_info.drop(0)

df_finance_info.to_csv('Financial_Info.csv', index = False)

    