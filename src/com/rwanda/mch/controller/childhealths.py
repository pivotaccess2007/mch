#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"


from datetime import datetime, timedelta
from controller.main import RSMSRWController
from model.childhealth import Childhealth
from util import queries

from util.mch_util import makecol, makedict, give_me_table


class ChildhealthController(RSMSRWController):
    
    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Childhealth.fetch_childhealths(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})
        exts    = {}

        vac_comps_attrs = [(makecol(x[0]), x[1]) for x in queries.VAC_DATA['VAC_COMPLETION']['attrs']]
        exts.update(dict([(makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.VAC_DATA['VAC_COMPLETION']['attrs']]))
        
        vac_series_attrs = [(makecol(x[0]), x[1]) for x in queries.VAC_DATA['VAC_SERIES']['attrs']]
        exts.update(dict([(makecol(x[0]), ('COUNT(*)',x[0])) for x in queries.VAC_DATA['VAC_SERIES']['attrs']]))
        cols    = ['COUNT(*) AS total']
        nat     = Childhealth.fetch_childhealths(cnds, cols, exts)
        #print vac_comps_attrs, vac_series_attrs, nat[0].__dict__
        return [vac_comps_attrs, vac_series_attrs, nat]

    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})
        
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('birth_date', 'Birth date'),
                                              ('child_number', 'Child number'),
                                              ('muac', 'MUAC'),
                                              ('created_at', 'Submission Date'),
                                              ('indexcol', "ID")
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=chi&id=%s">View</a>' % (x), }) 
    
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])

        INDICS = [('all', 'total', 'Total')
                    ] + [(makecol(x[0]), x[0], x[1]) for x in queries.VAC_DATA['VAC_COMPLETION']['attrs']
                    ] + [(makecol(x[0]), x[0], x[1]) for x in queries.VAC_DATA['VAC_SERIES']['attrs']
                    ]

        INDICSDICT = {x[0]: (x[1], x[2]) for x in INDICS}

        if self.navb.kw.get('subcat') is not None:
            sc = self.navb.kw.get('subcat')
            dcols = [x[0] for x in cols]
            wcl = INDICSDICT.get(sc)#; print wcl, PREDICT
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            if wcl and wcl[0] != 'total':   cnds.update({wcl[0]: ''})
            nat = Childhealth.fetch_log_childhealths(cnds, dcols)            
            #print wcl, INDICSDICT, INDICS
        else:
            dcols   = [x[0] for x in cols]
            nat = Childhealth.fetch_log_childhealths(cnds, dcols)

        if self.navb.kw.get('view') == 'table' or self.navb.kw.get('view') != 'log' :
            group_by = []
            group_by += ['province_pk']  if self.navb.kw.get('nation') or not group_by else []
            group_by += ['district_pk'] if self.navb.kw.get('province') else []
            group_by += ['referral_facility_pk'] if self.navb.kw.get('district') else []
            group_by += ['facility_pk'] if self.navb.kw.get('hd') else [] 
            #print "\nGROUP BY: %s \n" % group_by
            LOCS = {'nation': self.navb.kw.get('nation'),
                    'province': self.navb.kw.get('province'),
                    'district': self.navb.kw.get('district'),
                    'hospital': self.navb.kw.get('hd'),
                    'location': self.navb.kw.get('hc')
                    }
                        
            locateds = Childhealth.fetch_childhealths_by_location(cnds, group_by = group_by, INDICS = INDICS)
            #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()
            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular

        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'Vaccination%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc ) ) )
 
        #print INDICS_HEADERS, tabular, locateds
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)
    
        
    
