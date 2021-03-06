# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 09:06:25 2020

@author: Anirudh Raghavan
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

# We shall use Apple Inc as an example for this exercise

# Objective - Download Balance Sheet and Profit and Loss Account of the Apple 
# for the previous two quarters

def doc_info(link):
    
    link = aapl_links[5]['links']
    
    content = requests.get(link).json()
    
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
    operations = 'CONSOLIDATED STATEMENTS OF OPERATIONS'
    income = "CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME"
        
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
            
        elif income in report.shortname.text and wrong_name not in report.shortname.text:
            print(report.shortname.text)
        
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name'] = 'Income'
            report_dict['position'] = report.position.text
            report_dict['category'] = report.menucategory.text
            report_dict['url'] = base_url + report.htmlfilename.text
        
            # append the dictionary to the master list.
            master_reports.append(report_dict)
        
        elif operations in report.shortname.text:
            print(report.shortname.text)
        
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name'] = 'Operations'
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
    df_dict["Operations"] = df_dict["Operations"].columns.to_frame().T.append(df_dict["Operations"], ignore_index=True)
    
    bs = df_dict["Balance_Sheet"].iloc[:,1]
    inc = df_dict["Income"].iloc[:,1]
    op = df_dict['Operations'].iloc[:,1]
    
    inc.name = bs.name
    op.name = bs.name
    
    fin = op.append(inc, ignore_index = True)
    fin = fin.append(bs, ignore_index = True)
    
    return fin, bs.name
    

df_finance_info[bs.name] = fin


op = df_dict["Operations"]

op.columns = [1,2,3,4,5]


op = op.drop(op.columns[2:5], axis = 1)



bs = df_dict["Balance_Sheet"]
inc = df_dict["Income"]
op = df_dict['Operations']

op.columns = ['1','2','3']

bs.columns = ['1','2','3']
inc.columns = op.columns

op = op.drop(op.columns[2:5], axis = 1)
bs = bs.drop(bs.columns[2:3], axis = 1)
inc = inc.drop(inc.columns[2:5], axis = 1)

fin = op.append(inc, ignore_index = True)
fin = fin.append(bs, ignore_index = True)

List_D = list(fin['1'])

result = {}

for i in List_D:
    if i not in result.keys():
        result[i] = [j for j in range(len(List_D)) if List_D[j] == i]

print(result)


List_E = list(df_finance_info['Particulars'])

result2 = {}

for i in List_E:
    if i not in result2.keys():
        result2[i] = [j for j in range(len(List_E)) if List_E[j] == i]

result2

n = 0
avl = []
mismat = []
unavl = []

for key in result.keys():
    if key in result2.keys():
        if result[key] == result2[key]:
            avl.append(n)
            n += 1
            print(key)
            print(1)
        elif :
            mismat.append(n)
            n += 1
            print(key)
            print(2)
    else:
        unavl.append(n)
        n += 1
        print(key)
        print(3)

            
            
