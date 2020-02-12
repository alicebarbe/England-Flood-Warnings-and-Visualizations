# -*- coding: utf-8 -*-
#from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot

def plot_water_levels(listinput):
    """Plot the water levels of stations given corresponding date. Subplots are
    created for each station.
    
    Arguments:
        listinput (list): 
            list of station (MonitoringStation), dates (list), and
            levels (list), in this order. List must be of length multiple of 3.
            
    Returns:
        none; creates temp-plot.html file and auto-opens it.
    
    """ 
    if len(listinput) % 3 != 0:
        raise ValueError("Number of arguments must be a multiple of three, as \
                         station, dates, and levels.")
        
    fig = make_subplots(rows=len(listinput)//3, cols=1, shared_xaxes=True,
                        subplot_titles=[station.name for station in listinput[::3]])
    
    for i in range(len(listinput)//3):
        # initialize values to plot
        station = listinput[3*i]
        dates = listinput[3*i+1]
        levels = listinput[3*i+2]
        
        # add traces: high, low, level
        fig.add_trace(go.Scatter(x=dates, y=levels,
                                 mode='lines', name='Water level', 
                                 showlegend=(i==0), legendgroup="level",
                                 line_color='blue'),
                      row=i+1, col=1)
        fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                                 y=[station.typical_range[0], station.typical_range[0]],
                                 mode='lines', name='Typical low level', 
                                 showlegend=(i==0), legendgroup="low", 
                                 line_color='green'),
                      row=i+1, col=1)
        fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                                 y=[station.typical_range[1], station.typical_range[1]],
                                 mode='lines', name='Typical high level', 
                                 showlegend=(i==0), legendgroup="high",
                                 line_color='red'),
                      row=i+1, col=1)
        fig.update_yaxes(range=[min(0, min(levels), station.typical_range[0])-0.1, 
                                max(1, max(levels), station.typical_range[1])+0.1],
                         title_text="Water Level",
                      row=i+1, col=1)
        #fig.update_xaxes(title_text="Dates", row=i+1, col=1)
    fig.update_layout(height=1000)
    plot(fig, auto_open=True)