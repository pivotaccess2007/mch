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
from util.record import fetch_summary, fetch_current_mother_death, fetch_child_death, fetch_table, fetch_table_by_location

class Death(RSMSRWObj):
    """A Death report of RapidSMS. Deaths have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'death'

    def __init__(self, national_id, lmp = None, pregnancy_pk = None, birth_date = None, child_number = None):
        """Return a Death  """
        self.national_id = national_id
        self.lmp = lmp
        self.pregnancy_pk = pregnancy_pk
        self.birth_date = birth_date
        self.child_number = child_number
        self.table = Death._table

    def get_or_create(self, orm, obj):
        """ Retrieve a death object and return death record """
        try:
            dth = self.get()
            if dth:
                obj.FIELDS.update({'indexcol': dth.indexcol})
            self.save(orm, obj)
            return self.get()
        except:
            raise MchCriticalError(Exception('Death cannot be saved and fetched'))
        return False

    def get(self):
        """ Retrieve a death object and return death record """
        try:
            dth = fetch_current_mother_death(self.national_id)
            if self.birth_date and self.child_number:
                dth = fetch_child_death(self.national_id, self.birth_date, self.child_number)
            return dth
        except:
            raise MchCriticalError(Exception('Death cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a death object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except:
            raise MchCriticalError(Exception('Death cannot be saved'))
        return False

    @staticmethod
    def fetch_deaths(cnds, cols, exts):
        return fetch_summary(Death._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_deaths(cnds, cols):
        return fetch_table(Death._table, cnds, cols)

    @staticmethod
    def fetch_deaths_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Death._table, curr_cnds, cols, group_by))
        return data
