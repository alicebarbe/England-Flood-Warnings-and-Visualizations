# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 11:49:59 2020

@author: atylb2
"""
import time
import numpy as np
import matplotlib.pyplot as plt

def polyfit(dates, levels, p):
    x = [time.mktime(date.timetuple()) / 60 for date in dates]
    x = [a - x[-1] for a in x]
    p_coeff = np.polyfit(x, levels, p)
    poly = np.poly1d(p_coeff)
    """
    # Plot original data points
    plt.plot(x, levels, '.')
    
    # Plot polynomial fit at 30 points along interval
    plt.plot(x1, poly(x1))
    
    # Display plot
    plt.show()
    """

    x1 = np.linspace(x[0], x[-1], 50)
    return (poly(x1))
