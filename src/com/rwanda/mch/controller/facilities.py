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
from model.facility import Facility
from util.mch_util import average, makedict, makecol 


class FacilityController(RSMSRWController):
    
    def __init__(self, navb):
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        if self.navb.kw.get('factype'):
            facility_type = Facility.get_facility_type(self.navb.kw.get('factype').upper())
            cnds.update({ 'facility_type_pk = %s ': facility_type.indexcol })
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Facility.get_facilities_summary(cnds, cols)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        if self.navb.kw.get('factype'):
            facility_type = Facility.get_facility_type(self.navb.kw.get('factype').upper())
            cnds.update({ 'facility_type_pk = %s ': facility_type.indexcol })
        
        cols    = ['COUNT(*) AS total']
        exts    = {}
        attrs   = []
        nat     = Facility.get_facilities_summary(cnds, cols)
        self.navb.kw = {}
        return [nat, attrs]

    def get_tables(self):
        cnds    = self.navb.conditions()#;print cnds
        factpn  = ''
        if self.navb.kw.get('factype'):
            facility_type = Facility.get_facility_type(self.navb.kw.get('factype').upper())
            factpn = facility_type.name
            cnds.update({ 'facility_type_pk  = %s ': facility_type.indexcol })
        
        if self.navb.kw.get("search") and self.navb.kw.get("identity"):
            #print self.navb.kw.get("search"), self.navb.kw.get("identity")
            mkw     = self.navb.kw.get('identity').strip()
            if self.navb.kw.get("search") == 'code': cnds.update({"code = %s": mkw })        
        exts = {}
        attrs = []
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('indexcol', 'ID'),
                                              ('code',              'Fosa Code'),
                                              ('name', 'Name'),
                                              ('province_pk', 'Province'),
                                              ('district_pk', 'District'),
                                              ('referral_facility_pk', 'Referral Hospital'),
                                              ('sector_pk', 'Sector'),
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=fac&id=%s">View</a>' % (x), })
            
        sc      = self.navb.kw.get('subcat')
        #print cnds, markup, cols, sc, attrs

        DESCRI = []
        INDICS = []
        group = "Facility"
        title = "Facility List"

        dcols = [x[0] for x in cols]
        #print cnds
        nat = Facility.fetch_facilities_table(cnds, dcols)
        #DESCRI.append((group, title))
        desc  = 'Facilities%s' % (' (%s)' % (self.navb.find_descr(DESCRI + INDICS + [(self.navb.kw.get('factype'), factpn)],
                                                                        sc or self.navb.kw.get('factype')
                                                                    ) 
					                            )
                                    ) 
        #print INDICS, title, group, attrs, "NAT: ", nat[0].__dict__
        self.navb.kw = {}
        return (title, desc, group, attrs, markup, cols, nat)


    def register_facility(self):
        cnds    = self.navb.conditions()
        message = ''
        fac = None
        facs = []
        if self.navb.kw.get("facname") and self.navb.kw.get('faccode'):
            #print "PARAMS: ", self.navb.kw.get('ftype'), self.navb.kw.get('faccode')
            facility_type = Facility.get_facility_type(self.navb.kw.get('ftype').upper())
            old_fac = Facility.get_facility(self.navb.kw.get('faccode'))
            formdata = {    
                            "code": self.navb.kw.get('faccode'), 
                            "name": self.navb.kw.get('facname'),
                            "nation_pk": self.navb.kw.get('fac_nation'),
                            "province_pk": self.navb.kw.get('fac_province'),
                            "district_pk": self.navb.kw.get('fac_district'),    
                            "sector_pk": self.navb.kw.get('fac_sector'),
                            "referral_facility_pk": self.navb.kw.get('fac_hospital'),
                            'facility_type_pk': facility_type.indexcol
                        }

            #print "\nFORM: ", formdata, "\n"
            if old_fac:
                message, fac, facs = Facility.update_facility(formdata)
            else:
                message, fac, facs = Facility.get_or_create(formdata)
            self.navb.kw = {}
        
        return [message, fac, facs]


    def update_facility(self):
        cnds    = self.navb.conditions()
        message = ''
        fac = None
        facs = []
        if self.navb.kw.get("facname") and self.navb.kw.get('faccode'):            
            facility_type = Facility.get_facility_type(self.navb.kw.get('ftype').upper())
            old_fac = Facility.get_facility(self.navb.kw.get('faccode'))
            formdata = {    
                            "indexcol": old_fac.indexcol,
                            "code": self.navb.kw.get('faccode'), 
                            "name": self.navb.kw.get('facname'),
                            "nation_pk": self.navb.kw.get('fac_nation'),
                            "province_pk": self.navb.kw.get('fac_province'),
                            "district_pk": self.navb.kw.get('fac_district'),    
                            "sector_pk": self.navb.kw.get('fac_sector'),
                            "referral_facility_pk": self.navb.kw.get('fac_hospital'),
                            'facility_type_pk': facility_type.indexcol
                        }

            #print "\nFORM: ", formdata, "\n"
            message, fac, facs = Facility.update_facility(formdata)
            self.navb.kw = {}
        
        return [message, fac, facs]

