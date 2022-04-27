# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 13:29:07 2022

Automatically plot the API data I automatically pull from three databases
Push it to GitHub page

@author: eschares
"""

import pandas as pd
import plotly.express as px
from datetime import date

df = pd.read_csv('API_data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y_%m_%d')

date=str(date.today())

fig = px.line(df, x='Date', y=['Dimensions','Web of Science', 'OpenAlex'])

fig.update_layout(title='Number of 2022 ISU authored papers, last updated '+date,
                  title_x=0.5,
                  xaxis_title='Date data was pulled',
                  yaxis_title='Number of 2022 ISU papers')

fig.write_html("API_data_graphed.html")  #save as HTML file"
