"""Unit test for the geo module"""

import floodsystem.geo as geo
import floodsystem.stationdata as stationdata


def test_rivers_with_stations():
    # make a station list
    station_list = stationdata.build_station_list()
    rivers = geo.rivers_with_stations(station_list)

    # check number of rivers does not exceed number of stations
    assert (len(rivers) <= len(station_list))


def test_stations_by_river():
    # make a station list - since we are comparing to a known output, use the test data
    station_list = stationdata.build_station_list(use_cache=False, test=True)
    stations_by_river = geo.stations_by_river(station_list)

    assert (len(stations_by_river['River Avon']) == 32)
    assert (len(stations_by_river['Baguley Brook']) == 1)
    assert (len(stations_by_river['River Thames']) == 55)


def test_rivers_by_station_number():
    # make a station list
    station_list = stationdata.build_station_list()

    for N in [5, 10, 20]:
        rivers = geo.rivers_by_station_number(station_list, N)
        assert (len(rivers) >= N)

        if len(rivers) > N:
            # check for a true tie condition
            tie_val = rivers[N - 1][1]
            for river in rivers[N:]:
                assert (river[1] == tie_val)

            # check that all tied rivers were returned
            rivers_one_more = geo.rivers_by_station_number(station_list, len(rivers) + 1)
            assert (rivers_one_more[-1][1] < tie_val)
