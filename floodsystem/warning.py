from shapely.geometry import Point, Polygon, shape

class FloodWarning:

    def __init__(self,
                 identifier=None,
                 county=None,
                 severity_level=None,
                 severity=None,
                 tidal=None,
                 message=None,
                 region=None):

        self.id = identifier
        self.county = county

        self.severity_level = severity_level
        self.severity = severity

        self.tidal = tidal
        self.message = message
        self.region = self.geo_json_to_shape(region)

    def __repr__(self):
        d = "Flood Warning"
        d += "id : " + self.id
        d += "county : " self.county
        d += "severity : " + self.severity_level + " (" + self.severity + ") "
        return d

    def geo_json_to_shape(self, geo_json_obj):
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

    def coord_in_region(self, coord):

        point = Point(coord[0], coord[1])
        if self.region is not None:
            return self.region.contains(point)
        else:
            return False
