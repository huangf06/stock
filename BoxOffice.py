# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 11:57:59 2017

@author: Company
"""

import tushare as ts
df = ts.realtime_boxoffice()
print(df)