# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Model for a monitoring station and tools for manipulating station data."""

from floodsystem.utils import map


class MonitoringStation:
    """Class representing a river level monitoring station."""

    def __init__(self, station_id, measure_id, label, coord, typical_range,
                 river, town):

        self.station_id = station_id
        self.measure_id = measure_id

        # Handle case of erroneous data where data system returns
        # '[label, label]' rather than 'label'
        self.name = label
        if isinstance(label, list):
            self.name = label[0]

        self.coord = coord
        self.typical_range = typical_range
        self.river = river
        self.town = town

        self.latest_level = None

    def __repr__(self):
        d = "Station name:     {}\n".format(self.name)
        d += "   id:            {}\n".format(self.station_id)
        d += "   measure id:    {}\n".format(self.measure_id)
        d += "   coordinate:    {}\n".format(self.coord)
        d += "   town:          {}\n".format(self.town)
        d += "   river:         {}\n".format(self.river)
        d += "   typical range: {}".format(self.typical_range)
        return d

    def typical_range_consistent(self):
        """Return true if the typical range is inconsistent.

        Range is inconsistent if lowest value is greater than largest value.

        Returns
        -------
        bool
            if typical range is consistent.

        """
        # return false only if inconsistent
        if self.typical_range is not None:
            return self.typical_range[0] <= self.typical_range[1]
        return True

    def relative_water_level(self):
        """Return the water level as a proportion of the typical range.

        This is 0.0 when the water level is equal to the lower typical range
        and 1.0 when the water level is equal to the upper typical range


        Returns
        -------
        float
            the relative water level compared to the typical range.
            If the typical range is not consistent, None is returned.

        """
        if self.typical_range_consistent() and self.typical_range is not None \
                and self.latest_level:
            # only run map if the range is consistent and not None
            # the latest level is set
            return map(self.latest_level, self.typical_range, (0.0, 1.0))
        return None

    @staticmethod
    def inconsistent_typical_range_stations(stations):
        """Return the stations with inconsistent typical ranges.

        Parameters
        ----------
        stations : list[MonitoringStation]

        Returns
        -------
        output : list[MonituringStation]
            the monitoring stations with inconsistent typical ranges.

        """
        output = []
        for station in stations:
            if not station.typical_range_consistent():
                output.append(station)
        return output

    @staticmethod
    def get_relative_water_level(station):
        """Return the relative water level of a given station.

        Useful to pass directly to sorted() as a key

        Parameters
        ----------
        station : MonitoringStation

        Returns
        -------
        float
            the relative water level of the station.

        """
        level = station.relative_water_level()
        if level is not None:
            return level
        # if the value is not available, put the station at
        # the bottom of the list
        return -256
