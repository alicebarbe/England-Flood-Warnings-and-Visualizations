"""Framework to import, cache, and use flood warning and corresponding data."""

import json
import pickle
import os
import pandas as pd
from progressbar import ProgressBar
from floodsystem import datafetcher
from floodsystem.warning import FloodWarning, SeverityLevel


def build_warning_list(severity, use_pickle_caches=True, progress_bar=False):
    """Fetch warnings from the API and create a list of warnings.

    Also updates caches for flood regions for any new warnings.

    Parameters
    ----------
    severity : int
        warnings above this minimum severity value (ie of lower numerical
        value) will be returned.
    use_pickle_caches : bool, optional
        If true, then cached data regarding flood regions is used - the flood
        warnings are still the most recent pulled from the API. The default is
        True.
    progress_bar : bool, optional
        If supplied, creates a bar in the terminal and updates as the warning
        list is built. The defualt is False

    Returns
    -------
    warnings : list[FloodWarning]
        The list of FloodWarning objects of severity greater than or equal to
        severity.

    """
    data = datafetcher.fetch_flood_warnings(severity)

    if use_pickle_caches:
        polys = retrieve_pickle_cache('warning_polys.pk')
        areas = retrieve_pickle_cache('warning_areas.pk')

    warnings = []

    if progress_bar:
        bar = ProgressBar(marker='=', max_value=len(data['items'])).start()

    for progress_count, w in enumerate(data['items']):
        warning = FloodWarning()

        if 'floodAreaID' in w:
            warning.id = w['floodAreaID']
        if 'county' in w['floodArea']:
            warning.county = w['floodArea']['county']

        if 'timeMessageChanged' in w:
            warning.last_update = w['timeMessageChanged']

        # attempts to set the area based on a cached value, if not,
        # pulls from the api
        if use_pickle_caches:
            # finds the first area in the cache which matches the warnings id,
            # otherwise area is set to None
            area = next((a for a in areas if
                         (a['items']['currentWarning']['floodAreaID']
                          == warning.id)), None)
            if area is not None:
                warning.label = area['items']['label']
                warning.description = area['items']['description']
                warning.coord = (area['items']['lat'], area['items']['long'])

        if not warning.label or not warning.description:
            if '@id' in w['floodArea']:
                flood_area = datafetcher.fetch_warning_area(w['floodArea']['@id'])

                warning.label = flood_area['items']['label']
                warning.description = flood_area['items']['description']
                warning.area_json = flood_area

        # attempts to set the poly based on a cached value, if not,
        # pulls from the api
        if use_pickle_caches:
            # finds the first poly in the cache which matches the warnings id,
            # otherwise poly is set to None
            poly = next((p for p in polys if
                         (p[0][0]['properties']['FWS_TACODE'] == warning.id)),
                        None)
            if poly is not None:
                warning.region = poly[1]
                warning.geojson = poly[0]
                warning.is_poly_simplified = poly[2]
                warning.simplified_geojson = poly[3]

        if not warning.region or not warning.geojson:
            if 'polygon' in w['floodArea']:
                poly = datafetcher.fetch_warning_region(w['floodArea']['polygon'])
                if poly is not None:
                    warning.region = [FloodWarning.geo_json_to_shape(p['geometry'])
                                      for p in poly]
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

        if progress_bar:
            bar.update(progress_count)

    if progress_bar:
        bar.finish()

    return warnings


