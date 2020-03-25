"""Flood warning system extension demo code."""

import argparse
from progressbar import ProgressBar
from floodsystem.stationdata import build_station_list, \
    build_station_dataframe, update_water_levels
from floodsystem.warningdata import build_warning_list, build_regions_geojson,\
    build_severity_dataframe, update_poly_area_caches
from floodsystem.warning import FloodWarning, SeverityLevel
from floodsystem.plot import map_flood_warnings, \
    get_recommended_simplification_params


def run(severity, coords, plot_warnings, plot_stations, print_messages,
        overwrite_cache, simpl_params):

    warning_df = None
    station_df = None
    geojson = []
    warnings = []

    if plot_warnings or print_messages or overwrite_cache:
        # create warning list of the required severity level
        print("building warning list for {} severity warnings..."
              .format(severity.name))
        warnings = build_warning_list(severity.value, progress_bar=True)
        if len(warnings) == 0:
            print("No warnings of this severity available")
        print("")

        if plot_warnings or overwrite_cache:
            # if we are plotting the warnings or updating the cache the warning
            # geometry should be simplified
            print("Simplifying geometry...")
            bar = ProgressBar(max_value=len(warnings)).start()
            # if the simplification parameters were not explicitly specified,
            # uses the recommended ones
            if simpl_params is None:
                simpl_params = get_recommended_simplification_params(len(warnings))

            for progress_count, warning in enumerate(warnings):
                # if the cached geometry was simplified differently, resimplify
                if warning.is_poly_simplified != simpl_params:
                    warning.simplify_geojson(tol=simpl_params['tol'],
                                             buf=simpl_params['buf'])
                    warning.is_poly_simplified = simpl_params
                bar.update(progress_count)
            bar.finish()
            print("")

            if plot_warnings:
                # if we are plotting, build a dataframe and geojson object
                # containing information about each warnings and its geometry
                warning_df = build_severity_dataframe(warnings)
                geojson = build_regions_geojson(warnings)

            print("Saving caches...")
            update_poly_area_caches(warnings, overwrite=overwrite_cache)

    if plot_stations:
        print("Building station list and updating water levels...")
        stations = build_station_list()
        update_water_levels(stations)

        station_df = build_station_dataframe(stations)

    # mapping if there is anything to map
    if plot_warnings or plot_stations:
        print("Mapping...")
        map_flood_warnings(geojson, warning_df=warning_df,
                           min_severity=severity.value, station_df=station_df)

    if print_messages:
        # we want the most severe warnings last - the list will be long
        print("\n")
        sorted_warnings = FloodWarning.order_warning_list_with_severity(warnings)
        for warning in sorted_warnings:
            print(warning)
            print("")

    # checks for flood warnings in the specified location
    if coords is not None:
        print("Checking for warnings at (lat: {}, long: {})".format(coords[0],
                                                                    coords[1]))

        warnings_here = FloodWarning.check_warnings_at_location(warnings,
                                                                coords)
        if len(warnings_here) == 0:
            print("No flood warnings in this location")
        else:
            print("The following warnings apply to this location")
            for warning in warnings_here:
                print(warning)
                print("\n")

    print("Done")


if __name__ == "__main__":
    print("*** Extension Demonstration Script ***")
    print("")

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
                             "option fully rebuilds the cache. ")

    parser.add_argument("-dm" "--disable-warning-messages",
                        action='store_true', dest='disable_warning_messages',
                        help="disables printing detailed flood warning "
                             "messages")

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
        not args.disable_warning_messages,
        args.overwrite_warning_cache,
        simplification_params)
