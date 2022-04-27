# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:44:52 2022

@author: eschares
"""

import requests
import dimcli
from datetime import datetime

def OpenAlex():
    OUR_API_URL = "https://api.openalex.org/works?filter=institution.id:I173911158&group_by=publication_year&sort=key:desc&mailto=eschares@iastate.edu"
    api_response = requests.get(OUR_API_URL)

    parsed_response = api_response.json()

    result_list = parsed_response["group_by"]

    for result in result_list:
        if result["key"]=="2022":
            print(result["key"])
            print(result["count"])
            openalex_sum = result['count']
    
    return openalex_sum 

answer = OpenAlex()
answer = str(answer)

date = datetime.now().strftime("%Y_%m_%d")
date

file = open("API_data2.csv", "a")
file.write(date + "," + answer)
file.close()