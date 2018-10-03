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
from util.mch_security import GESTATION
from controller.main import RSMSRWController
from model.death import Death
from util import queries

from util.mch_util import makecol, give_me_table


class DeathController(RSMSRWController):
    
    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Death.fetch_deaths(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})
        exts    = {}
        attrs   = [ ((makecol(x[0][0]), x[0][1]), [ (makecol(y[0]), y[1]) for y in  x[1] ]) for x in queries.DEATH_DATA['attrs']]
        attrs_bylocs = dict(attrs)
        exts.update(dict([(makecol(x[0][0]), ('COUNT(*)', x[0][0])) for x in queries.DEATH_DATA['attrs']]))
        exts.update(dict([(makecol(y[0][0]), ('COUNT(*)', y[0][0])) for y in [ x[1] for x in queries.DEATH_DATA['attrs']] ]))
        exts.update(dict([(makecol(y[1][0]), ('COUNT(*)', y[1][0])) for y in [ x[1] for x in queries.DEATH_DATA['attrs']] ]))
        exts.update(dict([(makecol(y[2][0]), ('COUNT(*)', y[2][0])) for y in [ x[1] for x in queries.DEATH_DATA['attrs']] ]))
        exts.update(dict([(makecol(y[3][0]), ('COUNT(*)', y[3][0])) for y in [ x[1] for x in queries.DEATH_DATA['attrs']] ]))
        cols    = ['COUNT(*) AS total']
        nat     = Death.fetch_deaths(cnds, cols, exts)
        #print attrs, nat[0].__dict__
        return [attrs, attrs_bylocs, nat]


    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})

        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('birth_date', 'Birth date'),
                                              ('child_number', 'Child Number'),
                                              ('death_code', 'Visit'),
                                              ('created_at', 'Submission Date'),
                                              ('indexcol', "ID")
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=dth&id=%s">View</a>' % (x), })            

        INDICS = [('all', 'total', 'Total')]
        for x in queries.DEATH_DATA['attrs']:
            INDICS.append((makecol(x[0][0]), x[0][0], x[0][1]))
            for y in x[1]: INDICS.append((makecol(y[0]), y[0], '%s %s' % (x[0][1], y[1]) ))

        INDICSDICT = {x[0]: (x[1], x[2]) for x in INDICS}
  
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])
        
        if self.navb.kw.get('subcat'):
            sc = self.navb.kw.get('subcat')
            wcl  = INDICSDICT[sc]#;print wcl, INDICSDICT       
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            if wcl and wcl[0] != 'total':   cnds.update({wcl[0]: ''})
            
            dcols   = [x[0] for x in cols]
            nat = Death.fetch_log_deaths(cnds, dcols)
        
        else:
          dcols   = [x[0] for x in cols]
          nat = Death.fetch_log_deaths(cnds, dcols)

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
                        
            locateds = Death.fetch_deaths_by_location(cnds, group_by = group_by, INDICS = INDICS)
            #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()
            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular 
        
        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'Deaths%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc or group ) ) )
 
        #print INDICS_HEADERS, tabular, locateds
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)
    
        
    
