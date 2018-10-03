# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.ccm import CCM
from sms.api.messaging.zdmapper.mappers.childmapper import Childmapper
from sms.api.messaging.zdmapper.mappers.ccmmapper import CCMmapper
import datetime

class CMRmapper(object):
    """ CMR map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.cmr = CCM(report.nid, report.birth_date, report.child_number)
        self.cmr.table = self.cmr.table2
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.child = Childmapper(report)
        self.ccmmapper = CCMmapper(report)

    def get_unique_query(self):
        try:
            self.child_pk = getattr(self, 'child_pk') if hasattr(self, 'child_pk') else None
            self.ccm_pk = getattr(self, 'report_pk') if hasattr(self, 'report_pk') else None
            self.curr_symptom_dict = {
                                    'symptom_ib': self.codes(self.current_symptoms, 'ib'),
                                    'symptom_db': self.codes(self.current_symptoms, 'db'),
                                    'symptom_di': self.codes(self.current_symptoms, 'di'),
                                    'symptom_ma': self.codes(self.current_symptoms, 'ma'),
                                    'symptom_np': self.codes(self.current_symptoms, 'np'),
                                    'symptom_oi': self.codes(self.current_symptoms, 'oi'),
                                    'symptom_pc': self.codes(self.current_symptoms, 'pc'),
                                    'symptom_nv': self.codes(self.current_symptoms, 'nv'),
                                    }

            self.UNIQUE_QUERY = self.filters_of_dict_keys(self.curr_symptom_dict)
            self.UNIQUE_QUERY.update( {"child_pk = %s": self.child_pk })
            if self.ccm_pk: self.UNIQUE_QUERY.update( {"ccm_pk = %s": self.ccm_pk })
        except Exception, e:
            print "UNIQUE CMR: %s" % e
        return self

    def get_fields(self):

        try:
            child = self.child.store()
            self.child_pk = child.indexcol
            self.mother_pk = child.mother_pk
            self.pregnancy_pk = child.pregnancy_pk
            
            self.health_status = getattr(self, 'child_status') if hasattr(self, 'child_status') else None
            self.ccm_pk = getattr(self, 'report_pk') if hasattr(self, 'report_pk') else None
            indexcol = None
            self.get_unique_query()
            #print self.UNIQUE_QUERY
            cmr = self.cmr.get_cmr(self.UNIQUE_QUERY)
            if cmr:
                indexcol = cmr.indexcol
                self.created_at = cmr.created_at
            self.FIELDS.update(self.curr_symptom_dict)
            self.FIELDS.update( {
                                  'indexcol' : indexcol,
                                  'created_at' : self.created_at,
                                  'updated_at' : self.updated_at,
                                  'national_id' : self.national_id,
                                  'mother_pk': self.mother_pk,
                                  'user_phone' : self.user_phone,
                                  'user_pk' : self.user_pk,
                                  'role_pk' : self.role_pk,
                                  'nation_pk' : self.nation_pk,
                                  'province_pk' : self.province_pk,
                                  'district_pk' : self.district_pk,
                                  'referral_facility_pk' : self.referral_facility_pk,
                                  'facility_pk' : self.facility_pk,
                                  'sector_pk' : self.sector_pk,
                                  'cell_pk' : self.cell_pk,
                                  'village_pk' : self.village_pk,

                                  'birth_date' : self.birth_date,
                                  'child_number' : self.child_number,
                                  'pregnancy_pk' : self.pregnancy_pk,
                                  'child_pk': self.child_pk,
                                  'ccm_pk': self.ccm_pk,

                                 'intervention': self.code(self.intervention),
                                 'health_status': self.code(self.health_status),
                                 
                                 'message' : self.message.text,
                                 'is_valid': True 

                                
                                }
                        )
            #print self.FIELDS
        except Exception, e:
            print "FIELDS CMR: %s" % e
            pass

        return self

    def store(self):
        try:    
            cmr  =   self.cmr.save_cmr(self.orm, self.get_fields())
            return cmr             
        except Exception, e:
            print "STORE CMR: %s" % e
            pass
        return None
