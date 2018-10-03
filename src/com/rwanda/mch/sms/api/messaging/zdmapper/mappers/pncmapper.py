# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.pncvisit import Pncvisit
from sms.api.messaging.zdmapper.mappers.mothermapper import Mothermapper

class Pncmapper(object):
    """ Pncmapper map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.pnc = Pncvisit(report.nid, report.delivery_date, report.pnc_visit)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.mother = Mothermapper(report)

    def get_unique_query(self):
        try:
            self.UNIQUE_QUERY =  {"pregnancy_pk = %s": self.pregnancy_pk,
                                        "lower(pnc_visit) LIKE %s" : '%%%s%%' % self.pnc_visit.lower()
                                             }
        except Exception, e:
            print "UNIQUE PNC: %s" % e
        return self

    def get_fields(self):

        try:
            mother = self.mother.get()
            mother_pk = mother.indexcol
            self.health_status = getattr(self, 'mother_status') if hasattr(self, 'mother_status') else None

            self.FIELDS.update( {
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

                                  'delivery_date' : self.pnc.delivery_date,
                                  'pregnancy_pk' : self.pregnancy_pk,
                                  'child_pk': self.child_pk,
                                  'pnc_visit' : self.code(self.pnc_visit),

                                  'symptom_ch' : self.codes(self.current_symptoms, 'ch'),
                                  'symptom_di' : self.codes(self.current_symptoms, 'di'),
                                  'symptom_ds' : self.codes(self.current_symptoms, 'ds'),
                                  'symptom_fe' : self.codes(self.current_symptoms, 'fe'),
                                  'symptom_fp' : self.codes(self.current_symptoms, 'fp'),
                                  'symptom_hy' : self.codes(self.current_symptoms, 'hy'),
                                  'symptom_ja' : self.codes(self.current_symptoms, 'ja'),
                                  'symptom_ma' : self.codes(self.current_symptoms, 'ma'),
                                  'symptom_np' : self.codes(self.current_symptoms, 'np'),
                                  'symptom_ns' : self.codes(self.current_symptoms, 'ns'),
                                  'symptom_oe' : self.codes(self.current_symptoms, 'oe'),
                                  'symptom_pc' : self.codes(self.current_symptoms, 'pc'),
                                  'symptom_sa' : self.codes(self.current_symptoms, 'sa'),
                                  'symptom_rb' : self.codes(self.current_symptoms, 'rb'),
                                  'symptom_vo' : self.codes(self.current_symptoms, 'vo'),   
                                  
                                  'intervention': self.code(self.intervention),
                                  'health_status': self.code(self.health_status), 

                                  'message' : self.message.text,
                                  'is_valid' : True
                                }
                        )

        except Exception, e:
            print "FIELDS PNC: %s" % e
            pass

        return self

    def store(self):
        try:    
            pnc  =   self.pnc.save(self.orm, self.get_fields(), self.pnc1)
            return pnc             
        except Exception, e:
            print "STORE PNC: %s" % e
            pass
        return None
