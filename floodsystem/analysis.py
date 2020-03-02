# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 11:49:59 2020

@author: atylb2
"""

from datetime import datetime
import numpy as np

def polyfit(dates, levels, p):
    """Creates polynomial of order p that fits the level data
    
    Arguments:
        dates: (list of DateTime objects).
            list of dates with datapoints
        levels: (list of floats).
            list of levels corresponding to each point in dates
        p: (int).
            order of polynomial to fit
    
    Returns:
        poly: (np.poly1d object).
            polynomial object that fits level data
        d0: (DateTime object).
            offset used to normalize dates to start at 0, equal to the first
            date in dates
    
    """
    # convert date to minutes since epoch
    x = [date.timestamp() / 60 for date in dates]
    
    # normalize dates to start at 0, where the first date is 0
    x = [a - x[-1] for a in x]
    
    # fit polynomial to levels
    p_coeff = np.polyfit(x, levels, p)
    poly = np.poly1d(p_coeff)
    
    # return polynomial object initial time offset
    return (poly, dates[-1])
