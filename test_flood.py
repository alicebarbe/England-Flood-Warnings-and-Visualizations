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
