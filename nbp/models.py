# -*- coding: utf-8 -*-


class Currency(object):
    def __init__(self, currency_name, currency_code, rate, scaler):
        self.name = currency_name
        self.code = currency_code
        self.rate = rate
        self.scaler = scaler


    def __unicode__(self):
        return u'%s %s %s %s' % (self.name, self.scaler, self.code, self.rate)


    def to_dict(self, rescale_rate=False):
        values = {
            'name': self.name,
            'scaler': self.scaler,
            'rate': self.rate,
            'code': self.code }

        if rescale_rate:
            values['rate'] = self.rate / values.pop('scaler')

        return values
