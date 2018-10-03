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
from util.mch_security import GESTATION, TRACKING_DAYS
from controller.main import RSMSRWController
from model.nutrition import Nutrition
from util import queries

from util.mch_util import makecol, give_me_table


class NutritionController(RSMSRWController):
    
    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Nutrition.fetch_nutritions(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        chi_cnds    = self.navb.conditions()
        five_years_ago = self.navb.start - timedelta(days = TRACKING_DAYS)
        chi_cnds.update({"(birth_date) <= '%s'" % (self.navb.finish) : ''})
        chi_cnds.update({"(birth_date) >= '%s'" % (five_years_ago) : ''})
        chi_attrs =  queries.CHILD_NUTR.keys()
        chi_exts    = dict([(x, ('COUNT(*)', queries.CHILD_NUTR[x][0])) for x in chi_attrs])
        cols    = ['COUNT(*) AS total']
        chi_nutr     = Nutrition.fetch_children(chi_cnds, cols, chi_exts)

        pre_cnds    = self.navb.conditions()
        pre_cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        pre_cnds.update({"(recent_lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})
        pre_attrs =  queries.MOTHER_NUTR.keys()
        pre_exts    = dict([(x, ('COUNT(*)', queries.MOTHER_NUTR[x][0])) for x in pre_attrs])
        pre_nutr     = Nutrition.fetch_mothers(pre_cnds, cols, pre_exts)
        #print chi_nutr[0].__dict__, pre_nutr[0].__dict__
        return [chi_nutr, pre_nutr]



    def get_tables(self):
        chi_cnds    = self.navb.conditions()
        five_years_ago = self.navb.start - timedelta(days = TRACKING_DAYS)
        chi_cnds.update({"(birth_date) <= '%s'" % (self.navb.finish) : ''})
        chi_cnds.update({"(birth_date) >= '%s'" % (five_years_ago) : ''})
        chi_attrs =  queries.CHILD_NUTR.keys()
        
        pre_cnds    = self.navb.conditions()
        pre_cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        pre_cnds.update({"(recent_lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})
        pre_attrs =  queries.MOTHER_NUTR.keys()

        chi_cnds, markup, chicols = self.navb.neater_tables(cnds = chi_cnds, extras = [
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('birth_date', 'Birth date'),
                                              ('child_weight', 'Weight'),
                                              ('recent_muac', 'Muac'),
                                              ('created_at', 'Submission Date'),
                                              ('indexcol', "ID")
                                              
                                            ])

        CHIINDICS = [('child', 'total', 'Total Children'),
                        ] + [(makecol(x), queries.CHILD_NUTR[x][0], queries.CHILD_NUTR[x][1]) for x in chi_attrs ]
        CHIINDICSDICT = {x[0]: (x[1], x[2]) for x in CHIINDICS}
        
        pre_cnds, markup, precols = self.navb.neater_tables(cnds = pre_cnds, extras = [
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('recent_lmp', 'LMP'),
                                              #('gravidity', 'Gravidity'),
                                              #('parity', 'Parity'),
                                              ('recent_mother_weight', 'Weight'),
                                              ('recent_mother_height', 'Height'),
                                              ('recent_bmi', 'BMI'),
                                              ('recent_muac', 'MUAC'),
                                              ('created_at', 'Submission Date'),
                                              ('indexcol', "ID")
                                              
                                            ])

        
        PREINDICS = [('mother', 'total', 'Total Mothers'),
                        ] + [(makecol(x), queries.MOTHER_NUTR[x][0], queries.MOTHER_NUTR[x][1]) for x in pre_attrs ]
        PREINDICSDICT = {x[0]: (x[1], x[2]) for x in PREINDICS}
        
        
        INDICS = CHIINDICS
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])

        if self.navb.kw.get('subcat'):
          sc = self.navb.kw.get('subcat')
          if self.navb.kw.get('group') == 'mother' or self.navb.kw.get('subcat') == 'mother':
            wcl  = PREINDICSDICT[sc]#;print wcl, CMRINDICSDICT       
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            if wcl and wcl[0] != 'total':   pre_cnds.update({wcl[0]: ''})
            dcols, cols   = [x[0] for x in precols ], precols
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=mother&id=%s">View</a>' % (x), }) 
            nat = Nutrition.fetch_log_mothers(pre_cnds, dcols)
          else:
            wcl  = CHIINDICSDICT[sc]#;print wcl, CCMINDICSDICT       
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            if wcl and wcl[0] != 'total':   chi_cnds.update({wcl[0]: ''})
            dcols, cols   = [x[0] for x in chicols ], chicols
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=bir&id=%s">View</a>' % (x), }) 
            nat = Nutrition.fetch_log_children(chi_cnds, dcols) 
        
        else:
          if self.navb.kw.get('group') == 'mother' or self.navb.kw.get('subcat') == 'mother':
            dcols, cols   = [x[0] for x in precols], precols
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=mother&id=%s">View</a>' % (x), }) 
            nat = Nutrition.fetch_log_mothers(pre_cnds, dcols)
          else:
            dcols, cols   = [x[0] for x in chicols], chicols
            markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=bir&id=%s">View</a>' % (x), }) 
            nat = Nutrition.fetch_log_children(chi_cnds, dcols)

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
                        
            if self.navb.kw.get('subcat') in [x[0] for x in CHIINDICS]:
                #print PRE_INDICS, LOCS, cnds, group_by
                locateds = Nutrition.fetch_children_by_location(chi_cnds, group_by = group_by, INDICS = CHIINDICS)
            elif self.navb.kw.get('subcat') in [x[0] for x in PREINDICS]:
                 #print INDICS, LOCS, cnds, group_by
                 locateds = Nutrition.fetch_mothers_by_location(pre_cnds, group_by = group_by, INDICS = PREINDICS)
            else:
                INDICS = CHIINDICS + PREINDICS
                locateds = Nutrition.fetch_children_by_location(chi_cnds, group_by = group_by, INDICS = CHIINDICS)
                locateds += Nutrition.fetch_mothers_by_location(pre_cnds, group_by = group_by, INDICS = PREINDICS)
                #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()

            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular 
        
        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'Nutrition%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc or group ) ) )

        #print INDICS_HEADERS, tabular, locateds
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)




    
        
    
