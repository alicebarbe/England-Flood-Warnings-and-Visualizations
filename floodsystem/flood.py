from floodsystem.station import MonitoringStation
from floodsystem.utils import sorted_by_key


def stations_level_over_threshold(stations, tol):
    """Returns the stations whose relative water level exceeds
    the value of tol and the relative water levels of these stations.
    The stations are listed in order of decreasing relative water level

    Arguments:
        stations: (list of MonitoringStation).
            generated using build_station_list.
        tol:  float.
            All stations with relative water levels above tol are returned

    Returns:
        [(station, rel_water_level)]: [(MonitoringStation, float)].
            A list of tuples containing the MonitoringStation object
            and its relative water level
    """
    output = []

    for station in stations:
        relative_level = station.relative_water_level()

        if relative_level is not None:
            if relative_level > tol:
                output.append((station, relative_level))

    return sorted_by_key(output, 1, reverse=True)


def stations_highest_rel_level(stations, N):
    """Returns the N stations with the highest relative water levels,
     in descending order. Only N values are returned regarless of any
    tie conditions. Fewer than N may be returned if len(stations) < N

     Arguments:
         stations: (list of MonitoringStation).
            generated using build_station_list.
         N: int.
            Number of stations to returns

    Returns:
        [stations_with_highest_levels]: [MonitoringStation].
            List of MonitoringStation objects with the highest
            relative water levels
    """

    stations_ordered_by_level = sorted(stations, key=MonitoringStation.get_relative_water_level, reverse=True)
    return stations_ordered_by_level[:N]
