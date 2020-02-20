from floodsystem import datafetcher
from floodsystem.warning import FloodWarning, SeverityLevel
import pandas as pd
from pprint import pprint
import json



def build_warning_list(severity):
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
                warning.region = FloodWarning.geo_json_to_shape(poly[0]['geometry'])
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
    features = []
    features_without_coords = []

    for w in warnings:
        for feature in w.geojson:
            features.append(feature)
            #pprint(feature)
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


def build_severity_dataframe(warnings):
    data_arr = []

    for w in warnings:
        if w.severity != SeverityLevel.low:
            data_arr.append([w.severity.value, w.id])

    return pd.DataFrame(data_arr, columns=['severity', 'id'])
