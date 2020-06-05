# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 09:06:25 2020

@author: Anirudh Raghavan
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# We shall use Apple Inc as an example for this exercise

# Objective - Download Balance Sheet and Profit and Loss Account of the Apple 
# for the previous two quarters

def unq_count(LIST):
    result = {}
    for i in LIST:
        if i not in result.keys():
            result[i] = [j for j in range(len(LIST)) if LIST[j] == i ]
    return result


def doc_info(link, org_format, a):
    
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
    df_dict["Operations"] = df_dict["Operations"].columns.to_frame().T.append(df_dict["Operations"], ignore_index=True)
    
    bs = df_dict["Balance_Sheet"]
    op = df_dict['Operations']

    op = op.drop(op.columns[2:len(op.columns)], axis = 1)
    bs = bs.drop(bs.columns[2:len(bs.columns)], axis = 1)

    op.columns = bs.columns

    fin = op.append(bs, ignore_index = True)
    
    list_names = [i.lower().replace("'", "") for i in list(fin.iloc[:,0])]
    List_D1 = [i.lower().replace("'", "") for i in list(fin.iloc[:,0])]
    
    list_names = [i.lower().replace(a, "") for i in list_names]
    List_D1 = [i.lower().replace(a, "") for i in List_D1]
    
    list_values = list(fin.iloc[:,1])
    
    for item in list_names:
        if item not in org_format:
            if any(s in item for s in org_format):    
                for tag in org_format:
                    if tag in item:
                        ind = List_D1.index(item)
                        List_D1[ind] = tag
                        
                        break
            
            else:
                ind = List_D1.index(item)
                del List_D1[ind]
                del list_values[ind]
    
    dict_D1 = unq_count(List_D1)
    dict_format = unq_count(org_format)

    for key in dict_format.keys():
        if key in dict_D1.keys():
            if len(dict_format[key]) < len(dict_D1[key]):
                ind = list(set(dict_D1[key])-set(dict_format[key]))        
                n = 0
                for i in ind:
                    i = i - n
                    del List_D1[i]
                    del list_values[i]
                    n += 1
            
            dict_D1 = unq_count(List_D1)
        
    for key in dict_format.keys():
        if key not in dict_D1.keys():
            ind = dict_format[key]
            for i in ind:
                List_D1.insert(i,key)
                list_values.insert(i,np.nan)
            dict_D1 = unq_count(List_D1)
        
    for key in dict_format.keys():
        if len(dict_format[key]) > len(dict_D1[key]):
            ind = list(set(dict_format[key])-set(dict_D1[key]))        
            for i in ind:
                List_D1.insert(i,key)
                list_values.insert(i,np.nan)
            dict_D1 = unq_count(List_D1)
    
    return list_values, op.columns[1]

    
