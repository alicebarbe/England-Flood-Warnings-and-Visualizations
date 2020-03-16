from floodsystem.warningdata import build_warning_list, build_regions_geojson, build_severity_dataframe, save_to_pickle_cache
from floodsystem.warning import FloodWarning, SeverityLevel


def test_coord_in_region():

    geojson_geometry = {
           "type": "Polygon",
           "coordinates": [
             [[50.0, 0.0],
              [51.0, 0.0],
              [51.0, 1.0],
              [50.0, 1.0],
              [50.0, 0.0]]
             ]
         }

    warning = FloodWarning()
    warning.region = [FloodWarning.geo_json_to_shape(geojson_geometry)]

    # should be inside the region
    assert(warning.coord_in_region((0.5, 50.5)))
    assert (warning.coord_in_region((0.8, 50.1)))

    # should be outside the region
    assert (not warning.coord_in_region((3.5, 50.5)))
    assert (not warning.coord_in_region((4.2, 81.3)))