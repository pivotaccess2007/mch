#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from controller.main import RSMSRWController
from model.ambulance import Ambulance
from util.mch_util import average, makedict, makecol 


class AmbulanceController(RSMSRWController):
    
    def __init__(self, navb):
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Ambulance.get_ambulances_summary(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cols    = ['COUNT(*) AS total']
        exts    = {}
        attrs   = []
        nat     = Ambulance.get_ambulances_summary(cnds, cols, exts)
        return [nat, attrs]

    def get_tables(self):
        cnds    = self.navb.conditions()#;print cnds
        if self.navb.kw.get("search") and self.navb.kw.get("identity"):
            mkw     = "%%%s%%" % self.navb.kw.get('identity').strip()
            #if self.navb.kw.get("search") == 'fac': cnds.update({"national_id LIKE %s": mkw })
            if self.navb.kw.get("search") == 'sim': cnds.update({"telephone LIKE %s": mkw })        
        exts = {}
        attrs = []
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('indexcol', 'ID'),
                                              ('telephone',              'Telephone'),
                                              ('coordinator', 'Coordinator'),
                                              ('province_pk', 'Province'),
                                              ('district_pk', 'District'),
                                              ('referral_facility_pk', 'Hospital'),
                                              ('facility_pk', 'Health Centre'),
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=amb&id=%s">View</a>' % (x), })
            
        sc      = self.navb.kw.get('subcat')
        #print cnds, markup, cols, sc, attrs

        DESCRI = []
        INDICS = []
        group = "Ambulance"
        title = "Ambulance List"

        dcols = [x[0] for x in cols]
        #print cnds
        nat = Ambulance.fetch_ambulances_table(cnds, dcols)
        #DESCRI.append((group, title))
        desc  = 'Ambulances%s' % (' (%s)' % (self.navb.find_descr(DESCRI + INDICS,
                                                                        sc or self.navb.kw.get('subcat')
                                                                    ) 
					                            )
                                    ) 
        #print INDICS, title, group, attrs, "NAT: ", nat[0].__dict__
        return (title, desc, group, attrs, markup, cols, nat)


    def register_ambulance(self):
        cnds    = self.navb.conditions()
        message = ''
        amb = None
        if self.navb.kw.get("amb_facility") and self.navb.kw.get('telephone_moh'):
            fac     = self.navb.kw.get('amb_facility')
            phone   = self.navb.kw.get('telephone_moh')
            formdata = {    
                            "telephone": phone, 
                            "coordinator": self.navb.kw.get('coordinator'),
                            "nation_pk": self.navb.kw.get('amb_nation'),
                            "province_pk": self.navb.kw.get('amb_province'),
                            "district_pk": self.navb.kw.get('amb_district'),
                            "referral_facility_pk": self.navb.kw.get('amb_hospital'),
                            "facility_pk" : fac
                        }

            #print "\nFORM: ", formdata, "\n"
            message, amb = Ambulance.get_or_create(formdata)
            self.navb.kw = {}
        
        return [message, amb]

