import floodsystem.stationdata as stationdata
import floodsystem.flood as flood


def test_stations_level_over_threshold():
    # build the station list and update the current levels
    station_list = stationdata.build_station_list()
    stationdata.update_water_levels(station_list, use_cache=True)

    threshold = 0.8
    over_thresh = flood.stations_level_over_threshold(station_list, threshold)

    # ensure descending order
    assert (all(prev[1] >= this[1] for prev, this in zip(over_thresh, over_thresh[1:])))
    # ensure all levels are above the threshold
    assert (all(level > threshold for _, level in over_thresh))


def test_stations_highest_rel_level():
    stations = stationdata.build_station_list(test=True)
    stationdata.update_water_levels(stations, use_cache=True)

    for N in [3, 7, 18]:
        # check the size and order of the list for various values of N
        ordered_stations = flood.stations_highest_rel_level(stations, N)
        assert (len(ordered_stations) <= N)
        assert (all(n.relative_water_level() <= p.relative_water_level() for n, p in
                    zip(ordered_stations[1:], ordered_stations)))
