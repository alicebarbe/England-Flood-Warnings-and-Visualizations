# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 17:38:52 2020

@author: Alice
"""

from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_within_radius

def run():
    """Requirements for Task 1C"""

    # Build list of stations within radius of coordinates
    stations_dists = stations_within_radius(build_station_list(), (52.2053, 0.1218), 10)
    
    # Get alphabetized list of station names
    stations_list = [station_dist[0].name for station_dist in stations_dists]

    print(sorted(stations_list))


if __name__ == "__main__":
    print("*** Task 1C: CUED Part IA Flood Warning System ***")
    run()
