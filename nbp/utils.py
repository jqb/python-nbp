# -*- coding: utf-8 -*-
import datetime



def is_weekend_date(date):
    """
    Returns true, if weekday of date is weekend day
    """
    # Monday is 0 and Sunday is 6
    wd = date.weekday()
    return  wd == 5 or wd == 6
