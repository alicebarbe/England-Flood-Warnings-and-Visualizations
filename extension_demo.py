from floodsystem.stationdata import build_station_list, \
    build_station_dataframe, update_water_levels
from floodsystem.warningdata import build_warning_list, build_regions_geojson,\
    build_severity_dataframe, update_poly_area_caches
from floodsystem.warning import FloodWarning, SeverityLevel
from floodsystem.plot import map_flood_warnings, \
    get_recommended_simplification_params

import argparse


def run(severity, coords, plot_warnings, plot_stations, overwrite_cache,
        simplification_params):
    """Flood warning system extension demo code"""

    warning_df = None
    station_df = None
    geojson = []

    warnings = []

    if plot_warnings:
        print("Building warning list of severity {}...".format(severity.value))
        warnings = build_warning_list(severity.value)
        if len(warnings) == 0:
            print("No warnings of this severity available")

        print("Simplifying geometry...")
        if simplification_params is None:
            simplification_params = get_recommended_simplification_params(len(warnings))

        for warning in warnings:
            # if the cached geometry was simplified differently, resimplify it
            if warning.is_poly_simplified != simplification_params:
                warning.simplify_geojson(tol=simplification_params['tol'],
                                         buf=simplification_params['buf'])
                warning.is_poly_simplified = simplification_params

        warning_df = build_severity_dataframe(warnings)
        geojson = build_regions_geojson(warnings)

    if plot_stations:
        stations = build_station_list()
        update_water_levels(stations)

        station_df = build_station_dataframe(stations)

    # print warnings
    # we want the most severe warnings first - given that the list will be long
    print("\n")
    sorted_warnings = FloodWarning.order_warning_list_with_severity(warnings)
    for warning in sorted_warnings:
        print(warning)
        print("")

    print("Mapping ...")
    map_flood_warnings(geojson, warning_df=warning_df,
                       min_severity=severity.value, station_df=station_df)

    # checks for flood warnings in the specified location
    if coords is None:
        print("Checking for warnings in Jesus College, Cambridge ...")
        coords = (52.20527, 0.120705)

    else:
        print("Checking for warnings at (lat: {}, long: {})".format(coords[0],
                                                                    coords[1]))

    warnings_here = FloodWarning.check_warnings_at_location(warnings, coords)
    if len(warnings_here) == 0:
        print("No flood warnings in this location")
    else:
        print("The following warnings apply to this location")
        for warning in warnings_here:
            print(warning)
            print("\n")

    print("Saving caches...")
    update_poly_area_caches(warnings, overwrite_cache=overwrite_cache)


if __name__ == "__main__":
    print("*** Extension Demonstration Script ***")
    severity_levels = [s.name for s in SeverityLevel]

    # collect and parse command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--warning-min-severity", type=str, default="low",
                        choices=severity_levels, dest='warning_min_severity',
                        help="Fetches warnings only of the given severity "
                             "level or greater. Must be one of {}. Warnings of"
                             " severity moderate and above are active "
                             "currently, while low severity warnings were "
                             "active in the past 24 "
                             "hours".format(severity_levels))

    parser.add_argument("-lat", "--latitude", type=float, default=None,
                        help="The latitude, in degrees of a location to be "
                             "checked for any flood warnigns.")
    parser.add_argument("-long", "--longitude", type=float, default=None,
                        help="The longitude, in degrees of a location to be "
                            "checked for any flood warnigns.")

    parser.add_argument("-c", "--overwrite-warning-cache", action='store_true',
                        dest='overwrite_warning_cache',
                        help="If true, pulls all data on flood " 
                              "warning regions and rewrites cache " 
                              "files. Note warnings which have" 
                              "changed are always updated, this"  
                              "option fully rebuilds the cache")

    parser.add_argument("-dw", "--disable-plot-warnings", action='store_true',
                        dest='disable_plot_warnings',
                        help="disables plotting of warnings on a choropleth "
                             "map.")
    parser.add_argument("-ds", "--disable-plot-stations", action='store_true',
                        dest='disable_plot_stations',
                        help="disables plotting of station locations and their"
                             " relative water levels on a map")

    parser.add_argument("-tol", "--geometry-tolerance", type=float,
                        default=None, dest='geometry_tolerance',
                        help="Simplifies warning region geometry before "
                             "plotting to keep the map responsive. The "
                             "tolerance is given in degrees and sets the "
                             "maximum allowed deviation of the approximated "
                             "geometry from the true shape. By default, "
                             "settings which provide detailed warning regions "
                             "and keep the map responsive are used")
    parser.add_argument("-buf", "--geometry_buffer", type=float, default=None,
                        help="Simplifies warning region geometry before "
                             "plotting to keep the map responsive. The buffer "
                             "smoothes geometry and removes any voids by "
                             "taking the locus of the shape offset by a fixed "
                             "value, in degrees. By default, settings which "
                             "provide detailed warning regions and keep the "
                             "map responsive are used")

    args = parser.parse_args()

    # process the command line inputs
    coords = None
    if args.latitude is not None and args.longitude is not None:
        coords = (args.latitude, args.longitude)

    simplification_params = None
    if not (args.geometry_tolerance is None or args.geometry_buffer is None):
        simplification_params = {'tol': args.geometry_tolerance,
                                 'buf': args.geometry_buffer}

    # run the demo
    run(SeverityLevel[args.warning_min_severity],
        coords,
        not args.disable_plot_warnings,
        not args.disable_plot_stations,
        args.overwrite_warning_cache,
        simplification_params)