"""Visualizations of historical data, flooding zones, and stations."""

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot
from floodsystem.analysis import polyfit
from floodsystem.warning import SeverityLevel
import numpy as np


def create_water_levels_plot(listinput):
    """Plot the water levels of stations given corresponding date.

    Subplots are created for each station.

    Parameters
    ----------
    listinput : list
        list of station (MonitoringStation), dates (list), and
            levels (list), in this order. List must be of length multiple of 3.

    Raises
    ------
    ValueError
        when listinput is not of length multiple of three.

    Returns
    -------
    fig : plotly.graph_objects.figure
        plotly figure with water levels, high, and low plotted.

    """
    if len(listinput) % 3 != 0:
        raise ValueError("Number of arguments must be a multiple of three, as \
                         station, dates, and levels.")

    fig = make_subplots(rows=len(listinput) // 3, cols=1, shared_xaxes=True,
                        subplot_titles=[station.name
                                        for station in listinput[::3]])

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
                                 y=[station.typical_range[0],
                                    station.typical_range[0]],
                                 mode='lines', name='Typical low level',
                                 showlegend=(i == 0), legendgroup="low",
                                 line_color='green'),
                      row=i + 1, col=1)
        fig.add_trace(go.Scatter(x=[min(dates), max(dates)],
                                 y=[station.typical_range[1],
                                    station.typical_range[1]],
                                 mode='lines', name='Typical high level',
                                 showlegend=(i == 0), legendgroup="high",
                                 line_color='red'),
                      row=i + 1, col=1)
        fig.update_yaxes(range=[min(0, min(levels),
                                    station.typical_range[0]) - 0.1,
                                max(1, max(levels),
                                    station.typical_range[1]) + 0.1],
                         title_text="Water Level",
                         row=i + 1, col=1)
        # fig.update_xaxes(title_text="Dates", row=i+1, col=1)

    fig.update_layout(height=1000)
    return fig


def plot_water_levels(listinput):
    """Display plot generated in create_water_levels_plot.

    Parameters
    ----------
    listinput : list
        list of station (MonitoringStation), dates (list), and levels (list),
        in this order. List must be of length multiple of 3.

    Returns
    -------
    None.

    """
    fig = create_water_levels_plot(listinput)
    plot(fig, auto_open=True)


