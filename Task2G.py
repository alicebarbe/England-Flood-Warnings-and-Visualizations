# -*- coding: utf-8 -*-

from floodsystem.stationdata import build_station_list
from floodsystem.warningdata import build_warning_list, build_regions_geojson, build_severity_dataframe
from floodsystem.warning import FloodWarning, SeverityLevel
from floodsystem.plot import map_flood_warnings

from pprint import pprint
import matplotlib.pylab as plt

def run():
    """Requirements for task 2G"""

    severity = SeverityLevel.high

    stations = build_station_list()
    # a severity of moderate includes all active flood warnings
    warnings = build_warning_list(severity.value)
    for warning in warnings:
        warning.simplify_geojson(tol=0.001, buf=0.005, convex_hull=True)

    geojson = build_regions_geojson(warnings, 'test.json')
    df = build_severity_dataframe(warnings, severity.value)

    map_flood_warnings(geojson, df)

    # we want the most severe warnings first - given that the list will be long ...
    sorted_warnings = FloodWarning.order_warning_list_with_severity(warnings)
    for warning in sorted_warnings:
        print(warning)
        print("\n")

if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()
