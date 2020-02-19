# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 09:44:35 2020

@author: Alice
"""

from datetime import datetime, timedelta
from floodsystem.stationdata import build_station_list
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.plot import plot_water_levels
from floodsystem.plot import plot_water_levels_with_fit

def run():
    days_to_plot = 2
    stations_list = build_station_list()
    at_risk_stations = stations_highest_rel_level(stations_list, 5)
    argv = []
    
    # create input list
    for station in at_risk_stations:
        data = fetch_measure_levels(station.measure_id, 
                                    dt=timedelta(days=days_to_plot))
        argv.append(station)
        argv.append(data[0])
        argv.append(data[1])
        
    plot_water_levels_with_fit(argv, 4)
    
if __name__ == "__main__":
    print("*** Task 2E: CUED Part IA Flood Warning System ***")
    run()
