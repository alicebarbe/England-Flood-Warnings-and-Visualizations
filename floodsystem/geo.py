# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from haversine import haversine
from floodsystem.utils import sorted_by_key  # noqa
from floodsystem.stationdata import build_station_list


def stations_by_distance(stations, p):
    """Calculate distances from a coordinate p to each station. Return the station
    distance pairs in an ordered list, by distance.

    Arguments:
        stations (list of MonitoringStation): 
            generated using build_station_list.
        p (lat, lon): 
            float coordinates of the center.
            
    Returns:
        (station, distance) (MonitoringStation, float):
            pair of station object and the corresponding distance from it to point p
    """
    output = []
    for station in stations:
        # use haversine to calculate distance to p
        output.append((station, (haversine(station.coord, p))))
    return sorted_by_key(output, 1)


def stations_within_radius(stations, centre, r):
    """Return station/distance pair that are within radius r of center.
    
    Arguments:
        stations (list of MonitoringStation): 
            generated using build_station_list.
        p (lat, lon) (float, float): 
            float coordinates of the center.
        r (float):
            
            
    Returns:
        (station, distance) (MonitoringStation, float):
            pair of station object and the corresponding distance from it to point p
    """
    output = []
    for pair in stations_by_distance(stations, centre):
        # check if distance is within r of centre
        if pair[1] <= r:
            output.append(pair)
    return output


def rivers_with_stations(stations):
    """Return a set containing names of rivers with an associated monitoring station

    Arguments:
        stations (list of MonitoringStation):
            generated using build_station_list.

    Returns:
        {river_name} {string}
            A set containing the names of all the rivers with a monitoring station
    """

    output = set()
    for station in stations:
        # if the station has a river, add to the set
        if station.river:
            output.add(station.river)

    return output


def stations_by_river(stations):
    """Maps stations by the rivers which they are associated with. Return a dict
    containing MonitoringStations with key values for each river

    Arguments:
        stations (list of MonitoringStation):
            generated using build_station_list.

    Returns:
        {river_name : [MonitoringStations]} {string : [MonitoringStation]}
            dict containing lists of MonitoringStations for each river. The dict
            keys are the river names
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


def rivers_by_station_number(stations, N):
    """Finds the N rivers with the greatest number of stations. the rivers are
    returned in order of decreasing number of stations. If there is a tie between
     multiple rivers at the Nth entry, all rivers with equal number of stations
     are returned

    Arguments:
        stations (list of MonitoringStation):
            generated using build_station_list.

        N (int)
            The number of rivers to return, in descending order of number of
            stations

    Returns:
        (river_name, number_of_stations) (string, int)
            list of tuples containing the river names and number of stations
            of rivers with the N highest number of monitoring stations
    """
    river_station_nums = []
    river_stations = stations_by_river(stations)

    # find the number of stations next to each river, then sort rivers by this number
    for river, stations in river_stations.items():
        river_station_nums.append((river, len(stations)))
    output = sorted_by_key(river_station_nums, 1, reverse=True)

    # check for a tie condition at the end
    num_ties = 0
    while output[N - 1][1] == output[N + num_ties][1]:
        num_ties += 1

    return output[:(N + num_ties)]
