# -*- coding: utf-8 -*-
from datetime import date  # "date" for user usage only
from . import publication
from . import caching


def format_result(nbp_table, currency, search_date):
    currency_obj = nbp_table.get(currency)
    return {
        'search_date' : search_date.strftime('%Y-%m-%d'),
        'table_no'    : nbp_table.no,
        'pub_date'    : nbp_table.publication_date.strftime('%Y-%m-%d'),
        'url'         : nbp_table.url,
        'currency'    : currency_obj.to_dict(rescale_rate=True),
    }


def download_exchange_rate(date, currency, cache_dir=None):
    for table_type in ['a', 'b']:
        nbp_table = publication.get_table(date, table_type, cache_dir=cache_dir)
        if nbp_table and currency in nbp_table:
            return format_result(nbp_table, currency, date)
    return None
