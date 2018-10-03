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
from util.record import fetch_nbcvisit, fetch_summary, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Nbcvisit(RSMSRWObj):
    """A nbcvisit report of RapidSMS. Nbcvisits have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'nbcvisit'

    def __init__(self, national_id, birth_date, child_number, nbc_visit):
        """Return a Nbcvisit object which birth_date is *birth_date* """
        self.nbc_visit = nbc_visit
        self.national_id = national_id
        self.birth_date = birth_date
        self.child_number = child_number
        self.table = Nbcvisit._table

    def get_or_create(self, orm, obj, nbc1):
        """ Retrieve a nbcvisit object and return nbcvisit record """
        try:
            nbc = fetch_nbcvisit(self.national_id, self.birth_date, self.child_number, self.nbc_visit)
            if nbc:
                obj.FIELDS.update({'indexcol': nbc.indexcol})
            self.save(orm, obj, nbc1)
            return self.get()
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Nbvisit cannot be saved and fetched'))
        return False

    def get(self):
        """ Retrieve a nbcvisit object and return nbcvisit record """
        try:
            nbc = fetch_nbcvisit(self.national_id, self.birth_date, self.child_number, self.nbc_visit)
            return nbc
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Nbvisit cannot be fetched'))
        return False

    def save(self, orm, obj, nbc1):
        """ Save a Nbcvisit object and return indexcol """
        try:
            #print obj.FIELDS, nbc1
            ref = orm.ORM.store(self.table, obj.FIELDS)
            if obj.FIELDS.get('nbc_visit').lower() == 'nbc2' and nbc1 is True:
                ref1 = fetch_nbcvisit(self.national_id, self.birth_date, self.child_number, 'nbc1')
                if not ref1:
                    obj.FIELDS.update({'nbc_visit': 'nbc1'})
                    ref1 = orm.ORM.store(self.table, obj.FIELDS)    
            return ref
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Nbcvisit cannot be saved'))
        return False

    @staticmethod
    def fetch_nbcvisits(cnds, cols, exts):
        return fetch_summary(Nbcvisit._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_nbcvisits(cnds, cols):
        return fetch_table(Nbcvisit._table, cnds, cols)

    @staticmethod
    def fetch_nbcvisits_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Nbcvisit._table, curr_cnds, cols, group_by))
        return data
