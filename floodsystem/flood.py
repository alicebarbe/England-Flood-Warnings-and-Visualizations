from floodsystem.station import MonitoringStation
from floodsystem.utils import sorted_by_key


def stations_level_over_threshold(stations, tol):
    """Returns the stations whose relative water level exceeds
    the value of tol and the relative water levels of these stations.
    The stations are listed in order of decreasing relative water level

    Arguments:
        stations (list of MonitoringStation):
            generated using build_station_list.
        tol  float
            All stations with relative water levels above tol are returned

    Returns:
        [(station, rel_water_level)] [(MonitoringStation, float)]
            A list of tuples containing the MonitoringStation object
            and its relative water level
    """
    output = []

    for station in stations:
        if station.typical_range_consistent():
            relative_level = station.relative_water_level()

            if relative_level > tol:
                output.append((station, relative_level))

    return sorted_by_key(output, 1, reverse=True)
