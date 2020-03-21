"""Methods to determine risk of flood at stations."""

from floodsystem.station import MonitoringStation
from floodsystem.utils import sorted_by_key


def stations_level_over_threshold(stations, tol):
    """Return the stations whose relative water level exceed a threshold.

    The stations are listed in order of decreasing relative water level.

    Parameters
    ----------
    stations : list[MonitoringStation]
    tol : float
        threshold for relative water level

    Returns
    -------
    list[(MonitoringStation, float)]
        A list of tuples containing the MonitoringStation object and its
        relative water level.

    """
    output = []

    for station in stations:
        relative_level = station.relative_water_level()

        if relative_level is not None:
            if relative_level > tol:
                output.append((station, relative_level))

    return sorted_by_key(output, 1, reverse=True)


def stations_highest_rel_level(stations, N):
    """Return the N stations with the highest relative water levels.

    Only N values are returned regarless of any tie conditions.
    Fewer than N may be returned if len(stations) < N


    Parameters
    ----------
    stations : list[MonitoringStation]
        generated using build_station_list..
    N : int
        Number of stations to returns.

    Returns
    -------
    list[MonitoringStation]
        List of MonitoringStation objects with the highest relative water
        levels.

    """
    stations_ordered_by_level = sorted(stations,
        key=MonitoringStation.get_relative_water_level, reverse=True)
    return stations_ordered_by_level[:N]
