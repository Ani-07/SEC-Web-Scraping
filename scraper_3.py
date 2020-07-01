# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:23:19 2020

@author: Anirudh Raghavan
"""

from SEC_Doc_Scraping import doc_info_std
from doc_combiner import inc_doc_sum
from csv_creator import comp_links, csv_creator

comp_list = ["Amazon Com", "Apple Inc", "Microsoft", "Intel Corp",
             "INTERNATIONAL BUSINESS MACHINES CORP"]
  
forms = ["10-K","10-Q"]
      
meta_list = comp_links(comp_list, forms)
    
results = csv_creator(meta_list, comp_list, forms,7,16,19,46)

for csv_name in results[1]:
    inc_doc_sum(csv_name)

