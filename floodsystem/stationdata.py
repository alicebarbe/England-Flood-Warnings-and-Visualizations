# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Interface for extracting station data from JSON objects fetched from the
Internet."""

import pandas as pd

from floodsystem import datafetcher
from floodsystem.station import MonitoringStation


def build_station_list(use_cache=True, test=False):
    """Build and return a list of all river level monitoring stations
    based on data fetched from the Environment agency. Each station is
    represented as a MonitoringStation object.

    The available data for some station is incomplete or not
    available.

    If the flag test is set to true then fixed test data is used so
    results may be compared to known values for the data

    Parameters
    ----------
    use_cache : bool, optional
    test : bool, optional

    Returns
    -------
    stations : list of MonitoringStations

    """
    # Fetch station data - if testing use the fixed test data
    if test:
        data = datafetcher.fetch_test_station_data()
    else:
        data = datafetcher.fetch_station_data(use_cache)

    # Build list of MonitoringStation objects
    stations = []
    for e in data["items"]:
        # Extract town string (not always available)
        town = None
        if 'town' in e:
            town = e['town']

        # Extract river name (not always available)
        river = None
        if 'riverName' in e:
            river = e['riverName']

        # Attempt to extract typical range (low, high)
        try:
            typical_range = (float(e['stageScale']['typicalRangeLow']),
                             float(e['stageScale']['typicalRangeHigh']))
        except KeyError:
            typical_range = None

        try:
            # Create mesure station object if all required data is
            # available, and add to list
            s = MonitoringStation(
                station_id=e['@id'],
                measure_id=e['measures'][-1]['@id'],
                label=e['label'],
                coord=(float(e['lat']), float(e['long'])),
                typical_range=typical_range,
                river=river,
                town=town)
            stations.append(s)
        except KeyError:
            # Not all required data on the station was available, so
            # skip over
            pass

    return stations


def update_water_levels(stations, use_cache=False):
    """Attach level data contained in measure_data to stations."""
    # Fetch level data
    measure_data = datafetcher.fetch_latest_water_level_data(use_cache)

    # Build map from measure id to latest reading (value)
    measure_id_to_value = dict()
    for measure in measure_data['items']:
        if 'latestReading' in measure:
            latest_reading = measure['latestReading']
            measure_id = latest_reading['measure']
            measure_id_to_value[measure_id] = latest_reading['value']

    # Attach latest reading to station objects
    for station in stations:

        # Reset latestlevel
        station.latest_level = None

        # Attach new level data (if available)
        if station.measure_id in measure_id_to_value:
            if isinstance(measure_id_to_value[station.measure_id], float):
                station.latest_level = measure_id_to_value[station.measure_id]


def build_station_dataframe(stations):
    """Create a pandas DataFrame containing data for all monitoring stations.

    Parameters
    ----------
    stations : list of MonitoringStation
        generated using build_station_list.

    Returns
    -------
    df : pandas DataFrame
        the output dataframe.

    """
    df = pd.DataFrame()
    df['name'] = [(station.name if station.name is not None else "Unnamed")
                  for station in stations]
    df['lon'] = [(station.coord[1] if station.coord is not None else None)
                 for station in stations]
    df['lat'] = [(station.coord[0] if station.coord is not None else None)
                 for station in stations]
    df['level'] = [(station.latest_level if station.latest_level is not None
                    else "Not available") for station in stations]
    df['rel_level'] = [station.relative_water_level() if
                       station.relative_water_level() is not None else 0
                       for station in stations]

    return df
