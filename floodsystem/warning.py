"""Store and process flood warning data from Flood Monitoring API."""

from enum import Enum
from shapely.geometry import Point, shape, mapping
from floodsystem.utils import sorted_by_key


class FloodWarning:
    """A flood warning data class, obtained from the Flood Monitoring API."""

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
        self.severity = SeverityLevel(severity_lev) if severity_lev \
            is not None else SeverityLevel.low
        self.severity_lev = severity_lev

        self.area_json = None
        self.label = label
        self.description = description
        self.coord = None

        self.county = county
        self.towns = []

        self.region = region
        self.geojson = geojson
        self.simplified_geojson = geojson
        self.is_poly_simplified = {'tol': 0.000, 'buf': 0.000}

        self.tidal = tidal
        self.message = message
        self.last_update = None

    def __repr__(self):
        d = "== Flood Warning == \n"
        d += "id : " + (self.id if self.id is not None else "None") + "\n"
        d += "county : " + (self.county if self.county is not None else "None") + "\n"
        d += "severity : " + str(self.severity_lev if self.severity_lev is not None else 4)
        d += " (" + self.severity.name + ") " + "\n"
        d += "areas affected : " + (self.label if self.label is not None else " Not Available") + "\n"
        d += "Message : " + self.message if self.message is not None else "Not Available" + "\n"
        return d

    def coord_in_region(self, coord):
        """Determine if a coordinate is within the region of the flood warning.

        Parameters
        ----------
        coord : (lat, long)
            The coordinates of the point in question, as a tuple.

        Returns
        -------
        bool
            True if the point is in the region, false if the point is outside
            the region or the region is None.

        """
        point = Point(coord[1], coord[0])
        if self.region is not None:
            # return true if any one region contains the point
            for r in self.region:
                if r.contains(point):
                    return True
            return False
        return False

    def stations_in_warning(self, stations):
        """Produce a list of stations which are within the warning.

        Note it is often the case that a warning region may have no stations in
        it. This is because the Environmental Agency defines the warning regions based on
        flood planes or topology regions.

        Parameters
        ----------
        stations : list[MonitoringStation]
            Created using stationdata.build_station_list().

        Returns
        -------
        warning_stations : list[MonitoringStation]
            List of monitoring stations whose coordinates are within the
            warning region.

        """
        warning_stations = []
        for station in stations:
            if station.coord is not None:
                if self.coord_in_region(station.coord):
                    warning_stations.append(station)

        return warning_stations

    def find_towns_affected(self, stations):
        """Find towns in the flood warning region with a monitoring station.

        Parameters
        ----------
        stations : list[MonitoringStations]
            produced using stationdata.build_station_list().

        Returns
        -------
        list[String]
            list of names of the towns affected.

        """
        self.towns = []
        for station in self.stations_in_warning(stations):
            self.towns.append(station.town)

        return self.towns

    def simplify_geojson(self, tol=0.001, buf=0.002):
        """Simplify polygon geometry for better plotting, update self.simplified_geojson.

        Parameters
        ----------
        tol : float, optional
            Determines the maximum allowed deviation from the original shape.
            The default is 0.001.
        buf : float, optional
            The amount to dilate the shapes in order to smooth them.
            The default is 0.002.

        Returns
        -------
        None.

        """
        for i, r in enumerate(self.region):
            simplified_poly = r.simplify(tol, preserve_topology=False).buffer(buf)
            self.simplified_geojson[i]['geometry'] = mapping(simplified_poly)

    @staticmethod
    def geo_json_to_shape(geo_json_obj):
        """Convert a geoJSON to a shapely object.

        Parameters
        ----------
        geo_json_obj : dict
            geoJSON object to be converted.

        Returns
        -------
        shapely_object
            The shapely object (of type corresponding to the type of the input)
            The shape is corrected to form a simple polygon, e.g. by adding
            points at self intersections.

        """
        return shape(geo_json_obj).buffer(0)

    @staticmethod
    def order_warning_list_with_severity(warnings):
        """Put warnings in order of decreasing severity (most severe first).

        Parameters
        ----------
        warnings : list[FloodWarning]
            list of flood warnings.

        Returns
        -------
        warnings_sorted : list[FloodWarning]
            Ordered list of flood warnings.

        """
        # convert warnings to a list of tuples containing warning and severity
        warning_and_severity = [(w, repr(w.severity)) for w in warnings]

        warnings_sorted = [t[0] for t in sorted_by_key(warning_and_severity, 1)]
        return warnings_sorted

    @staticmethod
    def check_warnings_at_location(warnings, loc):
        """Check for any flood warnings concerning a specified location.

        Parameters
        ----------
        warnings : list[Warning]
             List of warnings generated from warningdata.build_warning_list().
        loc : (lat, long)

        Returns
        -------
        warnings_at_loc : list[Warning]
            A list of warnings pertaining to the location provided.

        """
        warnings_at_loc = []
        for warning in warnings:
            if warning.coord_in_region(loc):
                warnings_at_loc.append(warning)

        return warnings_at_loc


class SeverityLevel(Enum):
    """Enum to map severity levels to descriptive severities."""

    severe = 1
    high = 2
    moderate = 3
    low = 4
