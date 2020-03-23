# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 14:45:16 2020

@author: Alice
"""

import plotly.graph_objects as go
from plotly.offline import plot, iplot
import plotly.express as px
import numpy as np
"""
colors = px.colors.named_colorscales()
for color in colors:
    y = np.random.randn(500)
    fig = go.Figure(data=go.Scatter(
        y = y,
        mode='markers',
        marker=dict(
            size=16,
            color=y, #set color equal to a variable
            colorscale=color, # one of plotly colorscales
            showscale=True
        )
    ))
    fig.update_layout(title=color)
    iplot(fig)
"""
