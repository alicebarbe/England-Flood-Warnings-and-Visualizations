# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides functionality for retrieving real-time and
latest time history level data

"""

import datetime
import json
import os
import dateutil.parser
import requests


def fetch(url):
    """Fetch data from url and return fetched JSON object"""
    r = requests.get(url)
    data = r.json()
    return data


def dump(data, filename):
    """Save JSON object to file"""
    f = open(filename, 'w')
    data = json.dump(data, f)
    f.close()


def load(filename):
    """Load JSON object from file"""
    f = open(filename, 'r')
    data = json.load(f)
    f.close()
    return data


def fetch_station_data(use_cache=True):
    """Fetch data from Environment agency for all active river level
    monitoring stations via a REST API and return retrieved data as a
    JSON object.

    Fetched data is dumped to a cache file so on subsequent call it can
    optionally be retrieved from the cache file. This is faster than
    retrieval over the Internet and avoids excessive calls to the
    Environment Agency service.

    """

    # URL for retrieving data for active stations with river level
    # monitoring (see
    # http://environment.data.gov.uk/flood-monitoring/doc/reference)
    url = "http://environment.data.gov.uk/flood-monitoring/id/stations?status=Active&parameter=level&qualifier=Stage&_view=full"  # noqa

    sub_dir = 'cache'
    try:
        os.makedirs(sub_dir)
    except FileExistsError:
        pass
    cache_file = os.path.join(sub_dir, 'station_data.json')

    # Attempt to load station data from file, otherwise fetch over
    # Internet
    if use_cache:
        try:
            # Attempt to load from file
            data = load(cache_file)
        except FileNotFoundError:
            # If load from file fails, fetch and dump to file
            data = fetch(url)
            dump(data, cache_file)
    else:
        # Fetch and dump to file
        data = fetch(url)
        dump(data, cache_file)

    return data


def fetch_test_station_data():
    """Returns data from a test json file which is not updated and
    therefore can be used to check functions against known results

    Returns:
        data: json_object.
            A json object containing data from station_data_test.json
    """
    test_data_file = 'test/station_data_test.json'

    try:
        data = load(test_data_file)
    except FileNotFoundError as e:
        raise e

    return data


def fetch_latest_water_level_data(use_cache=False):
    """Fetch latest levels from all 'measures'. Returns JSON object"""

    # URL for retrieving data
    url = "http://environment.data.gov.uk/flood-monitoring/id/measures?parameter=level&qualifier=Stage&qualifier=level"  # noqa

    sub_dir = 'cache'
    try:
        os.makedirs(sub_dir)
    except FileExistsError:
        pass
    cache_file = os.path.join(sub_dir, 'level_data.json')

    # Attempt to load level data from file, otherwise fetch over
    # Internet
    if use_cache:
        try:
            # Attempt to load from file
            data = load(cache_file)
        except FileNotFoundError:
            data = fetch(url)
            dump(data, cache_file)
    else:
        data = fetch(url)
        dump(data, cache_file)

    return data


def fetch_measure_levels(measure_id, dt):
    """Fetch measure levels from latest reading and going back a period
    dt. Return list of dates and a list of values.

    """

    # Current time (UTC)
    now = datetime.datetime.utcnow()

    # Start time for data
    start = now - dt

    # Construct URL for fetching data
    url_base = measure_id
    url_options = "/readings/?_sorted&since=" + start.isoformat() + 'Z'
    url = url_base + url_options

    # Fetch data
    data = fetch(url)

    # Extract dates and levels
    dates, levels = [], []
    for measure in data['items']:
        # Convert date-time string to a datetime object
        if 'dateTime' in measure and 'value' in measure:
            d = dateutil.parser.parse(measure['dateTime'])

            # Append data
            dates.append(d)
            levels.append(measure['value'])

    return dates, levels


def fetch_flood_warnings(severity_level, use_cache=False):
    """Fetches the flood warnings issued from the API"""

    url = "http://environment.data.gov.uk/flood-monitoring/id/floods?min-severity={}".format(severity_level)

    sub_dir = 'cache'
    try:
        os.makedirs(sub_dir)
    except FileExistsError:
        pass
    cache_file = os.path.join(sub_dir, 'warning_data.json')

    # Attempt to load station data from file, otherwise fetch over
    # Internet
    if use_cache:
        try:
            # Attempt to load from file
            data = load(cache_file)
        except FileNotFoundError:
            # If load from file fails, fetch and dump to file
            data = fetch(url)
            dump(data, cache_file)
    else:
        data = fetch(url)
        dump(data, cache_file)

    return data


def fetch_warning_region(url):
    """fetches a geoJSON polygon for area over which a warning is active"""

    data = fetch(url)

    if 'features' in data:
        if len(data['features']) > 0:
            return data['features']

    return None


def fetch_warning_area(url):
    """fetches information on the area of a warning"""

    data = fetch(url)

    return data


def fetch_stations_by_type(type):
    """Fetches the stations of other types issued from the
    put type = Groundwater for groundwater stations"""

    base_url = "http://environment.data.gov.uk/flood-monitoring/id/"
    url = base_url + "stations?status=Active&type={}&_view=full".format(type)
    print(url)
    data = fetch(url)

    return data
