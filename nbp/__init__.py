# -*- coding: utf-8 -*-
VERSION = '1.0.1'

from datetime import datetime, date  # "date" for user usage only
import table


def download_and_parse_table(date, table_type):
    """
    Downloads latest NBP table for given 'date' and 'table_type'
    """
    day_candidate = table.get_days_count_for_table(date, table_type)

    for url, p in table.url_generator(date.year, day_candidate, table_type):
        resp = table.download(url)
        if resp:
            parsed = table.parse(resp)

            # update meta info: url of table
            parsed['url'] = url

            pub_date = datetime.strptime(parsed.get('pub_date'), '%Y-%m-%d')
            if not pub_date.date() > date:
                return parsed
    return None



def format_result(nbp_table, currency, search_date):
    currency_obj = nbp_table['positions'][currency]
    return {
        'search_date' : search_date.strftime('%Y-%m-%d'),
        'table_no' : nbp_table['table_no'],
        'pub_date' : nbp_table['pub_date'],
        'url'      : nbp_table['url'],
        'currency' : currency_obj.to_dict(rescale_rate=True),
        }



def download_exchange_rate(date, currency):
    for table_type in ['a', 'b']:
        nbp_table = download_and_parse_table(date, table_type)
        if nbp_table and currency in nbp_table['positions']:
            return format_result(nbp_table, currency, date)
    return None
