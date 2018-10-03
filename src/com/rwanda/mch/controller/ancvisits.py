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
from model.ancvisit import Ancvisit
from model.pregnancy import Pregnancy
from util import queries
from util.mch_util import makecol, makedict, give_me_table

class AncvisitController(RSMSRWController):

    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Ancvisit.fetch_ancvisits(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(anc_date) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})
        exts    = {}
        attrs   = [(makecol(x[0]), x[1]) for x in queries.ANC_DATA['attrs']]
        cnds.update({queries.ANC_DATA['query_str']: ''})
        exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.ANC_DATA['attrs']]))#;print exts
        cols    = ['COUNT(*) AS total']
        nat     = Ancvisit.fetch_ancvisits(cnds, cols, exts)

        precnds    = self.navb.conditions()
        precnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        precnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})#
        preexts = dict([('stdanc1', ('COUNT(*)', '(lmp + INTERVAL \'90 days\') <= created_at'))  ])
        pre     = Pregnancy.fetch_pregnancies(precnds, cols, preexts)
        #print attrs, "NAT: ", nat[0].__dict__, "PRE: ", pre[0].__dict__
        return [attrs, pre, nat]


    def get_tables(self):
        #print "KW: ", self.navb.kw
        cnds    = self.navb.conditions()
        cnds.update({"(anc_date) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})

        precnds    = self.navb.conditions()
        precnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        precnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})#

        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('indexcol', 'ID'),
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('lmp', 'LMP'),
                                              ('mother_weight', 'Weight'),
                                              ('muac', 'Muac'),
                                              ('created_at', 'Submission Date')
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=anc&id=%s">View</a>' % (x), })

        INDICS  = [(makecol(x[0]), x[0], x[1]) for x in queries.ANC_DATA['attrs']]
        PRE_INDICS = [('anc1', 'total', 'ANC1'), ('stdanc1', '(lmp + INTERVAL \'90 days\') <= created_at', 'Standard ANC1')]
        ANCDICT = makedict(queries.ANC_DATA['attrs'])
        PREDICT = { x[0]: (x[1], x[2]) for x in PRE_INDICS}
        
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])        
        
        if self.navb.kw.get('subcat') is not None:
            sc = self.navb.kw.get('subcat')
            dcols = [x[0] for x in cols]
            if self.navb.kw.get('subcat') in [x[0] for x in PRE_INDICS]:
                wcl = PREDICT.get(sc)#; print wcl, PREDICT
                INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
                INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in PRE_INDICS])
                if wcl and wcl[0] != 'total':   precnds.update({wcl[0]: ''})
                nat = Pregnancy.fetch_log_pregnancies(precnds, dcols)
            else:                
                wcl = ANCDICT.get(sc)
                INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
                INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
                cnds.update({wcl[0]: ''})
                nat     = Ancvisit.fetch_log_ancvisits(cnds, dcols)
            #;print  "INDICS: ", INDICS
            #print wcl, ANCDICT, INDICS
        else:
            dcols   = [x[0] for x in cols]
            #nat     = Ancvisit.fetch_log_ancvisits(cnds, dcols)
            nat = Pregnancy.fetch_log_pregnancies(precnds, dcols)

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
                        
            if self.navb.kw.get('subcat') in [x[0] for x in PRE_INDICS]:
                #print PRE_INDICS, LOCS, precnds, group_by
                locateds = Pregnancy.fetch_pregnancies_by_location(precnds, group_by = group_by, INDICS = PRE_INDICS)
            elif self.navb.kw.get('subcat') in [x[0] for x in INDICS]:
                 #print INDICS, LOCS, cnds, group_by
                 locateds = Ancvisit.fetch_ancvisits_by_location(cnds, group_by = group_by, INDICS = INDICS)
            else:
                INDICS = PRE_INDICS + INDICS
                locateds = Ancvisit.fetch_ancvisits_by_location(cnds, group_by = group_by, INDICS = INDICS)
                locateds += Pregnancy.fetch_pregnancies_by_location(precnds, group_by = group_by, INDICS = PRE_INDICS)
                #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()
            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular

        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'Antenatal care visits%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc ) ) )
 
        #print INDICS_HEADERS, tabular, locateds
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)


