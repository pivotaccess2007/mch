# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.nbcvisit import Nbcvisit
from model.childhealth import Childhealth
from sms.api.messaging.zdmapper.mappers.childmapper import Childmapper

class Nbcmapper(object):
    """ Nbcmapper map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.nbc = Nbcvisit(report.nid, report.birth_date, report.child_number, report.nbc_visit)
        self.chi = Childhealth(report.nid, report.birth_date, report.child_number)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.child = Childmapper(report)

    def get_unique_query(self):
        try:
            self.UNIQUE_QUERY =  {"child_pk = %s": self.child_pk,
                                        "lower(nbc_visit) LIKE %s" : '%%%s%%' % self.nbc_visit.lower()
                                             }
        except Exception, e:
            print "UNIQUE NBC: %s" % e
        return self

    def get_fields(self):

        try:
            child = self.child.get()
            self.child_pk = child.indexcol
            self.mother_pk = child.mother_pk
            self.pregnancy_pk = child.pregnancy_pk
            
            indexcol = None
            self.get_unique_query()
            nbc = self.nbc.get()
            if nbc:
                indexcol = nbc.indexcol
                self.created_at = nbc.created_at
            #print "HERE 0"
            self.health_status = getattr(self, 'child_status') if hasattr(self, 'child_status') else None
            self.nbc1 = True if hasattr(self, 'nbc1') and self.nbc1.strip().lower() in ['yego', 'yes', 'oui'] else False
            self.v2   = True if hasattr(self, 'v2') and self.v2.strip().lower() in ['yego', 'yes', 'oui'] else False
            #print "HERE 1", self.FIELDS
            self.FIELDS.update( {
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

                                  'birth_date' : self.nbc.birth_date,
                                  'child_number': self.child_number,
                                  'pregnancy_pk' : self.pregnancy_pk,
                                  'child_pk': self.child_pk,
                                  'nbc_visit' : self.code(self.nbc_visit),

                                  'symptom_af' : self.codes(self.current_symptoms, 'af'),
                                  'symptom_ci' : self.codes(self.current_symptoms, 'ci'),
                                  'symptom_cm' : self.codes(self.current_symptoms, 'cm'),
                                  'symptom_np' : self.codes(self.current_symptoms, 'np'),
                                  'symptom_pm' : self.codes(self.current_symptoms, 'pm'),
                                  'symptom_rb' : self.codes(self.current_symptoms, 'rb'),   
                                  
                                  'breastfeeding' : self.code(self.breastfeeding),
                                  'intervention': self.code(self.intervention),
                                  'health_status': self.code(self.health_status), 

                                  'message' : self.message.text,
                                  'is_valid' : True
                                }
                        )
            #print "HERE 2", self.FIELDS
            self.V2_FIELDS = {
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

                                  'vaccine': 'v2',
                                  'vaccine_status': 'vc',

                                  'symptom_ib' : self.codes(self.current_symptoms, 'ib'),
                                  'symptom_db' : self.codes(self.current_symptoms, 'db'),
                                  'symptom_np' : self.codes(self.current_symptoms, 'np'),

                                 'location' : 'hc',
                                 'child_weight': child.child_weight,
                                 
                                 'message' : self.message.text,
                                 'is_valid': True 

                                
                                }
            #print self.FIELDS
        except Exception, e:
            print "FIELDS NBC: %s" % e
            pass

        return self

    def store(self):
        try:    
            nbc  =   self.nbc.save(self.orm, self.get_fields(), self.nbc1)
            if self.v2:
                self.chi.FIELDS = self.V2_FIELDS
                self.chi.UNIQUE_QUERY = {'lower(vaccine) LIKE %s': '%%%s%%' % 'v2', 'child_pk = %s': self.child_pk}
                print self.chi.FIELDS
                chi  =   self.chi.save(self.orm, self.chi)
            return nbc             
        except Exception, e:
            print "STORE NBC: %s" % e
            pass
        return None
