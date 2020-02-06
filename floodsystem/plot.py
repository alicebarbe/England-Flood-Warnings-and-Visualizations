# -*- coding: utf-8 -*-
#from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.offline import plot

def plot_water_levels(station, dates, levels):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=levels,
                             mode='lines', name='Water level'))
    fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                             y=[station.typical_range[0], station.typical_range[0]],
                             mode='lines', name='Typical low level'))
    fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                             y=[station.typical_range[1], station.typical_range[1]],
                             mode='lines', name='Typical high level'))
    
    fig.update_layout(title=station.name,
                      xaxis_title="Dates",
                      yaxis_title="Water Level")
    fig.update_yaxes(range=[min(0, min(levels)-0.1), max(1, max(levels)+0.1)])
    plot(fig, auto_open=True)