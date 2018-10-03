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
from util.record import fetch_summary, fetch_riskresult, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Riskresult(RSMSRWObj):
    """A Riskresult report of RapidSMS. Riskresults have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'riskresult'

    def __init__(self, national_id, pregnancy_pk):
        """Return a Riskresult object which riskresult_date is *riskresult_date* """
        self.table = Riskresult._table
        self.national_id    = national_id
        self.pregnancy_pk   = pregnancy_pk

    def get_or_create(self, orm, obj):
        """ Retrieve a riskresult object and return riskresult record """
        try:
            res = fetch_riskresult(self.national_id, obj.risk_pk, obj.UNIQUE_QUERY)
            if res:
                obj.FIELDS.update({'indexcol': res.indexcol})
            self.save(orm, obj)
            return self.get(obj.risk_pk, obj.UNIQUE_QUERY)
        except:
            raise MchCriticalError(Exception('Riskresult cannot be saved and fetched'))
        return False

    def get(self, risk_pk, filters):
        """ Retrieve a riskresult object and return riskresult record """
        try:
            res = fetch_riskresult(self.national_id, risk_pk, filters)
            return res
        except:
            raise MchCriticalError(Exception('Riskresult cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a riskresult object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except:
            raise MchCriticalError(Exception('Riskresult cannot be saved'))
        return False


    @staticmethod
    def fetch_riskresults(cnds, cols, exts):
        return fetch_summary(Riskresult._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_riskresults(cnds, cols):
        return fetch_table(Riskresult._table, cnds, cols)

    @staticmethod
    def fetch_riskresults_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Riskresult._table, curr_cnds, cols, group_by))
        return data
