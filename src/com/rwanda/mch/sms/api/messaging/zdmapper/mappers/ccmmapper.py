# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.ccm import CCM
from sms.api.messaging.zdmapper.mappers.childmapper import Childmapper
import datetime

class CCMmapper(object):
    """ CCM map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.ccm = CCM(report.nid, report.birth_date, report.child_number)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.child = Childmapper(report)

    def get_unique_query(self):
        try:
            self.child_pk = getattr(self, 'child_pk') if hasattr(self, 'child_pk') else None
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

        except Exception, e:
            print "UNIQUE CCM: %s" % e
        return self

    def get_fields(self):

        try:
            child = self.child.store()
            self.child_pk = child.indexcol
            self.mother_pk = child.mother_pk
            self.pregnancy_pk = child.pregnancy_pk

            indexcol = None
            self.get_unique_query()
            ccm = self.ccm.get(self.UNIQUE_QUERY)
            if ccm:
                indexcol = ccm.indexcol
                self.created_at = ccm.created_at
            #print self.UNIQUE_QUERY
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

                                 'intervention': self.code(self.intervention),
                                 'muac' : self.muac,
                                 
                                 'message' : self.message.text,
                                 'is_valid': True 

                                
                                }
                        )
            #print self.FIELDS
        except Exception, e:
            print "FIELDS CCM: %s" % e
            pass

        return self

    def store(self):
        try:    
            ccm  =   self.ccm.save(self.orm, self.get_fields())
            return ccm             
        except Exception, e:
            print "STORE CCM: %s" % e
            pass
        return None
