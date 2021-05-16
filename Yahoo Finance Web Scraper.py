#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html
import requests
import json
import argparse
from collections import OrderedDict

driver = webdriver.Chrome(ChromeDriverManager().install())
content = driver.page_source
soup = BeautifulSoup(content)


# In[2]:


def financial(name):
    is_link = "https://finance.yahoo.com/quote/" + name + "/financials?p=" + name + "%27"
    driver.get(is_link)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = BeautifulSoup(html,'lxml')
    close_price = [entry.text for entry in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
    features = soup.find_all('div', class_='D(tbr)')
    headers = []
    temp_list = []
    label_list = []
    final = []
    index = 0
    for item in features[0].find_all('div', class_='D(ib)'):
        headers.append(item.text)
    while index <= len(features)-1:
        temp = features[index].find_all('div', class_='D(tbc)')
        for line in temp:
            temp_list.append(line.text)
        final.append(temp_list)
        temp_list = []
        index+=1
    df = pd.DataFrame(final[1:])
    df.columns = headers

    def convert_to_numeric(column):
        first_col = [i.replace(',','') for i in column]
        second_col = [i.replace('-','') for i in first_col]
        final_col = pd.to_numeric(second_col)

        return final_col

    for column in headers[1:]:

        df[column] = convert_to_numeric(df[column])
        df[column] = df[column].apply(lambda x: '{:.2f}'.format(x))

    final_df = df.fillna('-')
    content = driver.page_source
    soup = BeautifulSoup(content)
    financial_currency = soup.find('span', attrs={'class':'Fz(xs) C($tertiaryColor) Mstart(25px) smartphone_Mstart(0px) smartphone_D(b) smartphone_Mt(5px)'})
    print (financial_currency.text)
    display (final_df)


# In[3]:


financial("TSM")


# In[4]:


def stockprice(name):
    sum_link ="https://finance.yahoo.com/quote/" + name + "?p=" + name
    driver.get(sum_link)
    driver.execute_script("window.scrollTo(0, 5000)") 
    content = driver.page_source
    soup = BeautifulSoup(content)
    stock_price = soup.find('span', attrs={'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})
    stock_currency = soup.find('span', attrs={'data-reactid':'9'})
    print (name)
    print (stock_price.text)
    yes=stock_currency.text.split()
    print (yes[-3] + " " + yes[-2] + " " + yes[-1])
    


# In[5]:


stockprice("TSM")


# In[6]:


def companyprofile(name):
    sum_link ="https://www.marketwatch.com/investing/stock/" + name.lower()
    driver.get(sum_link)
    content = driver.page_source
    soup = BeautifulSoup(content)
    profile = soup.find('p', attrs={'class':'description__text'})
    print (profile.text)


# In[7]:


companyprofile("TSM")


# In[8]:


def overall_message(name):
    stockprice(name)
    print ("\n")
    print ("\n")
    companyprofile(name)
    print ("\n")
    print ("\n")
    financial (name)


# In[9]:


overall_message("JPM")


# In[10]:


overall_message("GOOG")


# In[ ]:




