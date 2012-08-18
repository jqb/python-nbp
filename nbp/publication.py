# -*- coding: utf-8 -*-
import urllib2
from datetime import datetime, date, timedelta
from xml.dom import minidom

from . import dateutils
from .models import Currency, Table


# URLS BUILDING AND GENERATION ##############################################
NBP_CURRENCY_TABLE_URL_PREFIX = 'http://rss.nbp.pl/kursy/xml2/'
NBP_CURRENCY_TABLE_URL_PATTERN = '%s/%s/%s%s%s.xml'
# order: year, table_type, short_year, table_type, pub_number

def build_url(year, pub_number, table_type, prefix=None):
    """
    Builds NBP currency table URL and it's params.

    :param year:       year from you want to download currency rate
    :param pub_number: number publication in the given year & table_type

    Returns a tuple:
      ``url``             - builded url as string,
      ``url_params_dict`` - params that was used to build th url

    ``url_params_dict`` contains following keys:
        ``year``, ``short_year``, ``pub_number``, ``table_type``

    Usage::

       >>> from nbp import publication
       >>> publication.build_url(2012, 123, 'a')
       >>> ('http://rss.nbp.pl/kursy/xml2/2012/a/12a123.xml', {
       ...    'pub_number': '123',
       ...    'table_type': 'a',
       ...    'short_year': '12',
       ...    'year': 2012
       ... })
    """
    prefix = prefix or NBP_CURRENCY_TABLE_URL_PREFIX

    short_year = str(year)[2:]                 # 2012  =>  12
    pub_number = str(pub_number).rjust(3, '0') # 4     =>  004

    params = year, table_type, short_year, table_type, pub_number
    url = '%s%s' % (prefix, NBP_CURRENCY_TABLE_URL_PATTERN % params)
    return (url, {
        'year'       : year,
        'pub_number' : pub_number,
        'short_year' : short_year,
        'table_type' : table_type
    })


def gen_urls(year=None, pub_number=None, table_type=None, gen_number=15):
    """
    Generator that iterates tuples of (``url``, ``url_params``)
    down over existing publication numbers.

    You can change number of generation via ``gen_number`` kwarg.
    The default value of ``gen_number`` is 15.
    """

    while gen_number > 0:
        if pub_number == 0:  # we're in the begining of the year
            previous_year_date = date(year, 1, 1) - timedelta(days=1)
            year       = previous_year_date.year
            pub_number = calculate_number(previous_year_date, table_type)
        yield build_url(year, pub_number, table_type)
        pub_number -= 1
        gen_number -= 1
# END #######################################################################


TABLE_TYPES_DAY_COUNTER = {
    'a' : dateutils.count_working_days,
    'b' : dateutils.count_wednesdays
}

def calculate_number(date, table_type):
    """
    Calculates publication number for the
    given ``date`` and ``table_type``.

    In NBP tables each publication has incremental number
    that depends on ``table_type``.
    """
    assert table_type in 'abAB'
    func = TABLE_TYPES_DAY_COUNTER[table_type.lower()]
    return func(date)


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


def parse(file_, url=None):
    """
    Parses given xml-file-like object.
    """
    dom = minidom.parse(file_)
    dget = dom.getElementsByTagName

    table_no = dget('numer_tabeli')[0].firstChild.data
    pub_date = datetime.strptime(
        dget('data_publikacji')[0].firstChild.data,
        '%Y-%m-%d',
    )
    table = Table(no=table_no, publication_date=pub_date, url=url)

    for elem in dget('pozycja'):
        get = elem.getElementsByTagName

        currency_name = get('nazwa_waluty')[0].firstChild.data
        currency_code = get('kod_waluty')[0].firstChild.data
        scaler        = get('przelicznik')[0].firstChild.data
        rate          = get('kurs_sredni')[0].firstChild.data

        table.set(currency_code, Currency(
            currency_name,
            currency_code,
            float(rate.replace(',', '.')),
            int(scaler),
        ))

    return table


def get_table(date, table_type):
    """
    Download and parse latest NBP table for given 'date' and 'table_type'
    """
    urlsgen = gen_urls(
        pub_number = calculate_number(date, table_type),
        year       = date.year,
        table_type = table_type,
    )

    for url, p in urlsgen:
        resp = download(url)
        if resp:
            table = parse(resp, url=url)
            if not table.publication_date.date() > date:
                return table

    return None
