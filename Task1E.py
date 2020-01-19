# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 21:26:52 2020

@author: Daniel
"""

import floodsystem.geo as geo
import floodsystem.stationdata as stationdata

def run():
    station_list = stationdata.build_station_list()

    N = 9
    rivers = geo.rivers_by_station_number(station_list, N)
    print("{} Rivers with the greatest number of stations: \n {}".format(N, rivers))

if __name__ == "__main__":
    run()
