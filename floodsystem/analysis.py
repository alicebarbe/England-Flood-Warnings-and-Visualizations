# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 11:49:59 2020

@author: atylb2
"""
import matplotlib
import numpy as np

def polyfit(dates, levels, p):
    x = matplotlib.dates.date2num(dates)
    p_coeff = np.polyfit(x[0] - x, levels, p)
    poly = np.poly1d(p_coeff)
    
