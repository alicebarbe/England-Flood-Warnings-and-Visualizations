# -*- coding: utf-8 -*-

from floodsystem.stationdata import build_station_list, \
    build_station_dataframe, update_water_levels
from floodsystem.warningdata import build_warning_list, build_regions_geojson,\
    build_severity_dataframe, update_poly_area_caches
from floodsystem.warning import FloodWarning, SeverityLevel
from floodsystem.plot import map_flood_warnings,\
    get_recommended_simplification_params


def run():
    """Requirements for task 2G"""

    # a severity of moderate includes all currently active flood warnings
    # severity.low includes warnings which were in force in the past 24 hours
    stations = build_station_list()
    update_water_levels(stations)

    severity = SeverityLevel.low

    print("Building warning list of severity {}...".format(severity.value))
    warnings = build_warning_list(severity.value)
    if len(warnings) == 0:
        print("No warnings of this severity")
        return

    print("Simplifying geometry...")
    simplification_params = get_recommended_simplification_params(len(warnings))

    for warning in warnings:
        # if the simplification parameters used for the cached file were
        # incorrect, resimplify the geometry
        if warning.is_poly_simplified != simplification_params:
            print('resimplifying')
            warning.simplify_geojson(tol=simplification_params['tol'],
                                     buf=simplification_params['buf'])
            warning.is_poly_simplified = simplification_params

    print("Making datasets...")
    geojson = build_regions_geojson(warnings)
    df = build_severity_dataframe(warnings)
    df2 = build_station_dataframe(stations)

    # we want the most severe warnings first - given that the list will be long
    sorted_warnings = FloodWarning.order_warning_list_with_severity(warnings)
    for warning in sorted_warnings:
        print(warning)
        print("\n")

    print("\n")
    print("Mapping warnings...")
    map_flood_warnings(geojson, warning_df=df, min_severity=severity.value,
                       station_df=df2)

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
    update_poly_area_caches(warnings)


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()
