# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Utility functions."""


def sorted_by_key(x, i, reverse=False):
    """For a list of lists, return list sorted by the ith component of list.

    E.g.
    Sort on first entry of tuple:

      > sorted_by_key([(1, 2), (5, 1]), 0)
      >>> [(1, 2), (5, 1)]

    Sort on second entry of tuple:

      > sorted_by_key([(1, 2), (5, 1)], 1)
      >>> [(5, 1), (1, 2)]


    Parameters
    ----------
    x : list of list/tuples
    i : int
        ith component of lists to sort from.
    reverse : bool, optional
        reverse sorted list. The default is False.

    Returns
    -------
    list
        sorted list of lists/tuples.

    """
    # Sort by distance
    def key(element):
        return element[i]

    return sorted(x, key=key, reverse=reverse)


def map(x, in_range, out_range):
    """Linearly map a value of x from an input range to an output range.

    Note that the value is not constrained to the output range,
    nor does x need to be constrained to the input range

    Parameters
    ----------
    x : float
        the input value.
    in_range : (float, float)
        tuple of the input range.
    out_range : (float float)
        tuple of output range.

    Returns
    -------
    float
        the mapped value.

    """
    return ((x - in_range[0]) / (in_range[1] - in_range[0])) * \
        (out_range[1] - out_range[0]) + out_range[0]
