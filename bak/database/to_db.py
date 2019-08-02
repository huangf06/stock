#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd, numpy as np, tushare as ts
import time
ts.set_token('7122fa9fc9317803d678bcdf5cbc2d2f67174243855d87eb36b48c57')
pro=ts.pro_api()
dt=time.strftime('%Y%m%d',time.localtime())
st=time.strftime('%Y%m%d',time.gmtime(time.time()-30*24*3600))


# In[2]:


df = pro.daily(trade_date=dt)


# In[3]:


if len(df)==0:
    cal=pro.trade_cal(exchange='',start_date=st,end_date=dt)
    lt=cal[cal.is_open==1].iloc[-2,1]
    df=pro.daily(trade_date=lt)


# In[4]:


# df.sort_values(by='amount')


# In[5]:


df


# In[ ]:


from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine("mysql://alpha:123@localhost/mysql")

try:
    df.to_sql('test',con=engine,if_exists='replace',index=False)
except Exception as e:
    print(e)

