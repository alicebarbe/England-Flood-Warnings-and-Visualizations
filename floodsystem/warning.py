from shapely.geometry import Point, Polygon, shape
from enum import Enum
from floodsystem.utils import sorted_by_key

class FloodWarning:

    def __init__(self,
                 identifier=None,
                 county=None,
                 severity=None,
                 tidal=None,
                 message=None,
                 region=None):

        self.id = identifier
        self.county = county

        self.severity_level = SeverityLevel.low
        self.severity = severity

        self.tidal = tidal
        self.message = message
        self.region = None

        self.towns = []

    def __repr__(self):
        d = "Flood Warning"
        d += "id : " + self.id
        d += "county : " + self.county
        d += "severity : " + self.severity_level + " (" + self.severity + ") "
        d += "towns affected : " + self.towns
        d += "Message : " + self.message
        return d

    def coord_in_region(self, coord):

        point = Point(coord[0], coord[1])
        if self.region is not None:
            return self.region.contains(point)
        else:
            return False

    def stations_in_warning(self, stations):
        warning_stations = []
        for station in stations:
            if station.coord is not None:
                if self.coord_in_region(station.coord):
                    warning_stations.append(station)

        return warning_stations

    def find_towns_affected(self, stations):
        self.towns = []
        for station in stations_in_warning(stations, self):
            self.towns.append(station.town)

        return self.towns

    @staticmethod
    def geo_json_to_shape(geo_json_obj):
        """"Converts a geoJSON to a shapely object

        Arguments:
            geo_json_obj  json_object
                The geoJSON object to be converted

        Returns:
            shape  shapely_object
                The shapely object (of type corresponding to the type of the input)
                The shape is corrected to form a simple polygon, e.g. by adding points
                at self intersections"""
        return shape(geo_json_obj).buffer(0)

    @staticmethod
    def order_warning_list_with_severity(warnings):

        # convert warnings to a list of tuples containing the warning and the severity
        warning_and_severity = [(w, w.severity) for w in warnings]

        warnings_sorted = [t[0] for t in sorted_by_key(warning_and_severity, 1)]
        return warnings_sorted

class SeverityLevel(Enum):
    severe = 1
    high = 2
    moderate = 3
    low = 4
