# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.childhealth import Childhealth
from sms.api.messaging.zdmapper.mappers.childmapper import Childmapper
import datetime

class Chimapper(object):
    """ Childhealth map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.chi = Childhealth(report.nid, report.birth_date, report.child_number)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.child = Childmapper(report)

    def get_unique_query(self):
        try:
            vac = ("lower(vaccine) LIKE %s", '%%%s%%' % self.vaccine.lower() ) if hasattr(self, 'vaccine') else ("vaccine IS NULL", '')
            comp = ("lower(vaccine_status) LIKE %s", '%%%s%%' % self.vaccine_completion.lower()
                    ) if hasattr(self, 'vaccine_completion') else ("vaccine_status IS NULL", '')
            self.UNIQUE_QUERY = { "child_pk = %s": self.child_pk,
                                    vac[0] : vac[1],
                                    comp[0] : comp[1] }

        except Exception, e:
            print "UNIQUE CHI: %s " % e
        return self

    def get_fields(self):

        try:
            child = self.child.store()
            self.child_pk = child.indexcol
            self.mother_pk = child.mother_pk
            self.pregnancy_pk = child.pregnancy_pk

            indexcol = None
            self.get_unique_query()
            chi = self.chi.get(self.UNIQUE_QUERY)
            self.vaccine = self.vaccine if hasattr(self, 'vaccine') else ''
            self.current_symptoms = self.current_symptoms if hasattr(self, 'current_symptoms') else ''
            if chi:
                indexcol = chi.indexcol
                self.created_at = chi.created_at

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

                                  'vaccine': self.code(self.vaccine),
                                  'vaccine_status': self.code(self.vaccine_completion),

                                  'symptom_ib' : self.codes(self.current_symptoms, 'ib'),
                                  'symptom_db' : self.codes(self.current_symptoms, 'db'),
                                  'symptom_np' : self.codes(self.current_symptoms, 'np'),

                                 'location' : self.code(self.location),
                                 'child_weight': self.child_weight,
                                 'muac' : self.muac,
                                 
                                 'message' : self.message.text,
                                 'is_valid': True 

                                
                                }
                        )
            #print self.FIELDS
        except Exception, e:
            print "FIELDS CHI: %s" % e
            pass

        return self

    def store(self):
        try:    
            chi  =   self.chi.save(self.orm, self.get_fields())
            return chi             
        except Exception, e:
            print "STORE CHI: %s" % e
            pass
        return None
