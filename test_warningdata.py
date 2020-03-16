from floodsystem.warningdata import build_warning_list, build_regions_geojson, build_severity_dataframe, \
    save_to_pickle_cache, retrieve_pickle_cache
from floodsystem.warning import FloodWarning, SeverityLevel

import os


def test_build_regions_geojson():
    """Note that this test only considers exceptional cases, since
    the variety of warning regions possible makes testing for a true
     warning almost impossible"""

    # empty array - should return an empty geojson object
    warnings = []
    geojson = build_regions_geojson(warnings)
    assert (geojson['type'] == 'FeatureCollection')
    assert (geojson['features'] == [])

    # warnings without any information - should return an empty geojson object
    warnings = [FloodWarning(), FloodWarning()]
    geojson = build_regions_geojson(warnings)
    assert (geojson['type'] == 'FeatureCollection')
    assert (geojson['features'] == [])


def test_build_severity_dataframe():
    # empty array - should return an empty datafram
    warnings = []
    severity = SeverityLevel.low
    df = build_severity_dataframe(warnings, severity.value)
    assert (df.empty)

    # warnings without any information or with partial information - should return defaults and severity low
    warnings = [FloodWarning(), FloodWarning()]
    print(warnings)
    df = build_severity_dataframe(warnings, severity.value)
    print(df.count().values)
    assert (all([col_len == 2 for col_len in df.count().values]))

def test_pickle_dump_and_recieve():
    """Checks that a pickle file is produced and that the retrieved data
     is identical to the original"""

    test_data = {'float': 3.425, 'coord': (51.2, 0.24), 'str': 'Testing'}
    save_to_pickle_cache('test_file.pk', test_data)
    assert (os.path.isfile('cache/test_file.pk'))

    retrieved_data = retrieve_pickle_cache('test_file.pk')
    assert(retrieved_data == test_data)

    os.remove('cache/test_file.pk')
