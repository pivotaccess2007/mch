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
from util.mch_security import PNC_GESTATION
from controller.main import RSMSRWController
from model.pncvisit import Pncvisit
from util import queries
from util.mch_util import makecol, makedict, give_me_table

class PncvisitController(RSMSRWController):

    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self ):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Pncvisit.fetch_pncvisits(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(delivery_date + INTERVAL \'%d days\') >= '%s'" % (PNC_GESTATION, self.navb.start) : ''})
        exts    = {}
        cols = ['COUNT(*) AS total']
        title, group, attrs, nat = ('', '', [], [])#; print self.navb.kw 
        
        if self.navb.kw.get('group') == 'no_risk':
          title = 'No Risk'
          group = 'no_risk'
          exts.update({self.navb.kw.get('group'): ('COUNT(*)', queries.PNC_DATA['NO_RISK']['query_str'])})
          cols = ['COUNT(*) AS total']
          nat = Pncvisit.fetch_pncvisits(cnds, cols, exts)
        elif self.navb.kw.get('group') == 'at_risk':
          title = 'At Risk'
          group = 'at_risk'
          attrs = [(makecol(x[0]), x[1]) for x in queries.PNC_DATA['RISK']['attrs']]
          exts.update(dict([( makecol(x[0]), ('COUNT(*)',x[0]) ) for x in queries.PNC_DATA['RISK']['attrs'] ]))
          exts.update({self.navb.kw.get('group'): ('COUNT(*)', queries.PNC_DATA['RISK']['query_str'])})
          cols = ['COUNT(*) AS total']
          nat = Pncvisit.fetch_pncvisits(cnds, cols, exts)
        elif self.navb.kw.get('group') in  [ makecol(x[0]) for x in queries.PNC_DATA['PNC']['attrs'] ] :
          title = makedict(queries.PNC_DATA['PNC']['attrs'])[self.navb.kw.get('group')][1]
          group = self.navb.kw.get('group')
          exts.update({ self.navb.kw.get('group'): ('COUNT(*)', makedict(queries.PNC_DATA['PNC']['attrs'])[self.navb.kw.get('group')][0]) } )
          cols = ['COUNT(*) AS total']
          nat = Pncvisit.fetch_pncvisits(cnds, cols, exts)
        else:
          cols = ['COUNT(*) AS total']
          exts = {'no_risk': ('COUNT(*)', queries.PNC_DATA['NO_RISK']['query_str']), 
					    'at_risk': ('COUNT(*)', queries.PNC_DATA['RISK']['query_str'])		
					    }
          exts.update(dict([ ( makecol(x[0]), ('COUNT(*)', x[0]) ) for x in queries.PNC_DATA['PNC']['attrs'] ]))
          nat = Pncvisit.fetch_pncvisits(cnds, cols, exts) 
        #print title, group, attrs, "NAT: ", nat[0].__dict__
        return (title, group, attrs, nat)


    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(delivery_date + INTERVAL \'%d days\') >= '%s'" % (PNC_GESTATION, self.navb.start) : ''})

        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('delivery_date', 'Birth date'),
                                              ('pnc_visit', 'Visit'),
                                              ('created_at', 'Submission Date'),
                                              ('indexcol', "ID")
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=pnc&id=%s">View</a>' % (x), }) 

        INDICS = [('all', 'total', 'Total'),

                    ] + [(makecol(x[0]), x[0], x[1]) for x in queries.PNC_DATA['PNC']['attrs']
                    ] + [
                        ('no_risk', "%s" % queries.PNC_DATA['NO_RISK']['query_str'], 'No Risk'), 
	                     ('at_risk', "%s" % queries.PNC_DATA['RISK']['query_str'], 'At Risk'),
                    ]

        INDICSDICT = {x[0]: (x[1], x[2]) for x in INDICS}
  
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])
        
        if self.navb.kw.get('group'):
          group = self.navb.kw.get('group')
          wcl = INDICSDICT[group]#;print wcl, INDICSDICT
          title = wcl[1]          
          INDICS = [(group, wcl[0], wcl[1])] if wcl else []
          INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
          if wcl and wcl[0] != 'total':   cnds.update({wcl[0]: ''})

          if group == 'at_risk': INDICS += [ (makecol(x[0]), x[0], x[1]) for x in queries.PNC_DATA['RISK']['attrs'] ]
          else: pass
          INDICSDICT.update({x[0]: (x[1], x[2]) for x in INDICS})
                        
          if self.navb.kw.get('subcat'):
            sc = self.navb.kw.get('subcat')
            wclsc  = INDICSDICT[sc]#;print wclsc, ATTRSDICT, ATTRS       
            INDICS = [(sc, wcl[0], wclsc[1])] if wclsc else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            cnds.update({wclsc[0]: ''})

          #print cnds
          dcols   = [x[0] for x in cols]
          nat = Pncvisit.fetch_log_pncvisits(cnds, dcols)
        
        else:
          dcols   = [x[0] for x in cols]
          nat = Pncvisit.fetch_log_pncvisits(cnds, dcols)

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
                        
            locateds = Pncvisit.fetch_pncvisits_by_location(cnds, group_by = group_by, INDICS = INDICS)
            #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()
            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular 
        
        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'Postnatal visits%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc or group ) ) )
 
        #print INDICS_HEADERS, tabular, locateds
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)
