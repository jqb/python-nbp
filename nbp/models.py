# -*- coding: utf-8 -*-
class Currency(object):
    def __init__(self, currency_name, currency_code, rate, scaler):
        self.name = currency_name
        self.code = currency_code
        self.rate = rate
        self.scaler = scaler

    def __unicode__(self):
        return u'<%s (%s) %s %s>' % (self.name, self.code, self.scaler, self.rate)

    def to_dict(self, rescale_rate=False):
        values = {
            'name': self.name,
            'scaler': self.scaler,
            'rate': self.rate,
            'code': self.code
        }

        if rescale_rate:
            values['rate'] = self.rate / values.pop('scaler')

        return values


class Table(object):
    NIL = type('NIL', (object,), {})()

    def __init__(self, no=None, publication_date=None, url=None, positions=None):
        self.no = no
        self.url = url
        self.publication_date = publication_date
        self.positions = positions or {}

    def __contains__(self, key):
        return key in self.positions

    def __iter__(self):
        return iter(self.positions.itervalues())

    def items(self):
        return self.positions.iteritems()

    def get(self, key, default=NIL):
        if default != self.NIL:
            return self.positions.get(key, default)
        return self.positions[key]

    def set(self, key, value):
        self.positions[key] = value

    def remove(self, key):
        del self.positions[key]
