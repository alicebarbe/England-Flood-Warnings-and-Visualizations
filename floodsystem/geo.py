# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Collection of functions related to geographical data."""

from haversine import haversine
from floodsystem.utils import sorted_by_key  # noqa


def stations_by_distance(stations, p):
    """Calculate distances from stations to a coordinate p.

    Parameters
    ----------
    stations : list[MonitoringStation]
        generated using build_station_list.
    p : float
        coordinates of the center.

    Returns
    -------
    (MonitoringStation, float)
        pair of station object and the corresponding distance from it to point
        p.

    """
    output = []
    for station in stations:
        # use haversine to calculate distance to p
        output.append((station, (haversine(station.coord, p))))
    return sorted_by_key(output, 1)


def stations_within_radius(stations, centre, r):
    """Return station/distance pair that are within radius r of center.

    Parameters
    ----------
    stations : list[MonitoringStation]
        generated using build_station_list.
    centre : (float, float)
        float coordinates of the center.
    r : float
        radius from center.

    Returns
    -------
    output : list[MonitoringStation]
        list of station objects.

    """
    output = []
    for pair in stations_by_distance(stations, centre):
        # check if distance is within r of centre
        if pair[1] <= r:
            output.append(pair[0])
    return output


def rivers_with_stations(stations):
    """Get names of rivers with an associated monitoring station.

    Parameters
    ----------
    stations : list[MonitoringStation]
        generated using build_station_list.

    Returns
    -------
    output : set
        A set containing the names of all the rivers with a monitoring station.

    """
    output = set()
    for station in stations:
        # if the station has a river, add to the set
        if station.river:
            output.add(station.river)

    return output


def stations_by_river(stations):
    """Map stations to the rivers which they are associated with.

    Parameters
    ----------
    stations : list[MonitoringStation]
        generated using build_station_list..

    Returns
    -------
    output : dict()
        {river_name : [MonitoringStations]}: {string : [MonitoringStation]}.
        dict containing lists of MonitoringStations for each river. The dict
        keys are the river names.

    """
    output = {}
    rivers = rivers_with_stations(stations)

    for river in rivers:
        stations_with_river = []

        for station in stations:
            if river == station.river:
                stations_with_river.append(station)

        output[river] = stations_with_river

    return output


def rivers_by_station_number(stations_list, N):
    """Find the N rivers with the greatest number of stations.

    The rivers are returned in order of decreasing number of stations.
    If there is a tie between multiple rivers at the Nth entry, all rivers
    with equal number of stations are returned.

    Parameters
    ----------
    stations : list[MonitoringStation]
        generated using build_station_list.
    N : int
        The number of rivers to return, in descending order of number of
        stations

    Returns
    -------
    list[(string, int)]
        list of tuples containing the river names and number of stations
        of rivers with the N highest number of monitoring stations.

    """
    river_station_nums = []
    river_stations = stations_by_river(stations_list)

    # find the number of stations next to each river, then sort rivers
    for river, stations in river_stations.items():
        # Append to the list tuples of the form (river_name,number_of_stations)
        river_station_nums.append((river, len(stations)))
    output = sorted_by_key(river_station_nums, 1, reverse=True)

    # check for a tie condition at the end
    num_ties = 0
    while output[N - 1][1] == output[N + num_ties][1]:
        num_ties += 1

    return output[:(N + num_ties)]
