NBP
===

Function(s) that downloads currency rate between PLN and the given
currency in given date. Currencies are downloaded from
The Polish National Bank site.

For example, if you need to know what was the currency rate
between PLN and EUR in 2010-07-11 you can simply type:

::

   >>> from datetime import date
   >>> import nbp
   >>> currency_data = nbp.download_exchange_rate(date(2010, 7, 11), 'EUR')
   >>> assert currency_data == {
           'search_date': '2010-07-11',
           'table_no': u'132/A/NBP/2010',
           'pub_date': u'2010-07-09',
           'currency': {
               'name': u'euro',
               'rate': 4.0732999999999997,
               'code': u'EUR',
	       },
	   }


`pub_date` equals to 2010-07-09 because 2010-07-11 was not the working day, so
the algorithm tryies to find first previous working day currency.


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
         'name': <name of currency eg. u'euro'>,
         'rate': <value of the exchange rate>,
         'code': <currency code eg 'EUR' or 'USD'>
         }}


Requirements
============

nosetest for tests

::

    $ nosetests tests.py
