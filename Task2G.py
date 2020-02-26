# -*- coding: utf-8 -*-

from floodsystem.stationdata import build_station_list
from floodsystem.warningdata import build_warning_list, build_regions_geojson, build_severity_dataframe, save_to_pickle_cache
from floodsystem.warning import FloodWarning, SeverityLevel
from floodsystem.plot import map_flood_warnings


def run():
    """Requirements for task 2G"""

    # a severity of moderate includes all currently active flood warnings
    # severity.low includes warnings which were in force in the past
    severity = SeverityLevel.high

    print("Building warning list...")
    warnings, polys, areas = build_warning_list(severity.value)

    print("Simplifying geometry...")
    for warning in warnings:
        if not warning.is_poly_simplified:
            warning.simplify_geojson(tol=0., buf=0.002, convex=True)

    print("Making datasets...")
    geojson = build_regions_geojson(warnings)
    df = build_severity_dataframe(warnings, severity.value)

    # we want the most severe warnings first - given that the list will be long ...
    sorted_warnings = FloodWarning.order_warning_list_with_severity(warnings)
    for warning in sorted_warnings:
        print(warning)
        print("\n")

    print("\n")
    print("Mapping warnings...")
    map_flood_warnings(geojson, df)

    print("Saving caches...")
    save_to_pickle_cache('warning_polys.pk', polys)
    save_to_pickle_cache('warning_areas.pk', areas)



if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()
