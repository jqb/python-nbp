# -*- coding: utf-8 -*-
import datetime
import urllib2
import copy
from xml.dom import minidom


import utils as nbp_utils
import models as nbp_models



def count_non_weekend_days(date):
    """
    Function counts non weekend days from the 1st January
    of the gived date year.
    """
    date = copy.copy(date)
    counter = 0
    current = datetime.date(date.year, 1, 1)

    while current <= date:
        if not nbp_utils.is_weekend_date(current):
            counter += 1
        current = current + datetime.timedelta(days=1)
    return counter



def count_wednesdays(date):
    """
    Function counts wednesdays from the 1st January of the gived date year.
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



TABLE_TYPES_DAY_COUNTER = {
    'a' : count_non_weekend_days,
    'b' : count_wednesdays
    }



def get_days_count_for_table(date, table_type):
    func = TABLE_TYPES_DAY_COUNTER[table_type]
    return func(date)



NBP_CURRENCY_TABLE_URL_PATTERN = 'http://rss.nbp.pl/kursy/xml2/%s/%s/%s%s%s.xml'
def get_url(year, day_num, table_type):
    """
    Builds NBP currency table URL and it's params.
    Returns the tuple:
    (url, url_params_dict)

    url_params_dict contains:
    - year
    - short_year
    - day_num (three digits int string with leading zeros if there are nessesary)
    - table_tyle
    """
    short_year = str(year)[2:]
    day_num = str(day_num).rjust(3, '0')
    p = year, table_type, short_year, table_type, day_num
    params = {
        'year': year,
        'short_year': short_year,
        'day_num': day_num,
        'table_type': table_type}
    return NBP_CURRENCY_TABLE_URL_PATTERN % p, params



def url_generator(year, day_num, table_type, loop_times=15):
    """
    Generator that iterates tuples of (url, url_params) over existing working days.
    """
    i = day_num
    for _ in range(loop_times):
        if i == 0: # we're in the begining of the year
            previous_year_date = datetime.date(year, 1, 1) - datetime.timedelta(days=1)
            year = previous_year_date.year
            i = get_days_count_for_table(previous_year_date, table_type)
        yield get_url(year, i, table_type)
        i -= 1



def download(url):
    """
    Tries to download exchange_rate_table for the given url.
    Returns:
      resp on success
      None on failure
    """
    try:
        resp = urllib2.urlopen(url)
        if hasattr(resp, 'getcode') and resp.getcode() == 200:
            return resp
    except urllib2.URLError, e:
        resp = None
    return resp



def parse(file_):
    """
    Parses given xml-file-like object.
    """
    dom = minidom.parse(file_)

    table_no = dom.getElementsByTagName('numer_tabeli')[0].firstChild.data
    pub_date = dom.getElementsByTagName('data_publikacji')[0].firstChild.data

    positions = {}
    for elem1 in dom.getElementsByTagName('pozycja'):
        currency_name = elem1.getElementsByTagName('nazwa_waluty')[0].firstChild.data
        scaler = elem1.getElementsByTagName('przelicznik')[0].firstChild.data
        currency_code = elem1.getElementsByTagName('kod_waluty')[0].firstChild.data
        rate = elem1.getElementsByTagName('kurs_sredni')[0].firstChild.data

        positions[currency_code] = nbp_models.Currency(
            currency_name,
            currency_code,
            float(rate.replace(',', '.')),
            int(scaler))

    return {'table_no': table_no, 'pub_date': pub_date, 'positions': positions }
