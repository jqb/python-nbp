# -*- coding: utf-8 -*-
from datetime import date

import nbp
from nose.tools import assert_equals



def test_downloads_exchange_rate_properly():
    expexted = {
        'search_date': '2010-07-11',
        'table_no': u'132/A/NBP/2010',
        'pub_date': u'2010-07-09',
        'currency': {
            'currency_name': u'euro',
            'rate': 4.0732999999999997,
            'currency_code': u'EUR'}}
    currency_data = nbp.download_exchange_rate(date(2010, 7, 11), 'EUR')
    assert_equals(expexted, currency_data)
