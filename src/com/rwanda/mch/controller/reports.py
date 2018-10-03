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
from model.report import Report
from model.pregnancy import Pregnancy
from model.refusal import Refusal
from model.departure import Departure
from model.ancvisit import Ancvisit
from model.pncvisit import Pncvisit
from model.nbcvisit import Nbcvisit
from model.birth import Birth
from model.risk import Risk
from model.riskresult import Riskresult
from model.childhealth import Childhealth
from model.nutrition import Nutrition
from model.ccm import CCM
from model.redalert import Redalert
from model.malaria import Malaria
from model.stock import Stock
from model.death import Death

from util import queries

from util.mch_util import makecol, give_me_table, parse_report_cols


class ReportController(RSMSRWController):
    
    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def extra_cnds(self, cnds, extra ={}):        
        try:    extra.update(cnds)
        except: pass
        return extra

    def get_report(self):
        cnds    = self.navb.conditions()
        report  = {}
        try:
            rcd = Report.get_report(self.navb.kw.get('tbl'), self.navb.kw.get('id'))
            #print "DB REDORD: ", rcd
            if rcd:
                try:
                    report = parse_report_cols(rcd)
                    #print "REPORT: ", report
                except Exception, e:
                    #print e
                    pass
        except Exception, e: 
            #print "ERROR READING REPORT: ", e
            pass

        return report

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})
        cols = ['COUNT(*) AS total']
        exts = {} 
        nat = [
                    ("pre", "Pregnancy", Pregnancy.fetch_pregnancies(cnds, cols, exts)),
                    ("anc", "Antenatal Consultation", Ancvisit.fetch_ancvisits(cnds, cols, exts)),
                    ("ref", "Refusal",  Refusal.fetch_refusals(cnds, cols, exts) ),
                    ("red", "Red Alert", Redalert.fetch_redalerts(cnds, cols, exts)),
                    ("rar", "Red Alert Result", Redalert.fetch_redresults(cnds, cols, exts)),
                    ("risk", "Risk", Risk.fetch_risks(cnds, cols, exts)),
                    ("res", "Risk Result", Risk.fetch_riskresults(cnds, cols, exts)),
                    ("dep", "Departure", Departure.fetch_departures(cnds, cols, exts)),
                    ("bir", "Birth", Birth.fetch_births(cnds, cols, exts)),
                    ("pnc", "Postnatal Care", Pncvisit.fetch_pncvisits(cnds, cols, exts)),
                    ("nbc", "Newborn Care", Nbcvisit.fetch_nbcvisits(cnds, cols, exts)),
                    ("chi", "Child Health", Childhealth.fetch_childhealths(cnds, cols, exts)),
                    ("cbn", "Community Based Nutrition", Nutrition.fetch_nutritions(cnds, cols, exts)),
                    ("ccm", "Community Case Management", CCM.fetch_ccms(cnds, cols, exts)),
                    ("cmr", "Case Management Response", CCM.fetch_cmrs(cnds, cols, exts)),
                    ("dth", "Death", Death.fetch_deaths(cnds, cols, exts)),
                    ("smn", "Severe Malaria", Malaria.fetch_malaria(self.extra_cnds(cnds, extra = {"keyword = 'SMN'": ''}), cols, exts)),
                    ("smr", "Severe Malaria Result", Malaria.fetch_malaria(self.extra_cnds(cnds, extra = {"keyword = 'SMR'": ''}), cols, exts)),
                    ("rso", "Risk Of Stock Out", Stock.fetch_stock(self.extra_cnds(cnds, extra = {"keyword = 'RSO'": ''}), cols, exts)),
                    ("so", "Stock out", Stock.fetch_stock(self.extra_cnds(cnds, extra = {"keyword = 'SO'": ''}), cols, exts)),
                    ("ss", "Stock Supplied", Stock.fetch_stock(self.extra_cnds(cnds, extra = {"keyword = 'SS'": ''}), cols, exts)),
                ]

        data = {}
        attrs = [(x[0], x[1]) for x in nat]
        total = 0
        for an in nat:
            try:
                value = an[2][0].total;print value, an[0]
                data.update( { an[0] : value } )
                total += value
            except Exception, e:
                print e
                data.update( { an[0] : 0 } )
                continue
        
         
        return [attrs, data, total]



    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})
        exts = {}
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('province_pk', 'Province'),
                                              ('district_pk', 'District'),
                                              ('referral_facility_pk', 'Hospital'),
                                              ('facility_pk', 'Health Centre'),
                                              ('sector_pk', 'Sector'),
                                              ('cell_pk', 'Cell'),
                                              ('village_pk', 'Village'),
                                              ('user_phone',            'Reporter Phone'),
                                              ('message', 'Message'),
                                              ('created_at', 'Submission Date')                                              
                                            ])


        INDICS = [
                    ("pre", 'total', "Pregnancy",
                            Pregnancy.fetch_log_pregnancies,
                            Pregnancy.fetch_pregnancies_by_location),
                    ("anc", 'total', "Antenatal Consultation",
                            Ancvisit.fetch_log_ancvisits,
                            Ancvisit.fetch_ancvisits_by_location),
                    ("ref", 'total', "Refusal",
                            Refusal.fetch_log_refusals,
                            Refusal.fetch_refusals_by_location ),
                    ("red", 'total', "Red Alert", 
                            Redalert.fetch_log_redalerts,
                            Redalert.fetch_redalerts_by_location),
                    ("rar", 'total', "Red Alert Result", 
                            Redalert.fetch_log_redresults,
                            Redalert.fetch_redresults_by_location),
                    ("risk", 'total', "Risk", 
                            Risk.fetch_log_risks,
                            Risk.fetch_risks_by_location),
                    ("res", 'total', "Risk Result", 
                            Riskresult.fetch_log_riskresults,
                            Riskresult.fetch_riskresults_by_location),
                    ("dep", 'total', "Departure", 
                            Departure.fetch_log_departures,
                            Departure.fetch_departures_by_location),
                    ("bir", 'total', "Birth", 
                            Birth.fetch_log_births,
                            Birth.fetch_births_by_location),
                    ("pnc", 'total', "Postnatal Care", 
                            Pncvisit.fetch_log_pncvisits,
                            Pncvisit.fetch_pncvisits_by_location),
                    ("nbc", 'total', "Newborn Care", 
                            Nbcvisit.fetch_log_nbcvisits,
                            Nbcvisit.fetch_nbcvisits_by_location),
                    ("chi", 'total', "Child Health", 
                            Childhealth.fetch_log_childhealths,
                            Childhealth.fetch_childhealths_by_location),
                    ("cbn", 'total', "Community Based Nutrition", 
                            Nutrition.fetch_log_nutritions,
                            Nutrition.fetch_nutritions_by_location),
                    ("ccm", 'total', "Community Case Management", 
                            CCM.fetch_log_ccms,
                            CCM.fetch_ccms_by_location),
                    ("cmr", 'total', "Case Management Response", 
                            CCM.fetch_log_cmrs,
                            CCM.fetch_cmrs_by_location),
                    ("dth", 'total', "Death", 
                            Death.fetch_log_deaths,
                            Death.fetch_deaths_by_location),
                    ("smn", 'total', "Severe Malaria", 
                            Malaria.fetch_log_malaria,
                            Malaria.fetch_malaria_by_location),
                    ("smr", 'total', "Severe Malaria Result", 
                            Malaria.fetch_log_malaria,
                            Malaria.fetch_malaria_by_location),
                    ("rso", 'total', "Risk Of Stock Out", 
                            Stock.fetch_log_stock,
                            Stock.fetch_stock_by_location),
                    ("so", 'total', "Stock out", 
                            Stock.fetch_log_stock,
                            Stock.fetch_stock_by_location),
                    ("ss", 'total', "Stock Supplied", 
                            Stock.fetch_log_stock,
                            Stock.fetch_stock_by_location),
                ]
            
        INDICSDICT = {x[0]: (x[1], x[2], x[3],x[4]) for x in INDICS}
        
        
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])

        if self.navb.kw.get('subcat'):
          sc = self.navb.kw.get('subcat')
          wcl  = INDICSDICT[sc]#;print wcl, INDICSDICT       
          INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
          INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
          if sc in ['smn', 'smr', 'rso', 'so', 'ss']: cnds = self.extra_cnds(cnds, extra = {"keyword = '%s'" % sc.upper(): ''})
          dcols   = [x[0] for x in cols ]
          nat = wcl[2](cnds, dcols)        
        else:
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
                        
            if self.navb.kw.get('subcat'):
                #print INDICS, LOCS, cnds, group_by
                wcl  = INDICSDICT[sc]
                INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
                INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
                locateds = wcl[3](cnds, group_by = group_by, INDICS = INDICS)
            else:
                INDICS = REDINDICS + RARINDICS
                locateds = Redalert.fetch_redalerts_by_location(cnds, group_by = group_by, INDICS = REDINDICS)
                locateds += Redalert.fetch_redresults_by_location(cnds, group_by = group_by, INDICS = RARINDICS)
                #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()

            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print locateds, "\n", tabular 
        
        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])
        desc  = 'Reports%s' % (' (%s)' % ( self.navb.find_descr( [(makecol(x[0]), x[2]) for x in INDICS], sc or group ) ) )

        #print INDICS_HEADERS, tabular, locateds
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)
    
        
    
