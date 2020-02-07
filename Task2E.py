# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from floodsystem.stationdata import build_station_list
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.plot import plot_water_levels

def run():
    days_to_plot = 10
    stations_list = build_station_list()
    at_risk_stations = stations_highest_rel_level(stations_list, 5)
    argv = []
    for station in at_risk_stations:
        data = fetch_measure_levels(station.measure_id, 
                                    dt=timedelta(days=days_to_plot))
        argv.append(station)
        argv.append(data[0])
        argv.append(data[1])
    plot_water_levels(argv)
    
if __name__ == "__main__":
    print("*** Task 2E: CUED Part IA Flood Warning System ***")
    run()