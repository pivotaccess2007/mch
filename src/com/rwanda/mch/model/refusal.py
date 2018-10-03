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
from util.record import fetch_summary, fetch_refusal, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Refusal(RSMSRWObj):
    """A refusal report of RapidSMS. Refusals have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'refusal'

    def __init__(self, national_id, created_at):
        """Return a Refusal  """
        self.national_id = national_id
        self.created_at = created_at
        self.table = Refusal._table

    def get_or_create(self, orm, obj):
        """ Retrieve a refusal object and return refusal record """
        try:
            ref = self.get()
            if ref:
                obj.FIELDS.update({'indexcol': ref.indexcol})
            self.save(orm, obj)
            return self.get()
        except:
            raise MchCriticalError(Exception('Refusal cannot be saved and fetched'))
        return False

    def get(self):
        """ Retrieve a refusal object and return refusal record """
        try:
            ref = fetch_refusal(self.national_id, self.created_at)
            return ref
        except:
            raise MchCriticalError(Exception('Refusal cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a refusal object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except:
            raise MchCriticalError(Exception('Refusal cannot be saved'))
        return False

    @staticmethod
    def fetch_refusals(cnds, cols, exts):
        return fetch_summary(Refusal._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_refusals(cnds, cols):
        return fetch_table(Refusal._table, cnds, cols)

    @staticmethod
    def fetch_refusals_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Refusal._table, curr_cnds, cols, group_by))
        return data
