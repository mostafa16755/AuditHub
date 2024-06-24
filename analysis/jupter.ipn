#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import pygwalker as pyg

# # Load data and skip the index column
file_path = 'sales_data_sample.csv'
df = pd.read_csv(file_path, index_col=0)

print(df.head())

pyg.walk(df)

