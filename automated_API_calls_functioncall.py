# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 11:26:21 2022

@author: eschares

Manage API calls to different databases: OpenAlex, Dimensions, Web of Science
Count number of ISU authored papers in 2022
Scheduled to run each day at 9:05am automatically through Windows Task Scheduler
"""

import os
import requests
import dimcli
import json

import pandas as pd
import plotly.express as px
#from datetime import date
from datetime import datetime



def OpenAlex(year):
    print ("In OpenAlex")
    OUR_API_URL = "https://api.openalex.org/works?filter=institution.id:I173911158&group_by=publication_year&sort=key:desc&mailto=eschares@iastate.edu"
    api_response = requests.get(OUR_API_URL)

    parsed_response = api_response.json()

    result_list = parsed_response["group_by"]

    for result in result_list:
        if result["key"]==str(year):
            print(result["key"], result["count"])
            #print(result["count"])
            openalex_sum = result['count']
    
    return str(openalex_sum)


def Dimensions(year):
    print("\nIn Dimensions")
    intyear = int(year)  # Dimensions API needs year to be an integer, not a string
    dimcli.login()  # my Dimensions API key already saved in dimcli installation on my local machine

    dsl = dimcli.Dsl()

    query = f"""search publications 
        where research_org_names = "Iowa State University" and year={intyear}
        return publications"""

    number_of_papers = dsl.query(query)
    #produces number_of_papers.count_total, number of ISU [year] papers in Dim

    return str(number_of_papers.count_total)


def WebofScience(year):
    print("\nIn WoS")
    #pubs_all = pd.DataFrame(columns = ['number', 'raw_pub_data'])

    # saved to my Environment Variables
    clarivate_api_key = os.environ.get('CLARIVATE_API_KEY')

    query = "OG = (Iowa State University) AND PY = " + str(year)

    # Here is the call we put out the API. Enter formatted query where it says *query*
    # 5/27/22 - changed count=0 so we can still get the NUMBER of results, just not using up any of our data with returning records
    url = "https://api.clarivate.com/api/wos?databaseId=WOS&usrQuery=("+query+")&count=0&firstRecord=1"
    
    #the request.get function sends out the url request along with the API key
    r = requests.get(url, headers={"X-APIKey": clarivate_api_key})
    
    #the results come back as a json. If there are any papers, the results are stored.
    results = json.loads(r.text)

    return str(results['QueryResult']['RecordsFound'])


# 2022 data
openalex_sum = OpenAlex(2022)
dimensions_sum = Dimensions(2022)
wos_sum = WebofScience(2022)

print("\n\n2022:\nOpenAlex: ", openalex_sum)
print("Dimensions: ", dimensions_sum)
print("Web of Science: ", wos_sum)

date = datetime.now().strftime("%Y_%m_%d")
file = open("ISU_2022_pubs_API_data.csv", "a")
file.write(date + ',' + openalex_sum + ',' + dimensions_sum + ',' + wos_sum + "\n")
file.close()

##  Graph the data and save as HTML file

df = pd.read_csv('ISU_2022_pubs_API_data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y_%m_%d')

fig = px.line(df, x='Date', y=['Dimensions','Web of Science', 'OpenAlex'])

fig.update_layout(title='Number of 2022 ISU authored papers, last updated '+date,
                  title_x=0.5,
                  xaxis_title='Date data was pulled',
                  yaxis_title='Number of 2022 ISU papers')

fig.write_html("ISU_2022_pubs_API_data_graphed.html")  #save as HTML file, overwrites old versions


# 4/28/23 - 2023 data
openalex_sum = OpenAlex(2023)
dimensions_sum = Dimensions(2023)
wos_sum = WebofScience(2023)

print("\n\n2023:\nOpenAlex: ", openalex_sum)
print("Dimensions: ", dimensions_sum)
print("Web of Science: ", wos_sum)

date = datetime.now().strftime("%Y_%m_%d")
file = open("ISU_2023_pubs_API_data.csv", "a")
file.write(date + ',' + openalex_sum + ',' + dimensions_sum + ',' + wos_sum + "\n")
file.close()

##  Graph the data and save as HTML file

df = pd.read_csv('ISU_2023_pubs_API_data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y_%m_%d')

fig = px.line(df, x='Date', y=['Dimensions', 'Web of Science', 'OpenAlex'])

fig.update_layout(title='Number of 2023 ISU authored papers, last updated '+date,
                  title_x=0.5,
                  xaxis_title='Date data was pulled',
                  yaxis_title='Number of 2023 ISU papers')

# save as HTML file, overwrites old versions
fig.write_html("ISU_2023_pubs_API_data_graphed.html")
