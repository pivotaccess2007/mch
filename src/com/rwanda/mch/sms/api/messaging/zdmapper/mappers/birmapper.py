# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.birth import Birth
from sms.api.messaging.zdmapper.mappers.childmapper import Childmapper
import datetime

class Birthmapper(object):
    """ Birth map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.bir = Birth(report.nid, report.birth_date, report.child_number)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.child = Childmapper(report)

    def get_fields(self):

        try:
            child = self.child.store()
            child_pk = child.indexcol
            if child: self.created_at = child.created_at
            mother_pk = child.mother_pk

            self.FIELDS.update( {
                                  'indexcol' : child_pk,
                                  'created_at' : self.created_at,
                                  'updated_at' : self.updated_at,
                                  'national_id' : self.national_id,
                                  'mother_pk': mother_pk,
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

                                  'symptom_af' : self.codes(self.current_symptoms, 'af'),
                                  'symptom_ci' : self.codes(self.current_symptoms, 'ci'),
                                  'symptom_cm' : self.codes(self.current_symptoms, 'cm'),
                                  'symptom_pm' : self.codes(self.current_symptoms, 'pm'),
                                  'symptom_np' : self.codes(self.current_symptoms, 'np'),
                                  'symptom_rb' : self.codes(self.current_symptoms, 'rb'),

                                 'location' : self.code(self.location),
                                 'breastfeeding' : self.code(self.breastfeeding),
                                 'child_weight': self.child_weight,

                                 'message' : self.message.text,
                                 'is_valid': True 

                                
                                }
                        )

        except Exception, e:
            print "FIELDS: %s" % e
            pass

        return self

    def store(self):
        try:    
            bir  =   self.bir.save(self.orm, self.get_fields())
            return bir             
        except Exception, e:
            print "STORE: %s" % e
            pass
        return None
