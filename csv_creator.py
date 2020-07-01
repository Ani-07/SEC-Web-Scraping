# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 21:55:28 2020

@author: Anirudh Raghavan
"""

from SEC_Doc_Scraping import doc_info_std
import json
from time import sleep

# Create list of company links

def comp_links(comp_list, forms):

    meta_list = []
    
    for stock in comp_list:
        files = []
        for form in forms:
            file_name = stock + form + "_links.json"
            files.append(file_name)
        meta_list.append(files)
        
    return meta_list
 

def csv_creator(meta_list, comp_list, forms, K_s, K_e, Q_s, Q_e):

    result_balance = []
    result_income = []
    signals = {}
    
    for i in range(len(meta_list)):
        files = meta_list[i]
        stock = comp_list[i]
        
        if i == 0 or i == 1:
            typ = 1
        else:
            typ = 0
            
        for j in range(len(files)):
            print(j)
            file = files[j]
            form = forms[j]
            
            with open(file) as json_file:
                links = json.load(json_file)
                
                if j == 0:
                    for a in range(K_s, K_e):
                
                        link = links[a]['links']
                        date = links[a]['file_date']
                        
                        if links[a]['file_type'] == "10-K":
                            
                            tmp = doc_info_std(link, form, stock, date, typ)
                            signals[link] = tmp
                            csv_file_b = stock + "_" + form + "_" + "Balance_Sheet" + "_" + date + ".csv"
                            csv_file_i = stock + "_" + form + "_" + "Income" + "_" + date + ".csv"
                            result_balance.append(csv_file_b)
                            result_income.append(csv_file_i)
                        
                        sleep(3)
                        
                else:
                    for a in range(Q_s, Q_e):
                
                        link = links[a]['links']
                        date = links[a]['file_date']
                        
                        if links[a]['file_type'] == "10-Q":
                            
                            tmp = doc_info_std(link, form, stock, date,typ)
                            signals[link] = tmp
                            csv_file_b = stock + "_" + form + "_" + "Balance_Sheet" + "_" + date + ".csv"
                            csv_file_i = stock + "_" + form + "_" + "Income" + "_" + date + ".csv"
                            result_balance.append(csv_file_b)
                            result_income.append(csv_file_i)
                        sleep(3)
                            
    return result_balance, result_income, signals
                

if __name__ == '__main__':
    
    file = meta_list[4][1]
    with open(file) as json_file:
        links = json.load(json_file)
    
    link = links[0]['links']
    date = links[0]['file_date']
    
    a = doc_info_std(link,"10-Q","IBM",date,1)
        
        
        
