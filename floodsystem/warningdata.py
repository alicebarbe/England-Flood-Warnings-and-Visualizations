from floodsystem import datafetcher
from floodsystem.warning import FloodWarning, SeverityLevel
import pandas as pd
import json


def build_warning_list(severity):
    """Fetch warnings from the API and create a list of warnings
    Arguments:
        severity int
            warnings above this minimum severity value (ie of lower numerical value) will be returned

    Returns:
        warnings [FloodWarnings]
            A list of flood warnings
    """
    data = datafetcher.fetch_flood_warnings(severity)

    warnings = []
    for w in data['items']:
        warning = FloodWarning()

        if 'floodAreaID' in w:
            warning.id = w['floodAreaID']
        if 'county' in w['floodArea']:
            warning.county = w['floodArea']['county']

        if '@id' in w['floodArea']:
            flood_area = datafetcher.fetch_warning_area(w['floodArea']['@id'])
            warning.label = flood_area['items']['label']
            warning.description = flood_area['items']['description']

        if 'polygon' in w['floodArea']:
            poly = datafetcher.fetch_warning_region(w['floodArea']['polygon'])
            if poly is not None:
                warning.region = [FloodWarning.geo_json_to_shape(p['geometry']) for p in poly]
                warning.geojson = poly

        if 'severityLevel' in w:
            warning.severity_lev = w['severityLevel']
            warning.severity = SeverityLevel(w['severityLevel'])

        if 'isTidal' in w:
            warning.tidal = w['isTidal']
        if 'message' in w:
            warning.message = w['message']

        warnings.append(warning)

    return warnings


def build_regions_geojson(warnings, file=None):
    """Creates a geoJSON FeatureCollection object for plotting flood warnings on a map
    Arguments:
        warnings [FLoodWarnings]
            List of flood warnings

        file string
            For debug purposes, saves parameters data to a file, without any coordinates
            if file is a non-None string

    Returns:
        json_object dictionary
            The geoJSON object containing the regions of all the warnings in warnings
    """
    features = []
    features_without_coords = []

    for w in warnings:
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
    if file is not None:
        with open(file, 'w') as out:
            data_without_coords = {'type': 'FeatureCollection', 'features': features_without_coords}
            json.dump(data_without_coords, out)
    return data


def build_severity_dataframe(warnings, min_severity):
    """Builds a pandas dataframe with data from the warnings, which is used to
    colour the map regionson a plot

    Arguments:
        warnings [FLoodWarnings]
            List of flood warnings

        min_severity int
            The minimum severity value for which to add warnings to the dataframe

    Returns:
        data_frame DataFrame
            Pandas DataFrame with the relevant data
    """
    data_arr = []

    for w in warnings:
        if w.severity.value <= min_severity:
            if w.label is not None:
                data_arr.append([w.severity.value, w.id, w.label])
            else:
                data_arr.append([w.severity.value, w.id, "No Label"])

    return pd.DataFrame(data_arr, columns=['severity', 'id', 'label'])
