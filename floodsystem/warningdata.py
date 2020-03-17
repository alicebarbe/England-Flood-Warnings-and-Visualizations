from floodsystem import datafetcher
from floodsystem.warning import FloodWarning, SeverityLevel
import pandas as pd
import json
import pickle
import os


def build_warning_list(severity, use_pickle_caches=True):
    """Fetch warnings from the API and create a list of warnings. Also updates caches
    for flood regions for any new warnings
    Arguments:
        severity: int.
            warnings above this minimum severity value (ie of lower numerical value) will be returned
        use_pickle_caches: bool.
            If true, then cached data regarding flood regions is used -
            the flood warnings are still the most recent pulled from the API

    Returns:
        (warnings, polys, areas): ([FloodWarnings] list list).
            A tuple containing the floodwarning list, as well as poly and area data to be cached
    """
    data = datafetcher.fetch_flood_warnings(severity)
    # lists to be cached - updates the cache regardless of use_pickle_caches
    polys_new = []
    areas_new = []

    if use_pickle_caches:
        polys = retrieve_pickle_cache('warning_polys.pk')
        areas = retrieve_pickle_cache('warning_areas.pk')
        for p, a in zip(polys, areas):
            polys_new.append(p)
            areas_new.append(a)

    warnings = []

    for w in data['items']:
        warning = FloodWarning()

        if 'floodAreaID' in w:
            warning.id = w['floodAreaID']
        if 'county' in w['floodArea']:
            warning.county = w['floodArea']['county']

        if 'timeMessageChanged' in w:
            warning.last_update = w['timeMessageChanged']

        # attempts to set the area based on a cached value, if not, pulls from the api
        if use_pickle_caches:
            for area in areas:
                if area['items']['currentWarning']['floodAreaID'] == warning.id:
                    print('cache area found')
                    warning.label = area['items']['label']
                    warning.description = area['items']['description']
                    warning.coord = (area['items']['lat'], area['items']['long'])
                    break

        if not warning.label or not warning.description:
            if '@id' in w['floodArea']:
                print("making area api call")
                flood_area = datafetcher.fetch_warning_area(w['floodArea']['@id'])
                warning.label = flood_area['items']['label']
                warning.description = flood_area['items']['description']
                areas_new.append(flood_area)

        # attempts to set the poly based on a cached value, if not, pulls from the api
        if use_pickle_caches:
            for poly in polys:
                if poly[0][0]['properties']['FWS_TACODE'] == warning.id:
                    print('cache found')
                    if poly is not None:
                        warning.region = poly[1]
                        warning.geojson = poly[0]
                        warning.is_poly_simplified = poly[2]

                    break

        if not warning.region or not warning.geojson:
            if 'polygon' in w['floodArea']:
                print("making api call")
                poly = datafetcher.fetch_warning_region(w['floodArea']['polygon'])
                if poly is not None:
                    warning.region = [FloodWarning.geo_json_to_shape(p['geometry']) for p in poly]
                    warning.geojson = poly
                    polys_new.append([warning.geojson, warning.region, warning.is_poly_simplified])

        if 'severityLevel' in w:
            warning.severity_lev = w['severityLevel']
            warning.severity = SeverityLevel(w['severityLevel'])

        if 'isTidal' in w:
            warning.tidal = w['isTidal']
        if 'message' in w:
            warning.message = w['message']

        warnings.append(warning)

    return warnings, polys_new, areas_new


def build_regions_geojson(warnings, file=None):
    """Creates a geoJSON FeatureCollection object for plotting flood warnings on a map
    Arguments:
        warnings: [FLoodWarnings].
            List of flood warnings

        file: string.
            For debug purposes, saves parameters data to a file, without any coordinates
            if file is a non-None string

    Returns:
        json_object: dictionary.
            The geoJSON object containing the regions of all the warnings in warnings
    """
    features = []
    features_without_coords = []

    for w in warnings:
        if w.geojson is not None:
            for feature in w.geojson:
                features.append(feature)
                # pprint(feature)
                if file is not None:
                    if 'geometry' in feature:
                        feature_without_coords = feature.copy().pop("geometry")
                    else:
                        feature_without_coords = feature.copy()
                    features_without_coords.append(feature_without_coords)

    data = {'type': 'FeatureCollection', 'features': features}

    # debugging - outputs the geojson to a file for verification
    if file is not None:
        with open(file, 'w') as out:
            data_without_coords = {'type': 'FeatureCollection', 'features': features_without_coords}
            json.dump(data_without_coords, out)

    return data


def retrieve_pickle_cache(filename):
    """"Reads a cached pickle file and returns the result.
    Args:
        filename: string.
            The name of the pickle file to be read. This file must be in the cache directory

    Returns:
        pickle_variables:
            The python variables read from the pickle file.
    """
    sub_dir = 'cache'
    cache_file = os.path.join(sub_dir, filename)

    try:
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
            f.close()
    except (pickle.UnpicklingError, FileNotFoundError):
        return []


def save_to_pickle_cache(filename, data):
    """"Saves data to a pickle cache file.
    Args:
        filename: string.
            The name of the pickle file to be saved. The file is placed
            in the cache directory.

        data:
            The data to be saved to a pickle file. Any Python variable
            type may be used
    """
    sub_dir = 'cache'
    try:
        os.makedirs(sub_dir)
    except FileExistsError:
        pass
    cache_file = os.path.join(sub_dir, filename)

    try:
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)
            f.close()
    except (pickle.UnpicklingError, FileNotFoundError):
        print('Error saving polygon data')


def build_severity_dataframe(warnings, min_severity):
    """Builds a pandas dataframe with data from the warnings, which is used to
    colour the map regions on a plot

    Arguments:
        warnings: [FLoodWarnings].
            List of flood warnings

        min_severity: int.
            The minimum severity value for which to add warnings to the dataframe

    Returns:
        data_frame: DataFrame.
            Pandas DataFrame with the relevant data
    """
    data_arr = []

    for w in warnings:
        if w.severity is not None:
            if w.severity.value <= min_severity:
                l = "Not available"
                last_update = "Not available"
                message = "Not available"
                warning_id = "Not available"
                warning_severity = 4

                if w.label is not None:
                    l = w.label
                if w.last_update is not None:
                    last_update = w.last_update
                if w.description is not None:
                    message = w.message
                if w.id is not None:
                    warning_id = w.id
                if w.severity_lev is not None:
                    warning_severity = w.severity_lev

                data_arr.append([w.severity.name, warning_id, l, last_update, message, warning_severity])

    return pd.DataFrame(data_arr, columns=['severity', 'id', 'label', 'last_updated', 'warning_message', 'warning_severity'])

def build_station_dataframe(stations):

    df = pd.DataFrame()

    df['name'] = [station.name for station in stations]
    df['lon'] = [station.coord[1] for station in stations]
    df['lat'] = [station.coord[0] for station in stations]
    df['level'] = [station.latest_level for station in stations]

    return df
