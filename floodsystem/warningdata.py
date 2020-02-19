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
        if 'polygon' in w['floodArea']:
            warning.region = FloodWarning.geo_json_to_shape(w['floodArea']['polygon'])

        if 'severity' in w:
            warning.severity = w['severity']
            warning.severity_level = SeverityLevel(w['severity'])

        if 'isTidal' in w:
            warning.tidal = w['isTidal']
        if 'message' in w:
            warning.message = w['message']

    warnings.append(warning)
