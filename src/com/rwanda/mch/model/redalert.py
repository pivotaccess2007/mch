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
from model.redresult import Redresult
from util.record import fetch_summary, fetch_redalert, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Redalert(RSMSRWObj):
    """A Redalert report of RapidSMS. Redalerts have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'redalert'

    def __init__(self, national_id, pregnancy_pk = None, birth_date = None, child_number = None):
        """Return a Redalert object which redalert_date is *redalert_date* """
        self.table = Redalert._table
        self.national_id    = national_id
        self.pregnancy_pk   = pregnancy_pk
        self.birth_date     = birth_date
        self.child_number   = child_number

    def get_or_create(self, orm, obj):
        """ Retrieve a redalert object and return redalert record """
        try:
            red = fetch_redalert(self.national_id, obj.UNIQUE_QUERY)
            if red:
                obj.FIELDS.update({'indexcol': red.indexcol})
            #print obj.UNIQUE_QUERY
            self.save(orm, obj)
            return self.get(obj.UNIQUE_QUERY)
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Redalert cannot be saved and fetched'))
        return False

    def get(self, filters):
        """ Retrieve a redalert object and return redalert record """
        try:
            red = fetch_redalert(self.national_id, filters)
            return red
        except:
            raise MchCriticalError(Exception('Redalert cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a redalert object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Redalert cannot be saved'))
        return False

    @staticmethod
    def fetch_redalerts(cnds, cols, exts):
        return fetch_summary(Redalert._table, cnds, cols, exts)

    @staticmethod
    def fetch_redresults(cnds, cols, exts):
        return Redresult.fetch_redresults(cnds, cols, exts)

    @staticmethod
    def fetch_log_redalerts(cnds, cols):
        return fetch_table(Redalert._table, cnds, cols)

    @staticmethod
    def fetch_redalerts_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Redalert._table, curr_cnds, cols, group_by))
        return data


    @staticmethod
    def fetch_log_redresults(cnds, cols):
        return Redresult.fetch_log_redresults( cnds, cols)

    @staticmethod
    def fetch_redresults_by_location(cnds, group_by = [], INDICS = []):
        return Redresult.fetch_redresults_by_location(cnds, group_by = group_by, INDICS = INDICS)
