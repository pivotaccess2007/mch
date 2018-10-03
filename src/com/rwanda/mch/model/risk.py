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
from model.riskresult import Riskresult
from util.record import fetch_summary, fetch_risk, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Risk(RSMSRWObj):
    """A Risk report of RapidSMS. Risks have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'risk'

    def __init__(self, national_id, pregnancy_pk):
        """Return a Risk object which risk_date is *risk_date* """
        self.table = Risk._table
        self.national_id    = national_id
        self.pregnancy_pk   = pregnancy_pk

    def get_or_create(self, orm, obj):
        """ Retrieve a risk object and return risk record """
        try:
            red = fetch_risk(self.national_id, obj.UNIQUE_QUERY)
            if red:
                obj.FIELDS.update({'indexcol': red.indexcol})
            self.save(orm, obj)
            return self.get(obj.UNIQUE_QUERY)
        except:
            raise MchCriticalError(Exception('Risk cannot be saved and fetched'))
        return False

    def get(self, filters):
        """ Retrieve a risk object and return risk record """
        try:
            red = fetch_risk(self.national_id, filters)
            return red
        except:
            raise MchCriticalError(Exception('Risk cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a risk object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except:
            raise MchCriticalError(Exception('Risk cannot be saved'))
        return False

    @staticmethod
    def fetch_risks(cnds, cols, exts):
        return fetch_summary(Risk._table, cnds, cols, exts)

    @staticmethod
    def fetch_riskresults(cnds, cols, exts):
        return Riskresult.fetch_riskresults(cnds, cols, exts)

    @staticmethod
    def fetch_log_risks(cnds, cols):
        return fetch_table(Risk._table, cnds, cols)

    @staticmethod
    def fetch_risks_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Risk._table, curr_cnds, cols, group_by))
        return data
