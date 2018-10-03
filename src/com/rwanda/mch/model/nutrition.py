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
from util.record import fetch_summary, fetch_cbn, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError
from model.birth import Birth
from model.mother import Mother

class Nutrition(RSMSRWObj):
    """A Nutrition report of RapidSMS. Nutritions have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'nutrition'

    def __init__(self,  national_id, birth_date, child_number):
        """Return a Nutrition object which nutrition_date is *nutrition_date* """
        self.national_id    = national_id
        self.birth_date     = birth_date
        self.child_number   = child_number
        self.table = Nutrition._table

    def get_or_create(self, orm, obj):
        """ Retrieve a nutrition object and return nutrition record """
        try:
            cbn = fetch_cbn(self.national_id, obj.UNIQUE_QUERY)
            if cbn:
                obj.FIELDS.update({'indexcol': cbn.indexcol})
            self.save(orm, obj)
            return self.get(obj.UNIQUE_QUERY)
        except Exception, e:
            raise MchCriticalError(Exception('Nutrition cannot be saved and fetched'))
        return False

    def get(self, filters):
        """ Retrieve a nutrition object and return nutrition record """
        try:
            cbn = fetch_cbn(self.national_id, filters)
            return cbn
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Nutrition cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a nutrition object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except Exception, e:
            raise MchCriticalError(Exception('Nutrition cannot be saved'))
        return False

    @staticmethod
    def fetch_nutritions(cnds, cols, exts):
        return fetch_summary(Nutrition._table, cnds, cols, exts)

    @staticmethod
    def fetch_children(cnds, cols, exts):
        return Birth.fetch_births(cnds, cols, exts)

    @staticmethod
    def fetch_mothers(cnds, cols, exts):
        return Mother.fetch_mothers(cnds, cols, exts)

    @staticmethod
    def fetch_log_children(cnds, cols):
        return Birth.fetch_log_births(cnds, cols)

    @staticmethod
    def fetch_children_by_location(cnds, group_by = [], INDICS = []):
        return Birth.fetch_births_by_location(cnds, group_by = group_by, INDICS = INDICS)

    @staticmethod
    def fetch_log_mothers(cnds, cols):
        return Mother.fetch_log_mothers(cnds, cols)

    @staticmethod
    def fetch_mothers_by_location(cnds, group_by = [], INDICS = []):
        return Mother.fetch_mothers_by_location(cnds, group_by = group_by, INDICS = INDICS)

    @staticmethod
    def fetch_log_nutritions(cnds, cols):
        return fetch_table(Nutrition._table, cnds, cols)

    @staticmethod
    def fetch_nutritions_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Nutrition._table, curr_cnds, cols, group_by))
        return data
