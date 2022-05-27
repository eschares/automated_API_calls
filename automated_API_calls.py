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



def OpenAlex():
    print ("In OpenAlex")
    OUR_API_URL = "https://api.openalex.org/works?filter=institution.id:I173911158&group_by=publication_year&sort=key:desc&mailto=your@email"
    api_response = requests.get(OUR_API_URL)

    parsed_response = api_response.json()

    result_list = parsed_response["group_by"]

    for result in result_list:
        if result["key"]=="2022":
            print(result["key"])
            print(result["count"])
            openalex_sum = result['count']
    
    return str(openalex_sum)


def Dimensions():
    print ("In Dimensions")
    dimcli.login()

    dsl = dimcli.Dsl()
    
    number_of_papers = dsl.query("""search publications 
        where research_org_names = "Iowa State University" and year=2022 
        return publications"""
        )
    #produces number_of_papers.count_total, number of ISU 2022 papers in Dim


    #Here we work on the breakdown by publisher
    data = dsl.query("""search publications 
        where research_org_names = "Iowa State University" and year=2022 
        return publisher"""
        )

    date = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

    df = data.as_dataframe()
    
    #sum_of_papers = df['count'].sum()   #wrong, only sums the top 20 publishers that got returned
    #print(sum_of_papers)

    if (0):
        ax = df.plot(
            kind='barh', 
            x='id', 
            y='count', 
            title='2022 ISU authored papers in Dimensions, total ' + str(number_of_papers.count_total) + '\nupdated ' + date, 
        )
        
        ax.yaxis.grid(True, linestyle='--', linewidth=0.5)
        
        fig = ax.get_figure()
        figure_filename = "output_" + date + ".png"
        fig.savefig(figure_filename)
    
    return str(number_of_papers.count_total)

def WebofScience():
    print ("In WoS")
    #pubs_all = pd.DataFrame(columns = ['number', 'raw_pub_data'])

    query = "OG = (Iowa State University) AND PY = 2022"


    # Here is the call we put out the API. You can enter your formatted query where it says *query*
    # 5/27/22 - changed count=0 so we can still get the NUMBER of results, just not using up any of our data with returning records
    url = "https://api.clarivate.com/api/wos?databaseId=WOS&usrQuery=("+query+")&count=0&firstRecord=1"
    #the request.get function sends out the url request along with the API key
    r = requests.get(url,headers = {"X-APIKey":"your_key"})                                                                           
    #the results come back as a json. If there are any papers, the results are stored.  
    results = json.loads(r.text)
    
    return str(results['QueryResult']['RecordsFound'])

os.system("move *.png old_publisher_graphs")

openalex_sum = OpenAlex()
dimensions_sum = Dimensions()
wos_sum = WebofScience()

print("\n\nOpenAlex: ", openalex_sum)
print("Dimensions: ", dimensions_sum)
print("Web of Science: ", wos_sum)

date = datetime.now().strftime("%Y_%m_%d")
file = open("API_data.csv", "a")
file.write(date + ',' + openalex_sum + ',' + dimensions_sum + ',' + wos_sum + "\n")
file.close()


##  Graph the data and save as HTML file

df = pd.read_csv('API_data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y_%m_%d')

fig = px.line(df, x='Date', y=['Dimensions','Web of Science', 'OpenAlex'])

fig.update_layout(title='Number of 2022 ISU authored papers, last updated '+date,
                  title_x=0.5,
                  xaxis_title='Date data was pulled',
                  yaxis_title='Number of 2022 ISU papers')

fig.write_html("API_data_graphed.html")  #save as HTML file, overwrites old versions
