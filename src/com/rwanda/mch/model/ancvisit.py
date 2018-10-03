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
from util.record import fetch_summary, fetch_ancvisit, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Ancvisit(RSMSRWObj):
    """A ancvisit report of RapidSMS. Ancvisits have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'ancvisit'

    def __init__(self, national_id, pregnancy_pk, anc_visit):
        """Return a Ancvisit object which lmp is *lmp* """
        self.national_id = national_id
        self.pregnancy_pk = pregnancy_pk
        self.anc_visit = anc_visit
        self.table = Ancvisit._table

    def get_or_create(self, orm, obj):
        """ Retrieve a ancvisit object and return ancvisit record """
        try:
            anc = fetch_ancvisit(self.national_id, self.pregnancy_pk, self.anc_visit)
            if anc:
                obj.FIELDS.update({'indexcol': anc.indexcol})
            self.save(orm, obj)
            return self.get()
        except:
            raise MchCriticalError(Exception('Ancvisit cannot be saved and fetched'))
        return False

    def get(self):
        """ Retrieve a ancvisit object and return ancvisit record """
        try:
            anc = fetch_ancvisit(self.national_id, self.pregnancy_pk, self.anc_visit)
            return anc
        except:
            raise MchCriticalError(Exception('Ancvisit cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a ancvisit object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except:
            raise MchCriticalError(Exception('Ancvisit cannot be saved'))
        return False

    @staticmethod
    def fetch_ancvisits(cnds, cols, exts):
        return fetch_summary(Ancvisit._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_ancvisits(cnds, cols):
        return fetch_table(Ancvisit._table, cnds, cols)

    @staticmethod
    def fetch_ancvisits_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Ancvisit._table, curr_cnds, cols, group_by))
        return data
