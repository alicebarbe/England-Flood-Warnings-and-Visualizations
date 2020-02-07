# -*- coding: utf-8 -*-
#from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot

def plot_water_levels(argv):
    """Plot the water levels of stations given corresponding date. Subplots are
    created for each station.
    
    Arguments:
        
    
    """ 
    if len(argv) % 3 != 0:
        raise ValueError("Number of arguments must be a multiple of three, as \
                         station, dates, and levels.")
        
    fig = make_subplots(rows=len(argv)//3, cols=1, shared_xaxes=True)
    
    for i in range(len(argv)//3):
        # initialize values to plot
        station = argv[3*i]
        dates = argv[3*i+1]
        levels = argv[3*i+2]
        print(i, station.name)
        
        fig.add_trace(go.Scatter(x=dates, y=levels,
                                 mode='lines', name='Water level', 
                                 showlegend=(i==0), legendgroup="level"),
                         row=i+1, col=1)
        fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                                 y=[station.typical_range[0], station.typical_range[0]],
                                 mode='lines', name='Typical low level', 
                                 showlegend=(i==0), legendgroup="low"),
                         row=i+1, col=1)
        fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                                 y=[station.typical_range[1], station.typical_range[1]],
                                 mode='lines', name='Typical high level', 
                                 showlegend=(i==0), legendgroup="high"),
                         row=i+1, col=1)
        fig.update_yaxes(range=[min(0, min(levels), station.typical_range[0])-0.1, 
                                max(1, max(levels), station.typical_range[1])+0.1],
                         row=i+1, col=1)
        
    fig.update_layout(xaxis_title="Dates",
                      yaxis_title="Water Level")
    plot(fig, auto_open=True)