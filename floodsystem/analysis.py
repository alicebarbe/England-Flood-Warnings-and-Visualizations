"""Module for analysis of historical level data."""

import numpy as np


def polyfit(dates, levels, p):
    """Create polynomial of order p that fits the level data.

    Parameters
    ----------
    dates : list[DateTime]
        list of dates with data points.
    levels : list[floats]
        list of levels corresponding to each point in dates.
    p : int
        order of polynomial to fit.

    Returns
    -------
    poly : np.poly1d
        polynomial object that fits level data.
    DateTime
        offset used to normalize dates to start at 0, equal to the first
        date in dates.

    """
    # convert date to minutes since epoch
    x = [date.timestamp() / 60 for date in dates]

    # normalize dates to start at 0, where the first date is 0
    x = [a - x[-1] for a in x]

    # fit polynomial to levels
    p_coeff = np.polyfit(x, levels, p)
    poly = np.poly1d(p_coeff)

    # return polynomial object initial time offset
    return (poly, dates[-1])
