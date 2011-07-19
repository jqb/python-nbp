NBP
===

Function(s) related  to Polish National  Bank.  The basic goal  was to
create function to get exchange rate for the given currency and date:

::

   from datetime import date
   import nbp


   currency_data = nbp.download_exchange_rate(date(2010, 7, 11), 'EUR')
   assert currency_data == {
        'search_date': '2010-07-11',
        'table_no': u'132/A/NBP/2010',
        'pub_date': u'2010-07-09',
        'currency': {
            'currency_name': u'euro',
            'rate': 4.0732999999999997,
            'currency_code': u'EUR'}}


Explanation
===========

Polish National Bank (NBP) provides three types of currency tables: A,
B and C. The module uses only A and B.  The A table is published every
working day and B table only on wednesdays.

The module first search for the  currency in the A table, and if there
is no  results it  searches B.  It the date  you provide  doesn't have
record  in the  tables,  algtorithm searches  for  the first  previous
working day.

Result  of the 'download_exchange_rate'  algorithm is  dictionary with
following keys:

::

   { 'search_date': <date which was passed to the algorithm as string>,
     'table_no':    <nbp currency table no eg. '132/A/NBP/2010'>,
     'pub_date':    <publication date of table, it can be diffrent then 'search_date'>,
     'currency': {
         'currency_name': <name of currency eg. u'euro'>,
         'rate':          <value of the exchange rate>,
         'currency_code': <currency code eg 'EUR' or 'USD'>
         }}


Requirements
============
 - nosetest for tests
