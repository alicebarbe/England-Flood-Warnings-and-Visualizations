from floodsystem import datafetcher
from floodsystem.warning import FloodWarning, SeverityLevel



def build_warning_list(severity):
    data = datafetcher.fetch_flood_warnings(severity)

    warnings = []
    for w in data['items']:
        warning = FloodWarning()

        if 'id' in w:
            warning.identifier = w['id']
        if 'county' in w['floodArea']:
            warning.county = w['floodArea']['county']
            print('warning county : ' + warning.county)
        if 'polygon' in w['floodArea']:
            print(w['floodArea']['polygon'])
            poly = datafetcher.fetch_warning_region(w['floodArea']['polygon'])
            if poly is not None:
                print("setting polygon")
                warning.region = FloodWarning.geo_json_to_shape(poly)

        if 'severityLevel' in w:
            warning.severity_lev = w['severityLevel']
            warning.severity = SeverityLevel(w['severityLevel'])

        if 'isTidal' in w:
            warning.tidal = w['isTidal']
        if 'message' in w:
            warning.message = w['message']

        warnings.append(warning)

    return warnings
