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
from util.record import fetch_summary, fetch_redresult, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Redresult(RSMSRWObj):
    """A Redresult report of RapidSMS. Redresults have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'redresult'

    def __init__(self, national_id, pregnancy_pk = None, birth_date = None, child_number = None):
        """Return a Redresult object which redresult_date is *redresult_date* """
        self.table = Redresult._table
        self.national_id    = national_id
        self.pregnancy_pk   = pregnancy_pk
        self.birth_date     = birth_date
        self.child_number   = child_number

    def get_or_create(self, orm, obj):
        """ Retrieve a redresult object and return redresult record """
        try:
            rar = fetch_redresult(self.national_id, obj.red_pk, obj.UNIQUE_QUERY)
            if rar:
                obj.FIELDS.update({'indexcol': rar.indexcol})
            self.save(orm, obj)
            return self.get(obj.red_pk, obj.UNIQUE_QUERY)
        except:
            raise MchCriticalError(Exception('Redresult cannot be saved and fetched'))
        return False

    def get(self, red_pk, filters):
        """ Retrieve a redresult object and return redresult record """
        try:
            rar = fetch_redresult(self.national_id, red_pk, filters)
            return rar
        except:
            raise MchCriticalError(Exception('Redresult cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a redresult object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except:
            raise MchCriticalError(Exception('Redresult cannot be saved'))
        return False


    @staticmethod
    def fetch_redresults(cnds, cols, exts):
        return fetch_summary(Redresult._table, cnds, cols, exts)


    @staticmethod
    def fetch_log_redresults(cnds, cols):
        return fetch_table(Redresult._table, cnds, cols)

    @staticmethod
    def fetch_redresults_by_location(cnds, group_by = [], INDICS = []):
        data = []#; print cnds, group_by, INDICS
        for INDIC in INDICS:
            #print "CNDS: ", cnds
            cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
            curr_cnds = {INDIC[1]: ''}
            if INDIC[1] == 'total':
                cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
                curr_cnds = {}           
            curr_cnds.update(cnds)
            #print cols
            data.append(fetch_table_by_location(Redresult._table, curr_cnds, cols, group_by))
        return data


