# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:58:09 2020

@author: Anirudh Raghavan
"""

import pandas as pd
import json


def search_exact(search, names_list, tmp_list):
    break_v = "No"
    for name in names_list:
        for item in tmp_list:
            if name in item:
                a = tmp_list.index(item)
                break_v = "Yes"
                break
            
            elif item == tmp_list[-1]:
                a = "No " + search
            
            if break_v == "Yes":
                break
    
    return a

def search_contain(search,names_list, tmp_list):
    for item in tmp_list:
        if all(x in item for x in names_list):
            result = tmp_list.index(item)
            break
        else:
            result = "No " + search
    return result
           


def inc_doc_sum (csv_name):
    
    with open("format_dict.json") as json_file:
        format_dict = json.load(json_file)

    tmp = pd.read_csv(csv_name)
    tmp_values = list(tmp[tmp.columns[1]])
    tmp_list = list(tmp[tmp.columns[0]])
    tmp_list = [str(x) for x in tmp_list]
    tmp_list = [x.lower() for x in tmp_list]
    
    doc_dict = {}
    
    doc_dict['Stock'] = csv_name.split("_")[0]
    doc_dict['Form'] = csv_name.split("_")[1]
    doc_dict['Date'] = csv_name.split("_")[-1].split(".")[0]
    
    for key in format_dict.keys():
        if key == "Income before taxes" or key == "Dividends" or key == "Net Income":
            result = search_contain(key, format_dict[key], tmp_list)
        else:
            result = search_exact(key, format_dict[key], tmp_list)
        
        if type(result) == int:
            doc_dict[key] = tmp_values[result]
        else:
            doc_dict[key] = result
     
    db = pd.read_csv("inc_format.csv")
    db = db.append(doc_dict, ignore_index = True)
    db.to_csv("inc_format.csv", index = False)

    


#file1 = open("csv_list_income.txt","r")
#result = file1.read()
#result = result.split(", ")

