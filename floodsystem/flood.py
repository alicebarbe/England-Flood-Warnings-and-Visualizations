from floodsystem.station import MonitoringStation
from floodsystem.utils import sorted_by_key


def stations_level_over_threshold(stations, tol):
    output = []

    for station in stations:
        if station.typical_range_consistent():
            relative_level = station.relative_water_level()

            if relative_level >= tol:
                output.append((station, relative_level))

    return sorted_by_key(output, 1, reverse=True)
