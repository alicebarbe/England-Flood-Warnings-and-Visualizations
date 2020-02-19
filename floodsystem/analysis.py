# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 11:49:59 2020

@author: atylb2
"""
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def polyfit(dates, levels, p):
    """Creates polynomial of order p that fits the level data
    
    Arguments:
        dates (list of DateTime objects):
            list of dates with datapoints
        levels (list of floats):
            list of levels corresponding to each point in dates
        p (int):
            order of polynomial to fit
    
    Returns:
        poly (np.poly1d object):
            polynomial object that fits level data
        d0 (DateTime object):
            offset used to normalize dates to start at 0, equal to the first
            date in dates
    
    """
    x = [date.timestamp() / 60 for date in dates]
    x = [a - x[-1] for a in x]
    p_coeff = np.polyfit(x, levels, p)
    poly = np.poly1d(p_coeff)
    
    return (poly, dates[-1])