def update_poly_area_caches(warnings, poly_cache='warning_polys.pk',
                            area_cache='warning_areas.pk', overwrite=False):
    """Create updated lists of polygons/areas pertaining to any new warnings.

    If previous cached data is available, and overwrite is false the new data
    is appended to this. polygon data is stored as a list of lists containing
    four attributes for each warning:
    [[geojson, region, is_poly_simplified, simplified_geojson], ...]

    area data is stored as a list of json objects obtained from the API for
    each warning: [[area_json], ...]

    Parameters
    ----------
    warnings : list[FLoodWarnings]
        The list of FloodWarning objects of severity greater than or equal to
        severity.
    poly_cache : string, optional
        The name of the polygon cache file. The default is 'warning_polys.pk'.
    area_cache : string, optional
        The name of the area cache file. The default is 'warning_areas.pk'.
    overwrite : bool, optional
        If True, previously cached data is overwritten and only current data is
         added to the cache files. The default is False.

    Returns
    -------
    None.

    """
    # if not overwriting, tries to read previous data and appends on new data
    if not overwrite:
        polys = retrieve_pickle_cache(poly_cache)
        areas = retrieve_pickle_cache(area_cache)
    else:
        print("Overwriting caches...")
        polys = []
        areas = []

    for warning in warnings:
        # if the warning id does not already have a corresponding polygon
        # region cached, add it
        if not any((poly[0][0]['properties']['FWS_TACODE'] == warning.id)
                   for poly in polys):
            if warning.geojson is not None and warning.region is not None:
                polys.append([warning.geojson, warning.region,
                              warning.is_poly_simplified,
                              warning.simplified_geojson])

        # if the warning id does not already have corresponding area data
        # cached, add it
        if not any((area['items']['currentWarning']['floodAreaID'] ==
                    warning.id) for area in areas):
            if warning.area_json is not None:
                areas.append(warning.area_json)

    save_to_pickle_cache(poly_cache, polys)
    save_to_pickle_cache(area_cache, areas)


def retrieve_pickle_cache(filename):
    """Read a cached pickle file and returns the result.

    Parameters
    ----------
    filename : string
        The name of the pickle file to be read.
        This file must be in the cache directory.

    Returns
    -------
    pickle_variables
        The python variables read from the pickle file..

    """
    sub_dir = 'cache'
    cache_file = os.path.join(sub_dir, filename)

    try:
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    except (pickle.UnpicklingError, FileNotFoundError):
        return []


def save_to_pickle_cache(filename, data):
    """Save data to a pickle cache file.

    Parameters
    ----------
    filename : string
        The name of the pickle file to be saved. The file is placed in the
        cache directory.
    data :
        The data to be saved to a pickle file. Any Python variable type may
        be used.

    Returns
    -------
    None.

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
    """Create geoJSON FeatureCollection object to plot flood warnings on a map.

    Parameters
    ----------
    warnings : list[FloodWarning]
        List of flood warnings.
    file : string, optional
        For debug purposes, saves parameters data to a file, without any
        coordinates if file is a non-None string. The default is None.

    Returns
    -------
    data : dict
        The geoJSON object containing the regions of all the warnings in
        warnings.

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
            data_without_coords = {'type': 'FeatureCollection',
                                   'features': features_without_coords}
            json.dump(data_without_coords, out)

    return data


def build_severity_dataframe(warnings):
    """Build dataframe with warnings data, used to colour the map regions.

    Parameters
    ----------
    warnings : list[FloodWarning]
        list of flood warnings.

    Returns
    -------
    df : pandas.DataFrame
        Pandas DataFrame with the relevant data for each warning

    """
    df = pd.DataFrame()

    df['severity'] = [w.severity.name if w.severity.name is not None else
                      "Not available" for w in warnings]
    df['id'] = [w.id if w.id is not None else "Not available"
                for w in warnings]
    df['label'] = [w.label if w.label is not None else "Not available"
                   for w in warnings]
    df['last_updated'] = [w.last_update if w.last_update is not None else
                          "Not available" for w in warnings]
    df['warning_message'] = [w.message if w.message is not None else
                             "Not available" for w in warnings]
    df['int_severity'] = [w.severity_lev if w.severity_lev is not None else 5
                          for w in warnings]

    # in some cases the county names are very long so we limit to 50 characters
    county_list = []
    county_str_size_lim = 47
    for warning in warnings:
        if warning.county is None:
            county_list.append("Not available")

        elif len(warning.county) > 50:
            counties = warning.county.split(',')
            county_str = counties[0]

            for county in counties[1:]:
                if len(county_str) + len(county) + 1 < county_str_size_lim:
                    county_str += ',' + county
                else:
                    county_str += '...'
                    break

            county_list.append(county_str)

        else:
            county_list.append(warning.county)

    df['county'] = county_list

    return df
