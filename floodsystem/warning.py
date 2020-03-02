from shapely.geometry import Point, MultiPolygon, Polygon, shape, mapping
from enum import Enum
from haversine import haversine
from floodsystem.utils import sorted_by_key


class FloodWarning:

    """A Class to store data regarding flood warnings, obtained from the Flood Monitoring API"""

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
        self.geojson = geojson
        self.is_poly_simplified = False
        self.coord = None

        self.last_update = None

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
        """Determines if a given coordinate is within the region of the flood warning

        Arguments:
            coord: (lat, long).
                The coordinates of the point in question, as a tuple

        Returns:
            is_in_region: bool.
                True if the point is in the region, false if the point is outside
                the region or the region is None"""

        point = Point(coord[1], coord[0])
        if self.region is not None:
            # return true if any one region contains the point
            for r in self.region:
                if r.contains(point):
                    return True
            return False
        else:
            return False

    def stations_in_warning(self, stations):
        """Produces a list of stations which are within the warning

        Arguments:
            stations: [MonitoringStations]
                Created using stationdata.build_station_list()

        Returns:
            stations_in_warning: [MonitoringStation]
                List of monitoring stations whose coordinates are within the warning region
        """

        warning_stations = []
        for station in stations:
            if station.coord is not None:
                if self.coord_in_region(station.coord):
                    warning_stations.append(station)

        return warning_stations

    def find_towns_affected(self, stations):
        """"Finds the towns within the flood warning region
        with a monitoring station in their vicinity

        Args:
            stations: (list of MonitoringStations) produced using stationdata.build_station_list

        Returns:
            towns: (list of Strings) A list of names of the towns affected
        """
        self.towns = []
        for station in self.stations_in_warning(stations):
            self.towns.append(station.town)

        return self.towns

    def simplify_geojson(self, tol=0.001, buf=0.005, convex=False):
        """Simplifies the geometry of the polygon for better plotting, updating
        self.region and self.geojson

        Args:
            tol: (float) Determines the maximum allowed deviation from the original shape
            buf: (float) The amount to dilate the shapes in order to smooth them
            convex: (bool) If true, the shape is approximated to a convex polygon

        """
        for i, r in enumerate(self.region):
            if convex:
                # removes concavity - doesnt seem to be working though
                self.region[i] = r.convex_hull
            self.region[i] = r.simplify(tol, preserve_topology=False).buffer(buf)

            # update the geoJSON object
            self.geojson[i]['geometry'] = mapping(self.region[i])

    @staticmethod
    def geo_json_to_shape(geo_json_obj):
        """"Converts a geoJSON to a shapely object

        Arguments:
            geo_json_obj:  json_object.
                The geoJSON object to be converted

        Returns:
            shape:  shapely_object.
                The shapely object (of type corresponding to the type of the input)
                The shape is corrected to form a simple polygon, e.g. by adding points
                at self intersections"""
        return shape(geo_json_obj).buffer(0)

    @staticmethod
    def order_warning_list_with_severity(warnings):
        """ Puts warnings in order of decreasing severity (most severe first)
        Arguments:
            warnings: [FloodWarning].
                List of flood warnings

        Returns:
            warnings_sorted: [FloodWarning].
                Ordered list of flood warnings
        """

        # convert warnings to a list of tuples containing the warning and the severity
        warning_and_severity = [(w, repr(w.severity)) for w in warnings]

        warnings_sorted = [t[0] for t in sorted_by_key(warning_and_severity, 1)]
        return warnings_sorted

    @staticmethod
    def check_warnings_at_location(warnings, loc):
        """Checks for any flood warnings concerning a specified location

        Arguments:
            loc: tuple of the form (Lat, Long)

            warnings: [Warning].
                List of warnings generated from warningdata.build_warning_list

        Returns:
            warnings_at_loc: list of Warnings.
                A list of warnings pertaining to the location provided."""

        warnings_at_loc = []
        for warning in warnings:
            if warning.coord_in_region(loc):
                warnings_at_loc.append(warning)

        return warnings_at_loc

class SeverityLevel(Enum):
    """Enum to map severity levels to descriptive severities"""

    severe = 1
    high = 2
    moderate = 3
    low = 4
