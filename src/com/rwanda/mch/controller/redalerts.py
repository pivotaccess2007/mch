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
from model.redalert import Redalert
from util import queries

from util.mch_util import makecol, give_me_table


class RedalertController(RSMSRWController):
    
    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Redalert.fetch_redalerts(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})
        red_exts    = {}
        red_attrs   = [(makecol(x[0]), x[1]) for x in queries.RED_DATA['attrs']]
        red_exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.RED_DATA['attrs']]))
        cols    = ['COUNT(*) AS total']
        red     = Redalert.fetch_redalerts(cnds, cols, red_exts)

        rar_exts    = {}
        rar_attrs   = [(makecol(x[0]), x[1]) for x in queries.RAR_DATA['attrs']]
        rar_outs   = [(makecol(x[0]), x[1]) for x in queries.RAR_DATA['outs']]
        rar_exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.RAR_DATA['attrs']]))
        rar_exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.RAR_DATA['outs']]))
        rar     = Redalert.fetch_redresults(cnds, cols, rar_exts)
        #print red_attrs, rar_attrs, red[0].__dict__, rar[0].__dict__
        return [red_attrs, rar_attrs, rar_outs, red, rar]



    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})

        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('birth_date', 'Birth date'),
                                              ('child_number', 'Child Number'),
                                              ('child_weight', 'Child Weight'),
                                              ('mother_weight', 'Mother Weight'),
                                              ('created_at', 'Submission Date'),
                                              ('indexcol', "ID")
                                            ]) 
            
        REDINDICS = [('red', 'total', 'Total RED'),] + [(makecol(x[0]), x[0], x[1]) for x in queries.RED_DATA['attrs'] ]
        REDINDICSDICT = {x[0]: (x[1], x[2]) for x in REDINDICS}
        
        RARINDICS = [('rar', 'total', 'Total RAR'),] + [(makecol(x[0]), x[0], x[1]) for x in queries.RAR_DATA['attrs']
                        ] + [(makecol(x[0]), x[0], x[1]) for x in queries.RAR_DATA['outs']]
        RARINDICSDICT = {x[0]: (x[1], x[2]) for x in RARINDICS}
        
        
        INDICS = REDINDICS
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])

        if self.navb.kw.get('subcat'):
          sc = self.navb.kw.get('subcat')
          if self.navb.kw.get('group') == 'rar' or self.navb.kw.get('subcat') == 'rar':
            wcl  = RARINDICSDICT[sc]#;print wcl, RARINDICSDICT       
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            if wcl and wcl[0] != 'total':   cnds.update({wcl[0]: ''})
            dcols   = [x[0] for x in cols ]
            nat = Redalert.fetch_log_redresults(cnds, dcols)
          else:
            wcl  = REDINDICSDICT[sc]#;print wcl, CCMINDICSDICT       
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            if wcl and wcl[0] != 'total':   cnds.update({wcl[0]: ''})
            dcols   = [x[0] for x in cols ]
            nat = Redalert.fetch_log_redalerts(cnds, dcols) 
        
        else:
          if self.navb.kw.get('group') == 'rar' or self.navb.kw.get('subcat') == 'rar':
            dcols   = [x[0] for x in cols]
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=rar&id=%s">View</a>' % (x), })
            nat = Redalert.fetch_log_redresults(cnds, dcols)
          else:
            dcols   = [x[0] for x in cols]
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=red&id=%s">View</a>' % (x), })
            nat = Redalert.fetch_log_redalerts(cnds, dcols)

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
                        
            if self.navb.kw.get('subcat') in [x[0] for x in REDINDICS]:
                #print REDINDICS, LOCS, cnds, group_by
                locateds = Redalert.fetch_redalerts_by_location(cnds, group_by = group_by, INDICS = REDINDICS)
            elif self.navb.kw.get('subcat') in [x[0] for x in RARINDICS]:
                #print RARINDICS, LOCS, cnds, group_by
                locateds = Redalert.fetch_redresults_by_location(cnds, group_by = group_by, INDICS = RARINDICS)
            else:
                INDICS = REDINDICS + RARINDICS
                locateds = Redalert.fetch_redalerts_by_location(cnds, group_by = group_by, INDICS = REDINDICS)
                locateds += Redalert.fetch_redresults_by_location(cnds, group_by = group_by, INDICS = RARINDICS)
                #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()
            
            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular 
        
        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'Red alerts%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc or group ) ) )
        
        #print INDICS_HEADERS, tabular, locateds
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)
    
        
    
