# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 09:06:25 2020

@author: Anirudh Raghavan
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd


# Objective - Download Balance Sheet and Profit and Loss Account of the Apple 
# for the previous two quarters

def unq_count(LIST):
    result = {}
    for i in LIST:
        if i not in result.keys():
            result[i] = [j for j in range(len(LIST)) if LIST[j] == i ]
    return result


def col_ident(df):
    for i in range(0,len(df.columns)):
        if df.iloc[0,i] != df.iloc[0,i+1]:
            value = i+1
            break
    return value

def doc_info_std(link, form, stock, date, typ):
    
    content = requests.get(link).json()
    
    print('-' * 100)
    print(link)
    
    for file in content['directory']['item']:
        
        base_url = r"https://www.sec.gov"
        
        # Grab the filing summary and create a new url leading to the file so we can download it.
        if file['name'] == 'FilingSummary.xml':
    
            xml_summary = base_url + content['directory']['name'] + "/" + file['name']
            
            print('File Name: ' + file['name'])
            print('File Path: ' + xml_summary)
            break
         
        elif file == content['directory']['item'][-1]:
            return    
    
    base_url = xml_summary.replace('FilingSummary.xml', '')
    
    # request and parse the content
    
    content = requests.get(xml_summary).content
    soup = BeautifulSoup(content, 'lxml')
    
    # find the 'myreports' tag because this contains all the individual reports submitted.
    reports = soup.find('myreports')
    
    balance_sheet_1 ='BALANCE SHEET'
    balance_sheet_2 ='Statement of Financial Position'
    
    wrong_names_bs = ['parenthetical','component','supplemental','reconciliation','derivative','details']
    
    operations_1 = ['income','statement']
    
    operations_2 = ['statement', 'operations']
    
    operations_3 = ['earnings','statement']
    
    wrong_names_inc = ['parenthetical','comprehensive','derivative','segment','deferred', 
                       'reclassified','details']
    
    master_reports = []
    
    
    for report in reports.find_all('report')[:-1]:
    
        # let's create a dictionary to store all the different parts we need.
        if balance_sheet_1.lower() in report.shortname.text.lower() and all(name not in report.shortname.text.lower() for name in wrong_names_bs) and report.htmlfilename != None:
            
            print(report.shortname.text)
        
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name'] = 'Balance_Sheet'
            report_dict['url'] = base_url + report.htmlfilename.text
            
            # append the dictionary to the master list.
            master_reports.append(report_dict)
            
        elif balance_sheet_2.lower() in report.shortname.text.lower() and all(name not in report.shortname.text.lower() for name in wrong_names_bs) and report.htmlfilename != None:
            print(report.shortname.text)
        
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name'] = 'Balance_Sheet'
            report_dict['url'] = base_url + report.htmlfilename.text
            
            # append the dictionary to the master list.
            master_reports.append(report_dict)
        
        
        elif all(name in report.shortname.text.lower() for name in operations_1) and all(name not in report.shortname.text.lower() for name in wrong_names_inc) and report.htmlfilename != None:
            print(report.shortname.text)
        
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name'] = 'Operations'
            report_dict['url'] = base_url + report.htmlfilename.text
            
            master_reports.append(report_dict)
            
        elif all(name in report.shortname.text.lower() for name in operations_2) and all(name not in report.shortname.text.lower() for name in wrong_names_inc) and report.htmlfilename != None:
            print(report.shortname.text)
        
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name'] = 'Operations'
        
            report_dict['url'] = base_url + report.htmlfilename.text
            
            master_reports.append(report_dict)
        
        
        elif all(name in report.shortname.text.lower() for name in operations_3) and all(name not in report.shortname.text.lower() for name in wrong_names_inc) and report.htmlfilename != None:
            print(report.shortname.text)
        
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name'] = 'Operations'
        
            report_dict['url'] = base_url + report.htmlfilename.text
            
            # append the dictionary to the master list.
            master_reports.append(report_dict)
    
    if len(master_reports) == 0:
        signal = "HTML files unavailable"
        
    else:
        signal = "HTML files available"
   
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
        
        value = col_ident(op)
        
        if value >= 1:
            op = op.drop(op.columns[value+1:len(op.columns)], axis = 1)
            op = op.drop(op.columns[1:value], axis = 1)
        else:
            op = op.drop(op.columns[value+1:len(op.columns)], axis = 1)
            
        value = col_ident(bs)
        
        if value >= 1:
            bs = bs.drop(bs.columns[value+1:len(bs.columns)], axis = 1)
            bs = bs.drop(bs.columns[1:value], axis = 1)
        else:
            bs = bs.drop(bs.columns[value+1:len(bs.columns)], axis = 1)
        
        
        file_name = stock + "_" + form + "_" + "Balance_Sheet" + "_" + date + ".csv"
        bs.to_csv(file_name, index = False)
        
        
        file_name = stock + "_" + form + "_" + "Income" + "_" + date + ".csv"
        op.to_csv(file_name, index = False)
    
    return signal
