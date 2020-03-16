# -*- coding: utf-8 -*-

from floodsystem.stationdata import build_station_list
from floodsystem.warningdata import build_warning_list, build_regions_geojson, build_severity_dataframe, save_to_pickle_cache
from floodsystem.warning import FloodWarning, SeverityLevel
from floodsystem.plot import map_flood_warnings, map_flood_warnings_interactive


def run():
    """Requirements for task 2G"""

    # a severity of moderate includes all currently active flood warnings
    # severity.low includes warnings which were in force in the past 24 hours
    severity = SeverityLevel.high

    print("Building warning list of severity {}...".format(severity.value))
    warnings, polys, areas = build_warning_list(severity.value)
    if len(warnings) == 0:
        print("No warnings of this severity")
        return

    print("Simplifying geometry...")
    for warning in warnings:
        if not warning.is_poly_simplified:
            warning.simplify_geojson(tol=0.005, buf=0.002, convex=True)

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
    map_flood_warnings_interactive(geojson, df)

    print("Checking for warnings in Jesus College, Cambridge ...")
    jc_coords = (52.20527, 0.120705)
    warnings_here = FloodWarning.check_warnings_at_location(warnings, jc_coords)
    if len(warnings_here) == 0:
        print("No flood warnings in this location")
    else:
        print("The following warnings apply to this location")
        for warning in warnings_here:
            print(warning)
            print("\n")

    print("Saving caches...")
    save_to_pickle_cache('warning_polys.pk', polys)
    save_to_pickle_cache('warning_areas.pk', areas)


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()
