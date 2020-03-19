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
        warnings: [FloodWarnings].
            The list of FloodWarning objects of severity greater than or equal to severity
    """
    data = datafetcher.fetch_flood_warnings(severity)

    if use_pickle_caches:
        polys = retrieve_pickle_cache('warning_polys.pk')
        areas = retrieve_pickle_cache('warning_areas.pk')

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
            # finds the first area in the cache which matches the warnings id, otherwise area is set to None
            area = next((a for a in areas if (a['items']['currentWarning']['floodAreaID'] == warning.id)), None)
            if area is not None:
                print('cache area found')
                warning.label = area['items']['label']
                warning.description = area['items']['description']
                warning.coord = (area['items']['lat'], area['items']['long'])

        if not warning.label or not warning.description:
            if '@id' in w['floodArea']:
                print("making area api call")
                flood_area = datafetcher.fetch_warning_area(w['floodArea']['@id'])

                warning.label = flood_area['items']['label']
                warning.description = flood_area['items']['description']
                warning.area_json = flood_area

        # attempts to set the poly based on a cached value, if not, pulls from the api
        if use_pickle_caches:
            # finds the first poly in the cache which matches the warnings id, otherwise poly is set to None
            poly = next((p for p in polys if (p[0][0]['properties']['FWS_TACODE'] == warning.id)), None)
            if poly is not None:
                warning.region = poly[1]
                warning.geojson = poly[0]
                warning.is_poly_simplified = poly[2]
                warning.simplified_geojson = poly[3]

        if not warning.region or not warning.geojson:
            if 'polygon' in w['floodArea']:
                print("making api call")
                poly = datafetcher.fetch_warning_region(w['floodArea']['polygon'])
                if poly is not None:
                    warning.region = [FloodWarning.geo_json_to_shape(p['geometry']) for p in poly]
                    warning.geojson = poly
                    warning.is_poly_simplified = {'tol': 0.000, 'buf': 0.000}
                    warning.simplified_geojson = poly

        if 'severityLevel' in w:
            warning.severity_lev = w['severityLevel']
            warning.severity = SeverityLevel(w['severityLevel'])

        if 'isTidal' in w:
            warning.tidal = w['isTidal']
        if 'message' in w:
            warning.message = w['message']

        warnings.append(warning)

    return warnings


def update_poly_area_caches(warnings, poly_cache='warning_polys.pk', area_cache='warning_areas.pk'):
    """Creates updated lists of polygons and areas pertaining to any new warnings.
    If previous cached data is available, the new data is appended to this.

    polygon data is stored as a list of lists containing four attributes for each warning, as shown below
    [[geojson, region, is_poly_simplified, simplified_geojson], ...]

    area data is stored as a list of json objects obtained from the API for each warning, as shown below
    [[area_json], ...]

    Arguments:
        warnings: [FloodWarnings].
            The list of FloodWarning objects of severity greater than or equal to severity

        poly_cache: string.
            The name of the polygon cache file. If no value is passed, defaults to 'warning_polys.pk'

        area_cache: string.
            The name of the area cache file. If no value is passed, defaults to 'warning_areas.pk'
    """

    # tries to retrieve all previously cached data, and adds on any
    polys = retrieve_pickle_cache(poly_cache)
    areas = retrieve_pickle_cache(area_cache)

    for warning in warnings:
        # if the warning id does not already have a corresponding polygon region cached, add it
        if not any((poly[0][0]['properties']['FWS_TACODE'] == warning.id) for poly in polys):
            if warning.geojson is not None and warning.region is not None:
                polys.append([warning.geojson, warning.region, warning.is_poly_simplified, warning.simplified_geojson])

        # if the warning id does not already have corresponding area data cached, add it
        if not any((area['items']['currentWarning']['floodAreaID'] == warning.id) for area in areas):
            if warning.area_json is not None:
                areas.append(warning.area_json)

    save_to_pickle_cache(poly_cache, polys)
    save_to_pickle_cache(area_cache, areas)


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
        geo = []
        # If available use the simplified geojson, otherwise use the raw
        if w.simplified_geojson is not None:
            geo = w.simplified_geojson
        elif w.geojson is not None:
            geo = w.geojson

        for feature in geo:
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

    df = pd.DataFrame(data_arr, columns=['severity', 'id', 'label', 'last_updated', 'warning_message', 'warning_severity'])
    return df
