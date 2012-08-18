# -*- coding: utf-8 -*-
import unittest


import nbp
from nbp import dateutils, date


class NBPTests(unittest.TestCase):
    def test_downloads_exchange_rate_properly(self):
        expexted = {
            'search_date': '2010-07-11',
            'table_no': u'132/A/NBP/2010',
            'pub_date': u'2010-07-09',
            'url': 'http://rss.nbp.pl/kursy/xml2/2010/a/10a132.xml',
            'currency': {
                'name': u'euro',
                'rate': 4.0732999999999997,
                'code': u'EUR',
                },
            }
        currency_data = nbp.download_exchange_rate(
            nbp.date(2010, 7, 11), 'EUR', cache_dir='/home/kuba/.nbp/')
        self.assertEquals(expexted, currency_data)


class DateUtilsTests(unittest.TestCase):
    """
    There's a January 2012 showed below to beter understand what
    tests are doing:

        January 2012
    Su Mo Tu We Th Fr Sa
     1  2  3  4  5  6  7
     8  9 10 11 12 13 14
    15 16 17 18 19 20 21
    22 23 24 25 26 27 28
    29 30 31
    """
    def test__is_weekend__should_tell_if_given_date_is_weekend_day(self):
        self.assertEquals(dateutils.is_weekend(date(2012, 1, 7)), True)
        self.assertEquals(dateutils.is_weekend(date(2012, 1, 8)), True)

        self.assertEquals(dateutils.is_weekend(date(2012, 1, 14)), True)
        self.assertEquals(dateutils.is_weekend(date(2012, 1, 15)), True)

        self.assertEquals(dateutils.is_weekend(date(2012, 1, 17)), False)
        self.assertEquals(dateutils.is_weekend(date(2012, 1, 18)), False)

    def test__count_working_days__should_calculate_working_days(self):
        self.assertEquals(dateutils.count_working_days(date(2012, 1, 20)), 15)
        self.assertEquals(dateutils.count_working_days(date(2012, 1, 30)), 21)

    def test__count_wednesdays__should_count_wednesdays(self):
        self.assertEquals(dateutils.count_wednesdays(date(2012, 1, 20)), 3)


if __name__ == '__main__':
    unittest.main()
