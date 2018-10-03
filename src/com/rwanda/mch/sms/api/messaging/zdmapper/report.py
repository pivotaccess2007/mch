#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from model.mother import Mother
import datetime

from sms.api.messaging.zdmapper.mappers import cbnmapper, cmrmapper, ccmmapper, pncmapper, nbcmapper, rarmapper, resmapper, dthmapper, chimapper, birmapper, redmapper, riskmapper, depmapper, ancmapper, refmapper, premapper

SAVE_MAPPERS = {
		     "CBN" : cbnmapper.Cbnmapper, 

		     "CMR" : cmrmapper.CMRmapper, 

		     "CCM" : ccmmapper.CCMmapper, 

		     "PNC" : pncmapper.Pncmapper, 

		     "NBC" : nbcmapper.Nbcmapper, 

		     "RAR" : rarmapper.Rarmapper, 

		     "RES" : resmapper.Resmapper, 

		     "DTH" : dthmapper.Deathmapper, 

		     "CHI" : chimapper.Chimapper, 

		     "BIR" : birmapper.Birthmapper, 

		     "RED" : redmapper.Redmapper, 

		     "RISK" : riskmapper.Riskmapper, 

		     "DEP" : depmapper.Depmapper, 

		     "ANC" : ancmapper.Ancmapper, 

		     "REF" : refmapper.Refmapper, 

		     "PRE" : premapper.Premapper 
            }

class Report(object):
    """ SMS report object, ready for persistance in the db """

    def __init__(self, rectifier):
        self.rectifier = rectifier
        self.codes = lambda y, x: x.lower() if x in [ c.lower() for c in y] else None
        self.code = lambda x: x[0].lower() if len(x) == 1 else None
        self.init_fields(rectifier)
        self.__dict__.update(rectifier.__dict__)
        self.filters_of_dict_keys = lambda x: self.process_filters_of_dict_keys(x)
        self.mapper = SAVE_MAPPERS.get(rectifier.report.keyword)(self)

    def save(self):
        try:
            pointeur = self.mapper.store()        
        except Exception, e:
            print e
            self.rectifier.errors.append( ['MCH_DB_REPORT_SAVE_ERROR',
                                            'MCH_DB_REPORT_SAVE_ERROR: %s' % self.errmessages.get('invalid').get('unknown_error').get('rw')
                                            ]
                                        )
        return self.rectifier

    def init_fields(self, rectifier):
        enduser = rectifier.chw
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.national_id = rectifier.nid
        self.user_phone = enduser.telephone
        self.user_pk = enduser.indexcol
        self.role_pk = enduser.role_pk
        self.nation_pk = enduser.nation_pk
        self.province_pk = enduser.province_pk
        self.district_pk = enduser.district_pk
        self.referral_facility_pk = enduser.referral_facility_pk
        self.facility_pk = enduser.facility_pk
        self.sector_pk = enduser.sector_pk
        self.cell_pk = enduser.cell_pk
        self.village_pk = enduser.village_pk
        return True

    def process_filters_of_dict_keys(self, ans):
        vs = {}
        for k in ans.keys():
            v = ans.get(k)
            if v: vs.update({'%s IS NOT NULL' % k : ''})
        return vs
        
        
        
