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
from model.pregnancy import Pregnancy
from util import queries
from util.mch_util import makecol, makedict, give_me_table


class PregnancyController(RSMSRWController):
    
    def __init__(self, navb):
        navb.gap  = timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT PREGNANCY, AND LET THE USER GO BACK AND FORTH
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})#;print cnds         
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Pregnancy.fetch_pregnancies(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})#;print cnds         
        exts = {}
        cols = ['COUNT(*) AS total']
        title, group, attrs, nat = ('', '', [], [])#; print self.navb.kw 
        if self.navb.kw.get('group') == 'no_risk':
          title = 'No Risk'
          group = 'no_risk'
          cnds.update({queries.NO_RISK['query_str']: ''})
          cols = ['COUNT(*) AS total']
          nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)
        elif self.navb.kw.get('group') == 'at_risk':
          title = 'At Risk'
          group = 'at_risk'
          cnds.update({queries.RISK['query_str']: ''})
          attrs = [(makecol(x[0]), x[1]) for x in queries.RISK['attrs']]
          exts.update(dict([( makecol(x[0]), ('COUNT(*)',x[0]) ) for x in queries.RISK['attrs'] ]))
          cols = ['COUNT(*) AS total']
          nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)
        elif self.navb.kw.get('group') == 'high_risk':
          title = 'High Risk'
          group = 'high_risk'
          cnds.update({queries.HIGH_RISK['query_str']: ''})
          attrs = [( makecol(x[0]), x[1]) for x in queries.HIGH_RISK['attrs'] ]
          exts.update(dict([( makecol(x[0]), ('COUNT(*)',x[0]) ) for x in queries.HIGH_RISK['attrs'] ]))
          cols = ['COUNT(*) AS total']
          nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)
        elif self.navb.kw.get('group') == 'toilet':
          title = 'With Toilet'
          group = 'toilet'
          cnds.update({"LOWER(toilet) = 'to'": ''})
          cols = ['COUNT(*) AS total']
          nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)
        elif self.navb.kw.get('group') == 'handwash':
          title = 'With Handwashing'
          group = 'handwash'
          cnds.update({"LOWER(handwash) = 'hw'": ''})
          cols = ['COUNT(*) AS total']
          nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)

        elif self.navb.kw.get('group') == 'notoilet':
          title = 'No Toilet'
          group = 'notoilet'
          cnds.update({"LOWER(toilet) = 'nt'": ''})
          cols = ['COUNT(*) AS total']
          nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)
        elif self.navb.kw.get('group') == 'nohandwash':
          title = 'No Handwashing'
          group = 'nohandwash'
          cnds.update({"LOWER(handwash) = 'nh'": ''})
          cols = ['COUNT(*) AS total']
          nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)
        else:
          cols = ['COUNT(*) AS total']
          exts = {'no_risk': ('COUNT(*)', queries.NO_RISK['query_str']), 
					    'at_risk': ('COUNT(*)', queries.RISK['query_str']),
					    'high_risk': ('COUNT(*)', queries.HIGH_RISK['query_str']),
                        'toilet': ('COUNT(*)', "LOWER(toilet) = 'to'"),
					    'notoilet': ('COUNT(*)', "LOWER(toilet) = 'nt'"),
                        'handwash': ('COUNT(*)', "LOWER(handwash) = 'hw'"),
					    'nohandwash': ('COUNT(*)', "LOWER(handwash) = 'nh'")					
					    }
          nat = Pregnancy.fetch_pregnancies(cnds, cols, exts) 
        #print title, group, attrs, "NAT: ", nat[0].__dict__
        return (title, group, attrs, nat)


    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})#;print cnds         
        exts = {}
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('lmp', 'LMP'),
                                              ('gravidity', 'Gravidity'),
                                              ('parity', 'Parity'),
                                              ('mother_weight', 'Weight'),
                                              ('mother_height', 'Height'),
                                              ('bmi', 'BMI'),
                                              ('created_at', 'Submission Date'),
                                              ('indexcol', 'ID')
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=pre&id=%s">View</a>' % (x), })

        #print cnds, markup, cols
        DESCRI = []
        HIGHRISKDICT = makedict(queries.HIGH_RISK['attrs'])
        RISKDICT = makedict(queries.RISK['attrs'])
        INDICS = []
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])#; print self.navb.kw 
        if self.navb.kw.get('subcat') is not None:
            sc = self.navb.kw.get('subcat')#;print RISKDICT
            wcl = HIGHRISKDICT.get(sc) or RISKDICT.get(sc)#;print wcl
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            cnds.update({wcl[0]: ''})
            dcols = [x[0] for x in cols]#;print  "INDICS: ", INDICS
            #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        elif self.navb.kw.get('group') == 'no_risk':
          title = 'No Risk'
          group = 'no_risk'
          INDICS  = [(group, queries.NO_RISK['query_str'], title)]
          cnds.update({queries.NO_RISK['query_str']: ''})
          dcols = [x[0] for x in cols]#;print INDICS
          #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        elif self.navb.kw.get('group') == 'at_risk' and self.navb.kw.get('subcat') is None:
          title = 'At Risk'
          group = 'at_risk'
          INDICS  = [(group, queries.RISK['query_str'], title)]
          for k in RISKDICT.keys(): INDICS.append((k, RISKDICT[k][0], RISKDICT[k][1]))
          cnds.update({queries.RISK['query_str']: ''})
          dcols = [x[0] for x in cols]
          #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        elif self.navb.kw.get('group') == 'high_risk' and self.navb.kw.get('subcat') is None:
          title = 'High Risk'
          group = 'high_risk'
          INDICS  = [(group, queries.HIGH_RISK['query_str'], title)]
          for k in HIGHRISKDICT.keys(): INDICS.append((k, HIGHRISKDICT[k][0], HIGHRISKDICT[k][1]))
          cnds.update({queries.HIGH_RISK['query_str']: ''})
          dcols = [x[0] for x in cols]
          #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        elif self.navb.kw.get('group') == 'toilet':
          title = 'With Toilet'
          group = 'toilet'
          INDICS  = [(group, "LOWER(toilet) = 'to'", title)]
          cnds.update({"LOWER(toilet) = 'to'": ''})
          dcols = [x[0] for x in cols]
          #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        elif self.navb.kw.get('group') == 'handwash':
          title = 'With Handwashing'
          group = 'handwash'
          INDICS  = [(group, "LOWER(handwash) = 'hw'", title)]
          cnds.update({"LOWER(handwash) = 'hw'": ''})
          dcols = [x[0] for x in cols]
          #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        elif self.navb.kw.get('group') == 'notoilet':
          title = 'No Toilet'
          group = 'notoilet'
          INDICS  = [(group, "LOWER(toilet) = 'nt'", title)]
          cnds.update({"LOWER(toilet) = 'nt'": ''})
          dcols = [x[0] for x in cols]
          #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        elif self.navb.kw.get('group') == 'nohandwash':
          title = 'No Handwashing'
          group = 'nohandwash'
          INDICS  = [(group, "LOWER(handwash) = 'nh'", title)]
          cnds.update({"LOWER(handwash) = 'nh'": ''})
          dcols = [x[0] for x in cols]
          #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        else:
          dcols = [x[0] for x in cols]
          INDICS  = [   ("no_risk", queries.NO_RISK['query_str'], 'No Risk'),
                        ("at_risk", queries.RISK['query_str'], 'At Risk'),
                        ("high_risk", queries.HIGH_RISK['query_str'], 'High Risk'),
                        ("toilet", "LOWER(toilet) = 'to'", 'With toilet'),
                        ("handwash", "LOWER(handwash) = 'hw'", 'With handwashing'),  
                        ("notoilet", "LOWER(toilet) = 'nt'", 'With no toilet'),
                        ("nohandwash", "LOWER(handwash) = 'nh'", 'With no Handwashing')
                    ]
          #nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        
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
            locateds = Pregnancy.fetch_pregnancies_by_location(cnds, group_by = group_by, INDICS = INDICS)
            #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()
            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print tabular
        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
        DESCRI.append((group, title))
        desc  = 'Pregnancies%s' % (' (%s)' % (self.navb.find_descr(DESCRI + [(makecol(x[0]), x[2]) for x in INDICS],
                                                                        sc or self.navb.kw.get('group')
                                                                    ) 
					                            )
                                    ) 
        #print title, group, attrs, "NAT: ", nat[0].__dict__
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)

    def get_deilivery_notifications(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})#;print cnds         
        exts = {}
        cols = ['COUNT(*) AS total']
        title, group, attrs, nat = ('', '', [], [])
        today = self.navb.start#datetime.today().date()
        next_monday = today + timedelta(days=-today.weekday(), weeks=1)
        next_sunday = next_monday + timedelta(days = 6)
        next_two_monday = today + timedelta(days=-today.weekday(), weeks=2)
        next_two_sunday = next_two_monday + timedelta(days = 6)
        attrs = [
	                ('next_week', 'Deliveries in Next Week', 
                    "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (GESTATION , next_monday, next_sunday)),
	                ('next_two_week', 'Deliveries in Next two Weeks', 
                    "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (GESTATION , next_two_monday, next_two_sunday)),
	            ]
        exts.update(dict([(x[0], ('COUNT(*)',x[2])) for x in attrs]))
        nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)
        details = {}
        for attr in attrs:
            attr_cnds = self.navb.conditions()
            attr_cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
            attr_cnds.update({attr[2]: ''})
            cols = ['COUNT(*) AS total']
            exts = {'no_risk': ('COUNT(*)', queries.NO_RISK['query_str']), 
	             'at_risk': ('COUNT(*)', queries.RISK['query_str']),
                 'high_risk': ('COUNT(*)', queries.HIGH_RISK['query_str']),
	            }
            details.update({ attr[0] : Pregnancy.fetch_pregnancies(attr_cnds, cols, exts) })
        #print title, group, attrs, "NAT: ", nat[0].__dict__, details
        return (title, group, attrs, nat, details)


    def get_deilivery_notifications_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(lmp + INTERVAL \'%d days\') >= '%s'" % (GESTATION, self.navb.start) : ''})#;print cnds         
        
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('national_id',            'Mother ID'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('lmp', 'LMP'),
                                              ('gravidity', 'Gravidity'),
                                              ('parity', 'Parity'),
                                              ('mother_weight', 'Weight'),
                                              ('mother_height', 'Height'),
                                              ('bmi', 'BMI'),
                                              ('created_at', 'Submission Date')
                                              
                                            ])

        today = self.navb.start#datetime.today().date()
        next_monday = today + timedelta(days=-today.weekday(), weeks=1)
        next_sunday = next_monday + timedelta(days = 6)
        next_two_monday = today + timedelta(days=-today.weekday(), weeks=2)
        next_two_sunday = next_two_monday + timedelta(days = 6)
        attrs = [
	                ('next_week', 'Deliveries in Next Week', 
                    "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (GESTATION , next_monday, next_sunday)),
	                ('next_two_week', 'Deliveries in Next two Weeks', 
                    "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s'" % (GESTATION , next_two_monday, next_two_sunday)),
                    
	            ]

        INDICSDICT = { x[0]: (x[2], x[1]) for x in attrs}
        INDICS     = [ (x[0], x[2], x[1]) for x in attrs]        

        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])

        if self.navb.kw.get('subcat') is not None:
            sc = self.navb.kw.get('subcat')
            dcols = [x[0] for x in cols]
            wcl = INDICSDICT.get(sc);
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            if sc == 'next_week':
                INDICS +=  [('no_risk',
          "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_monday, next_sunday, queries.NO_RISK['query_str']),
                          'No Risk'), 
	                     ('at_risk',
         "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_monday, next_sunday, queries.RISK['query_str']),
                          'At Risk'),
                         ('high_risk',
        "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_monday, next_sunday, queries.HIGH_RISK['query_str']),
                         'High Risk')]
            elif sc == 'next_two_week':
                INDICS +=  [('no_risk',
      "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_two_monday, next_two_sunday, queries.NO_RISK['query_str']),
                          'No Risk'), 
	                     ('at_risk',
      "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_two_monday, next_two_sunday, queries.RISK['query_str']),
                          'At Risk'),
                         ('high_risk',
     "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_tow_monday, next_two_sunday, queries.HIGH_RISK['query_str']),
                          'High Risk')]
            
            INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
            cnds.update({wcl[0]: ''})
            nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)
            #print wcl, INDICSDICT, INDICS
        else:
            INDICS +=  [('no_risk',
          "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_monday, next_two_sunday, queries.NO_RISK['query_str']),
                          'No Risk'), 
	                     ('at_risk',
         "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_monday, next_two_sunday, queries.RISK['query_str']),
                          'At Risk'),
                         ('high_risk',
        "(lmp + INTERVAL '%s days') BETWEEN '%s' AND '%s' AND %s" % (GESTATION , next_monday, next_two_sunday, queries.HIGH_RISK['query_str']),
                         'High Risk')]
            dcols   = [x[0] for x in cols]
            nat = Pregnancy.fetch_log_pregnancies(cnds, dcols)

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
                        
            locateds = Pregnancy.fetch_pregnancies_by_location(cnds, group_by = group_by, INDICS = INDICS)
            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular

        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'Deliveries Notifications%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc ) ) )

        """
        nat = Pregnancy.fetch_pregnancies(cnds, cols, exts)
        details = {}
        for attr in attrs:
            attr_cnds = self.navb.conditions()
            attr_cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
            attr_cnds.update({attr[2]: ''})
            cols = ['COUNT(*) AS total']
            exts = {'no_risk': ('COUNT(*)', queries.NO_RISK['query_str']), 
	             'at_risk': ('COUNT(*)', queries.RISK['query_str']),
                 'high_risk': ('COUNT(*)', queries.HIGH_RISK['query_str']),
	            }
            details.update({ attr[0] : Pregnancy.fetch_pregnancies(attr_cnds, cols, exts) })
        #print title, group, attrs, "NAT: ", nat[0].__dict__, details
        """
        
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)


    
