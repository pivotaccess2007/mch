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
from model.ccm import CCM
from util import queries

from util.mch_util import makecol, makedict, give_me_table


class CCMController(RSMSRWController):
    
    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = CCM.fetch_ccms(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})
        ccm_exts    = {}
        ccm_attrs   = [(makecol(x[0]), x[1]) for x in queries.CCM_DATA['attrs']]
        ccm_exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.CCM_DATA['attrs']]))
        cols    = ['COUNT(*) AS total']
        ccm     = CCM.fetch_ccms(cnds, cols, ccm_exts)

        cmr_exts    = {}
        cmr_attrs   = [(makecol(x[0]), x[1]) for x in queries.CMR_DATA['attrs']]
        cmr_exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.CMR_DATA['attrs']]))
        cmr     = CCM.fetch_cmrs(cnds, cols, cmr_exts)
        #print ccm_attrs, cmr_attrs, ccm[0].__dict__, cmr[0].__dict__
        return [ccm_attrs, cmr_attrs, ccm, cmr]

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

        
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])

        CCMINDICS = [('ccm', 'total', 'Total CCM'),] + [(makecol(x[0]), x[0], x[1]) for x in queries.CCM_DATA['attrs'] ]
        CCMINDICSDICT = {x[0]: (x[1], x[2]) for x in CCMINDICS}

        CMRINDICS = [('cmr', 'total', 'Total CMR'),] + [(makecol(x[0]), x[0], x[1]) for x in queries.CMR_DATA['attrs'] ]
        CMRINDICSDICT = {x[0]: (x[1], x[2]) for x in CMRINDICS}
        INDICS = CCMINDICS
        if self.navb.kw.get('subcat'):
          sc = self.navb.kw.get('subcat')
          dcols   = [x[0] for x in cols]
          if self.navb.kw.get('group') == 'cmr' or self.navb.kw.get('subcat') == 'cmr':
            wcl  = CMRINDICSDICT[sc]#;print wcl, CMRINDICSDICT       
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            if wcl and wcl[0] != 'total':   cnds.update({wcl[0]: ''})
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=cmr&id=%s">View</a>' % (x), }) 
            nat = CCM.fetch_log_cmrs(cnds, dcols)
          else:
            wcl  = CCMINDICSDICT[sc]#;print wcl, CCMINDICSDICT       
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            if wcl and wcl[0] != 'total':   cnds.update({wcl[0]: ''})
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=ccm&id=%s">View</a>' % (x), }) 
            nat = CCM.fetch_log_ccms(cnds, dcols) 
        
        else:
          dcols   = [x[0] for x in cols]
          if self.navb.kw.get('group') == 'cmr' or self.navb.kw.get('subcat') == 'cmr':
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=cmr&id=%s">View</a>' % (x), }) 
            nat = CMR.fetch_log_cmrs(cnds, dcols)
          else:
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=ccm&id=%s">View</a>' % (x), }) 
            nat = CCM.fetch_log_ccms(cnds, dcols)

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
                        
            if self.navb.kw.get('subcat') in [x[0] for x in CCMINDICS]:
                #print PRE_INDICS, LOCS, cnds, group_by
                locateds = CCM.fetch_ccms_by_location(cnds, group_by = group_by, INDICS = CCMINDICS)
            elif self.navb.kw.get('subcat') in [x[0] for x in CMRINDICS]:
                 #print INDICS, LOCS, cnds, group_by
                 locateds = CCM.fetch_cmrs_by_location(cnds, group_by = group_by, INDICS = CMRINDICS)
            else:
                INDICS = CCMINDICS + CMRINDICS
                locateds = CCM.fetch_ccms_by_location(cnds, group_by = group_by, INDICS = CCMINDICS)
                locateds += CCM.fetch_cmrs_by_location(cnds, group_by = group_by, INDICS = CMRINDICS)
                #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()

            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular 
        
        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'CCM%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc or group ) ) )
 
        #print INDICS_HEADERS, tabular, locateds
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)
    
        
    
