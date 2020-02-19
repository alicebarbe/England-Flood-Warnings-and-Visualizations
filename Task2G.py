# -*- coding: utf-8 -*-

from floodsystem.stationdata import build_station_list
from floodsystem.warningdata import build_warning_list
from floodsystem.warning import FloodWarning, SeverityLevel

def run():
    severity = SeverityLevel.severe

    stations = build_station_list()
    # a severity of 3 includes all active flood warnings
    warnings = build_warning_list(1)

    relevant_warnings = []

    for warning in warnings:
        warning.find_towns_affected(stations)
        if repr(warning.severity) <= repr(severity):
            relevant_warnings.append(warning)

    # we want the most severe warnings first - given that the list will be long ...
    sorted_warnings = FloodWarning.order_warning_list_with_severity(warnings)
    for warning in sorted_warnings:
        print(warning)
        print("\n")


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()
