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
from util.record import fetch_pncvisit, fetch_summary, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Pncvisit(RSMSRWObj):
    """A pncvisit report of RapidSMS. Pncvisits have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'pncvisit'

    def __init__(self, national_id, delivery_date, pnc_visit):
        """Return a Pncvisit object which lmp is *lmp* """
        self.pnc_visit = pnc_visit
        self.national_id = national_id
        self.delivery_date = delivery_date
        self.table = Pncvisit._table

    def get_or_create(self, orm, obj, pnc1):
        """ Retrieve a pncvisit object and return pncvisit record """
        try:
            pnc = fetch_pncvisit(self.national_id, self.delivery_date, self.pnc_visit)
            if pnc:
                obj.FIELDS.update({'indexcol': pnc.indexcol})
            self.save(orm, obj, pnc1)
            return self.get()
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Pncvisit cannot be saved and fetched'))
        return False

    def get(self):
        """ Retrieve a pncvisit object and return pncvisit record """
        try:
            pnc = fetch_pncvisit(self.national_id, self.delivery_date, self.pnc_visit)
            return pnc
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Pncvisit cannot be fetched'))
        return False

    def save(self, orm, obj, pnc1):
        """ Save a Pncvisit object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            if obj.FIELDS.get('pnc_visit').lower() == 'pnc2' and pnc1 is True:
                ref1 = fetch_pncvisit(self.national_id, self.delivery_date, 'pnc1')
                if not ref1:
                    obj.FIELDS.update({'pnc_visit': 'pnc1'})
                    ref1 = orm.ORM.store(self.table, obj.FIELDS)    
            return ref
        except:
            raise MchCriticalError(Exception('Pncvisit cannot be saved'))
        return False

    @staticmethod
    def fetch_pncvisits(cnds, cols, exts):
        return fetch_summary(Pncvisit._table, cnds, cols, exts)


    @staticmethod
    def fetch_log_pncvisits(cnds, cols):
        return fetch_table(Pncvisit._table, cnds, cols)

    @staticmethod
    def fetch_pncvisits_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Pncvisit._table, curr_cnds, cols, group_by))
        return data