def plot_water_levels_with_fit(listinput, p):
    """Add best-fit line to water level graphs, and display them.

    Parameters
    ----------
    listinput : list
        list of station (MonitoringStation), dates (list), and levels (list),
        in this order. List must be of length multiple of 3.
    p : int
        order of polynomial fit

    Returns
    -------
    None.

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
                                 showlegend=(i == 0),
                                 legendgroup="fittedlevel",
                                 line_color='gray'),
                      row=i + 1, col=1)

    plot(fig, auto_open=True)


def map_flood_warnings(geojson, warning_df=None,
                       min_severity=4, station_df=None):
    """Plot flood warnings and station levels as a chloropleth map figure.

    Parameters
    ----------
    geojson : geo_json
        Contains the perimeter definitions for all warnings. Created from
            warningdata.build_regions_geojson.
    warning_df : pandas.dataframe, optional
        Contains information regarding the severity of the floods and the
        location name. Created using warningdata.build_severity_dataframe.
        Defaults to None, where warnings are not mapped.
    station_df : pandas.dataframe, optional
         Contains information of position and relative water level of each
         station, to be plotted as a scatter map. Defaults to None, where
         stations are not mapped.
    min_severity : int, optional
        If provided, plots only warnings equal to or above this severity
        level Use SeverityLevel.value to obtain the integer value
        corresponding to a named severity level. default is 4 (all warnings
        plotted)

    Returns
    -------
    None.

    """
    colours = {'severe': 'rgb(41, 24, 107)',
               'high': 'rgb(18, 95, 142)',
               'moderate': 'rgb(65, 157, 133)',
               'low': 'rgb(160, 214, 91)'}

    hover_temp_choro = "<b>%{customdata[2]}</b><br>" \
                       "severity : %{customdata[0]}<br>" \
                       "last update : %{customdata[3]}<br><br>" \
                       "warning link : <a href='https://flood-warning-" \
                       "information.service.gov.uk/warnings?location=" \
                       "%{customdata[6]}'> %{customdata[6]}</a>"

    hover_temp_scatter = "<b>%{customdata[0]}</b><br>" \
                         "Water level : %{customdata[3]} m<br>" \
                         "Typical Range : %{customdata[5][0]}m - " \
                         "%{customdata[5][1]}m<br>" \
                         "Relative Level : %{customdata[4]:.3r}<br>" \
                         "Town : %{customdata[6]}"

    fig = go.Figure()

    if not (warning_df is None or warning_df.empty):
        # create discrete color scale, depending on severities plotted
        color_floats = np.linspace(0, min_severity, min_severity+1)/min_severity
        # TODO: color configs somewhere more global
        color_list = ["red", "orange", "yellow", "green"]
        colorscale = []
        # I thought I liked discrete bars
        for i in range(len(color_floats) - 1):
            colorscale.append((color_floats[i], color_list[i]))
            colorscale.append((color_floats[i+1], color_list[i]))
        # NVM I liked the continuous bar - comment this to go back to discrete
        colorscale = color_list[:min_severity]
        # TODO: replace with something more efficient, from the enum?
        #ticktext = ["severe", "high", "medium", "low"][:min_severity]
        ticktext = ["low", "medium", "high", "severe"][4-min_severity:]

        fig.add_choroplethmapbox(geojson=geojson,
                                 z=warning_df['int_severity'],
                                 zmax=min_severity+0.1,
                                 zmin=1-0.1,
                                 colorscale=colorscale,
                                 autocolorscale=False,

                                 colorbar_thickness=15,
                                 colorbar_outlinewidth=0,
                                 colorbar_tickvals=list(range(min_severity, 0, -1)),
                                 colorbar_ticktext=ticktext,
                                 #colorbar_tickangle=90,
                                 colorbar_tickmode="array",
                                 colorbar_x=0.01,
                                 colorbar_yanchor="bottom",
                                 colorbar_y=0,
                                 colorbar_title_text="Flood Warnings",

                                 locations=warning_df['id'],
                                 featureidkey="properties.FWS_TACODE",
                                 hovertemplate=hover_temp_choro,
                                 customdata=[row for _, row in
                                             warning_df.iterrows()],
                                 marker_opacity=0.6,
                                 # TODO: if I set linewidth to 0 it's pretty
                                 # but also impossible to click link because
                                 # the lines are super thin.
                                 marker_line_color='white',
                                 name="Flood Warning")

    if not (station_df is None or station_df.empty):
        # define the ranges of the level scale to discount any outliers
        min_lev = station_df.rel_level.mean() - station_df.rel_level.std()
        max_lev = station_df.rel_level.mean() + station_df.rel_level.std()

        # create map of stations
        fig.add_scattermapbox(lon=station_df.lon, lat=station_df.lat,
                              text=station_df.name,
                              mode='markers',  # hover information column
                              marker_color=station_df.rel_level,
                              marker_cmin=min_lev,
                              marker_cmax=max_lev,
                              #marker_colorscale='haline_r',
                              marker_colorscale='rdbu',
                              #marker_reversescale=True,
                              #marker_colorscale = [(0, "red"),   (0.33, "red"),
                              #                     (0.33, "green"), (0.66, "green"),
                              #                     (0.66, "blue"),  (1, "blue")],
                              marker_colorbar_thickness=15,
                              marker_colorbar_x=0.1,
                              marker_colorbar_title='Relative Water Level',
                              #marker_color=(round((station_df.rel_level),

                              customdata=[row for _, row in
                                          station_df.iterrows()],
                              hovertemplate=hover_temp_scatter,
                              name="Station",
                              )

    fig.update_layout(mapbox_style="carto-positron",
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_zoom=5.5,
                      mapbox_center={"lat": 53, "lon": -1.5},
                      showlegend=True,
                      legend_y=0.98,
                      legend_x=0.9,
                      legend_title="Click to display:")

    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True, visible=True)
    plot(fig, auto_open=True)


def get_recommended_simplification_params(warning_len):
    """Return the recommended geometry simplification tolerance and buffer.

    These settings are based on the number of warnings present, and designed
    to prevent the map interface from lagging if many warnings are present.

    Parameters
    ----------
    warning_len : int
        number of warnings in the warning list.

    Returns
    -------
    dict
        {'tol': float, 'buf': float}.
        Parameters which determine the degree of shape approximation
        recommended for mapping.

    """
    if warning_len < 10:
        return {'tol': 0.000, 'buf': 0.000}
    else:
        tol = (round(warning_len, -1) - 10) * 0.00005
        buf = (round(warning_len, -1) - 10) * 0.0001

        return {'tol': tol, 'buf': buf}
