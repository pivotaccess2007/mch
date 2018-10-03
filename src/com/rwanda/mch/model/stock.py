#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from model.rsmsrwobj import RSMSRWObj
from util.record import fetch_summary, fetch_table, fetch_table_by_location, filter_data, fetch_report, fetch_resource, migrate
from exception.mch_critical_error import MchCriticalError
from service.stock.metrics import DRUGS
from util.mch_util import parse_codes

class Stock(RSMSRWObj):
    """A stock report of RapidSMS. Stock have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'stock'

    def __init__(self, telephone):
        """Return a stock object which telephone is *telephone* """
        self.telephone = telephone
        self.table = Stock._table

    @staticmethod
    def fetch_stock(cnds, cols, exts):
        return fetch_summary(Stock._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_stock(cnds, cols):
        return fetch_table(Stock._table, cnds, cols)

    @staticmethod
    def fetch_stock_by_location(cnds, group_by = [], INDICS = []):
        data = []; print cnds, group_by, INDICS
        for INDIC in INDICS:
            #print "CNDS: ", cnds
            cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
            curr_cnds = {INDIC[1]: ''}
            if INDIC[1] == 'total':
                cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
                curr_cnds = {}           
            curr_cnds.update(cnds)
            #print cols
            data.append(fetch_table_by_location(Stock._table, curr_cnds, cols, group_by))
        return data


    @staticmethod
    def get_report_drugs(pk):
        message = ""
        try:
            record = fetch_report(Stock._table, pk)
            report = fetch_resource(code = record.keyword)
            message = parse_codes(report, record, CODES = DRUGS)
        except Exception,e :
            #print e
            pass
        return message

    @staticmethod
    def get_report_details(pk):
        message = ""
        try:
            record = fetch_report(Stock._table, pk)
            return record.message
            report = fetch_resource(code = record.keyword)
            message = "Report: %(keyword)s, DRUGS: %(drugs)s" % {'keyword': record.keyword,
                                            'drugs': parse_codes(report, record, CODES = DRUGS)}
        except Exception,e :
            #print e
            pass
        return message



