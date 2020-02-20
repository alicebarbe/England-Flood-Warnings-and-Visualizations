from shapely.geometry import Point, MultiPolygon, Polygon, shape
from enum import Enum
from floodsystem.utils import sorted_by_key


class FloodWarning:

    def __init__(self,
                 identifier=None,
                 county=None,
                 label=None,
                 description=None,
                 severity_lev=None,
                 tidal=None,
                 message=None,
                 region=None,
                 geojson=None):

        self.id = identifier
        self.county = county
        self.label = label
        self.description = description

        self.severity = SeverityLevel(severity_lev) if severity_lev is not None else SeverityLevel.low
        self.severity_lev = severity_lev

        self.tidal = tidal
        self.message = message
        self.region = region
        self.geojson = None

        self.towns = []

    def __repr__(self):
        d = "== Flood Warning == \n"
        d += "id : " + (self.id if self.id is not None else "None") + "\n"
        d += "county : " + (self.county if self.county is not None else "None") + "\n"
        d += "severity : " + str(self.severity_lev) + " (" + self.severity.name + ") " + "\n"
        d += "areas affected : " + (self.label if self.label is not None else " Not Available") + "\n"
        d += "Message : " + self.message
        return d

    def coord_in_region(self, coord):

        point = Point(coord[1], coord[0])
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
        for station in self.stations_in_warning(stations):
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
        warning_and_severity = [(w, repr(w.severity)) for w in warnings]

        warnings_sorted = [t[0] for t in sorted_by_key(warning_and_severity, 1)]
        return warnings_sorted

    def get_points(self):
        if self.region.geom_type == 'Polygon':
            print("polygon")
            return self.region.exterior.xy

        if self.region.geom_type == 'MultiPolygon':
            allx = []
            ally = []
            for poly in self.region:
                allx.append(p for p in poly.xy[0])
                ally.append(p for p in poly.xy[1])
            return allx, ally

        else:
            return (0,0)


class SeverityLevel(Enum):
    severe = 1
    high = 2
    moderate = 3
    low = 4
