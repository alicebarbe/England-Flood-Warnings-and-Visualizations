# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot, iplot
import plotly.express as px
from floodsystem.analysis import polyfit
from ipywidgets import HBox


def create_water_levels_plot(listinput):
    """Plot the water levels of stations given corresponding date. Subplots are
    created for each station.
    
    Arguments:
        listinput (list): 
            list of station (MonitoringStation), dates (list), and
            levels (list), in this order. List must be of length multiple of 3.
            
    Returns:
        fig (plotly go.figure):
            plotly figure with water levels, high, and low plotted
    
    """
    if len(listinput) % 3 != 0:
        raise ValueError("Number of arguments must be a multiple of three, as \
                         station, dates, and levels.")

    fig = make_subplots(rows=len(listinput) // 3, cols=1, shared_xaxes=True,
                        subplot_titles=[station.name for station in listinput[::3]])

    for i in range(len(listinput) // 3):
        # initialize values to plot
        station = listinput[3 * i]
        dates = listinput[3 * i + 1]
        levels = listinput[3 * i + 2]

        # add traces: high, low, level
        fig.add_trace(go.Scatter(x=dates, y=levels,
                                 mode='lines', name='Water level',
                                 showlegend=(i == 0), legendgroup="level",
                                 line_color='blue'),
                      row=i + 1, col=1)
        fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                                 y=[station.typical_range[0], station.typical_range[0]],
                                 mode='lines', name='Typical low level',
                                 showlegend=(i == 0), legendgroup="low",
                                 line_color='green'),
                      row=i + 1, col=1)
        fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                                 y=[station.typical_range[1], station.typical_range[1]],
                                 mode='lines', name='Typical high level',
                                 showlegend=(i == 0), legendgroup="high",
                                 line_color='red'),
                      row=i + 1, col=1)
        fig.update_yaxes(range=[min(0, min(levels), station.typical_range[0]) - 0.1,
                                max(1, max(levels), station.typical_range[1]) + 0.1],
                         title_text="Water Level",
                         row=i + 1, col=1)
        # fig.update_xaxes(title_text="Dates", row=i+1, col=1)

    fig.update_layout(height=1000)
    return fig


def plot_water_levels(listinput):
    """Display plot generated in create_water_levels_plot

    Args:
        listinput: (list) list of station (MonitoringStation), dates (list), and
            levels (list), in this order. List must be of length multiple of 3.
    """
    fig = create_water_levels_plot(listinput)
    plot(fig, auto_open=True)


def plot_water_levels_with_fit(listinput, p):
    """Add best-fit line to water level graphs, and display them
    
    Arguments:
        listinput (list): 
            list of station (MonitoringStation), dates (list), and
            levels (list), in this order. List must be of length multiple of 3.
        p (integer):
            order of polynomial fit
    
    Returns:
        none; creates temp-plot.html file and auto-opens it.
    
    """
    fig = create_water_levels_plot(listinput)

    for i in range(len(listinput) // 3):
        # initialize values to plot
        dates = listinput[3 * i + 1]
        levels = listinput[3 * i + 2]

        poly, d0 = polyfit(dates, levels, p)

        # convert dates to minutes (integers), normalized to start at zero
        x = [date.timestamp() / 60 for date in dates]
        offset = d0.timestamp() / 60
        x = [a - offset for a in x]

        # calculate levels from fit
        x_levels = poly(x)

        # plot curve
        fig.add_trace(go.Scatter(x=dates, y=x_levels,
                                 mode='lines', name='Fitted water level',
                                 showlegend=(i == 0), legendgroup="fittedlevel",
                                 line_color='gray'),
                      row=i + 1, col=1)

    plot(fig, auto_open=True)


def on_flood_region_click():
    print('Click registered')


def map_flood_warnings(geojson, df, df2):
    """"Plots flood warnings as a chloropleth map figure
    Arguments:
        geojson: geo_json_object.
            Contains the perimeter definitions for all warnings. Created from
            warningdata.build_regions_geojson

        df: Pandas Dataframe.
            Contains information regarding the severity of the floods and the location name.
            Created using warningdata.build_severity_dataframe
    """
    colours = {'low': 'green', 'moderate': 'yellow', 'high': 'orange', 'severe': 'red'}

    if df.empty:
        print("Empty dataframe. Possibly no flood warnings at this time")
        return

    fig = go.Figure()
    fig.add_choroplethmapbox(geojson=geojson,
                             # colorscale=colours,
                             z=df.warning_severity,
                             # autocolorscale=False,
                             locations=df.id,
                             featureidkey="properties.FWS_TACODE",
                             # mapbox_style="carto-positron",
                             # hover_name=df.label,
                             # hover_data=[df.last_updated],
                             # colorscale=colours,
                             # opacity=0.4,
                             # center={"lat": 52.4, "lon": -1.5},
                             # zoom=6)
                             )

    fig.add_scattermapbox(lon=df2.lon, lat=df2.lat,
                          # color="continent",  # which column to use to set the color of markers
                          text=df2.name,
                          mode='markers'  # column added to hover information
                          )

    fig.update_layout(mapbox_style="carto-positron", margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True, visible=True)
    plot(fig, auto_open=True)


def map_flood_warnings_interactive(geojson, df):
    """"Plots flood warnings as a chloropleth map figure, with support for
    interactive actions, such as click events
    Arguments:
        geojson: geo_json_object.
            Contains the perimeter definitions for all warnings. Created from
            warningdata.build_regions_geojson

        df: Pandas Dataframe.
            Contains information regarding the severity of the floods and the location name.
            Created using warningdata.build_severity_dataframe
    """
    colours = {'low': 'green', 'moderate': 'yellow', 'high': 'orange', 'severe': 'red'}

    if df.empty:
        print("Empty dataframe. Possibly no flood warnings at this time")
        return

    fig = go.FigureWidget(px.choropleth_mapbox(df,
                                               geojson=geojson,
                                               color="severity",
                                               locations="id",
                                               featureidkey="properties.FWS_TACODE",
                                               mapbox_style="carto-positron",
                                               hover_name="label",
                                               hover_data=['last_updated'],
                                               color_discrete_map=colours,
                                               opacity=0.4,
                                               center={"lat": 52.4, "lon": -1.5},
                                               zoom=6))

    fig.data[0].on_click(on_flood_region_click)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True, visible=True)
    plot(fig)


def get_recommended_simplification_params(warning_len):
    """"Returns the recommended geometry simplification tolerance and buffer, based
    on the number of warnings present. These settings are designed to prevent the map
    interface from lagging if many warnings are present

    Arguments:
        warning_len: int.
            The number of warnings in the warning list

    Returns:
        simplification params: {'tol': float, 'buf': float}.
            Parameters which determine the degree of shape approximation
            recommended for mapping
    """

    if warning_len < 10:
        return {'tol': 0.000, 'buf': 0.000}
    else:
        tol = (round(warning_len, -1) - 10) * 0.00005
        buf = (round(warning_len, -1) - 10) * 0.0001

        return {'tol': tol, 'buf': buf}
