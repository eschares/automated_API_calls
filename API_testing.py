# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:24:49 2022

@author: eschares
"""

import requests
import json
import matplotlib.pyplot as plt


print ("In OpenAlex")
if(0):
    OUR_API_URL = "https://api.openalex.org/works?filter=institution.id:I173911158&group_by=publication_year&sort=key:desc&mailto=eschares@iastate.edu"
    api_response = requests.get(OUR_API_URL)
    
    parsed_response = api_response.json()
    
    result_list = parsed_response["group_by"]
    
    years = []
    year_counts = []
    
    for i in range(1960, 2022):
        years.append(i)
    
    for year in years:
        year = str(year)
        for result in result_list:
            if result["key"]==year:
                print(f'{result["key"]}: {result["count"]}')
                year_counts.append(result["count"])
            
    #print(year_counts)
    
    plt.bar(years, year_counts)

years = []
for i in range(2015, 2022):
    years.append(str(i))

is_oa = []
is_not_oa = []

for year in years:
    OUR_API_URL = 'https://api.openalex.org/works?filter=institution.id:I173911158,is_paratext:false,type:journal-article,from_publication_date:'+year+'-01-01,to_publication_date:'+year+'-12-31&group_by=is_oa&mailto=eschares@iastate.edu'
    api_response = requests.get(OUR_API_URL)

    parsed_response = api_response.json()

    result_list = parsed_response['group_by']
    
    #print(result_list[0])
    for k,v in result_list[0].items():
        print(k,v)
    
    for result in result_list:
        #print(result)
        if result["key"] == 'true':
            is_oa.append(result['count'])
        elif result["key"] == 'false':
            is_not_oa.append(result['count'])
            
#plt.plot(years,is_oa)
#plt.plot(years,is_not_oa)
