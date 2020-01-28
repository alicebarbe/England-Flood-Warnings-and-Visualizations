# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains utility functions.

"""


def sorted_by_key(x, i, reverse=False):
    """For a list of lists/tuples, return list sorted by the ith
    component of the list/tuple, E.g.

    Sort on first entry of tuple:

      > sorted_by_key([(1, 2), (5, 1]), 0)
      >>> [(1, 2), (5, 1)]

    Sort on second entry of tuple:

      > sorted_by_key([(1, 2), (5, 1]), 1)
      >>> [(5, 1), (1, 2)]

    """

    # Sort by distance
    def key(element):
        return element[i]

    return sorted(x, key=key, reverse=reverse)


def map(x, in_min, in_max, out_min, out_max):
    '''Linearly maps a value of x from a range in_min - in_max
    to one of range out_min - out_max. Note that the value is
    not constrained to the output range, nor does x need to be
    constrained to the input range

    Arguments:
        x float
            the input value

        in_min float
            bottom limit of input range

        in_max float
            upper limit of input range

        out_min float
            bottom limit of output range

        out_max float
            upper limit of output range

    Returns:
        out_val float
            the mapped value
     '''

    return ((x - in_min) / (in_max - in_min)) * (out_max - out_min) + out_min
