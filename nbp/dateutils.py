# -*- coding: utf-8 -*-
import datetime
import copy


def is_weekend(date):
    """
    Returns true, if weekday of given date is weekend day

    Usage::

       >>> from nbp import dateutils, date
       >>> dateutils.is_weekend(date(2009, 8, 8)) == True  # True
       >>>
    """
    # Monday is 0 and Sunday is 6
    wd = date.weekday()
    return  wd == 5 or wd == 6


def count_working_days(date):
    """
    Function counts working days from the 1st January
    of the gived ``date`` year till ``date`` inclusive.

    Eg:

        January 2012
    Su Mo Tu We Th Fr Sa
     1  2  3  4  5  6  7
     8  9 10 11 12 13 14
    15 16 17 18 19 20 21
    22 23 24 25 26 27 28
    29 30 31

    for 2012-01-08 (Friday) that will be 15 days.

    Usage::

       >>> from nbp import dateutils, date
       >>> dateutils.count_working_days(date(2012, 1, 20)) == 15  # True
       >>>
    """
    date = copy.copy(date)
    counter = 0
    current = datetime.date(date.year, 1, 1)

    while current <= date:
        if not is_weekend(current):
            counter += 1
        current = current + datetime.timedelta(days=1)
    return counter



def count_wednesdays(date):
    """
    Function counts wednesdays from the 1st January of the
    gived ``date`` year till the ``date`` inclusive.

    Eg:

        January 2012
    Su Mo Tu We Th Fr Sa
     1  2  3  4  5  6  7
     8  9 10 11 12 13 14
    15 16 17 18 19 20 21
    22 23 24 25 26 27 28
    29 30 31

    for 2012-01-08 (Friday) that will be 4th, 11th, 18th
    so 3 wednesdays together.

    Usage::

       >>> from nbp import dateutils, date
       >>> dateutils.count_wednesdays(date(2012, 1, 20)) == 3  # True
       >>>
    """
    date = copy.copy(date)
    counter = 0
    current = datetime.date(date.year, 1, 1)

    # search for first wednesday
    while current.weekday() != 2: # wednesday
        current = current + datetime.timedelta(days=1)

    while current <= date:
        counter += 1
        current = current + datetime.timedelta(days=7)
    return counter
