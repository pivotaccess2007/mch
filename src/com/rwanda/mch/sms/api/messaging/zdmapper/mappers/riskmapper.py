# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.risk import Risk
from sms.api.messaging.zdmapper.mappers.mothermapper import Mothermapper
import datetime

class Riskmapper(object):
    """ Risk map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.risk = Risk(report.nid, report.pregnancy_pk)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.mother = Mothermapper(report)

    def get_unique_query(self):
        try:
            self.curr_symptom_dict = {
                                        'symptom_af' : self.codes(self.current_symptoms, 'af'),
                                        'symptom_ch' : self.codes(self.current_symptoms, 'ch'),
                                        'symptom_di' : self.codes(self.current_symptoms, 'di'),
                                        'symptom_ds' : self.codes(self.current_symptoms, 'ds'),
                                        'symptom_fe' : self.codes(self.current_symptoms, 'fe'),
                                        'symptom_fp' : self.codes(self.current_symptoms, 'fp'),
                                        'symptom_hy' : self.codes(self.current_symptoms, 'hy'),
                                        'symptom_ja' : self.codes(self.current_symptoms, 'ja'),
                                        'symptom_ma' : self.codes(self.current_symptoms, 'ma'),
                                        'symptom_ns' : self.codes(self.current_symptoms, 'ns'),
                                        'symptom_oe' : self.codes(self.current_symptoms, 'oe'),
                                        'symptom_pc' : self.codes(self.current_symptoms, 'pc'),
                                        'symptom_sa' : self.codes(self.current_symptoms, 'sa'),
                                        'symptom_rb' : self.codes(self.current_symptoms, 'rb'),
                                        'symptom_vo' : self.codes(self.current_symptoms, 'vo')
                                        }

            self.UNIQUE_QUERY = self.filters_of_dict_keys(self.curr_symptom_dict)
            self.UNIQUE_QUERY.update( {"pregnancy_pk %s" % ("= %s" % self.pregnancy_pk if self.pregnancy_pk else "IS NULL"): ''})

        except Exception, e:
            print "UNIQUE RISK: %s" % e
        return self

    def get_fields(self):

        try:
            mother = self.mother.store()
            mother_pk = mother.indexcol
            
            self.get_unique_query()            
            #print self.UNIQUE_QUERY
            self.FIELDS.update(self.curr_symptom_dict)
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

                                  'pregnancy_pk' : self.pregnancy_pk,

                                  'location' : self.code(self.location),
                                  'mother_weight' : self.mother_weight,

                                  'message' : self.message.text,
                                  'is_valid' : True
                                }
                        )

        except Exception, e:
            print "FIELDS RISK: %s" % e
            pass

        return self

    def store(self):
        try:    
            risk  =   self.risk.save(self.orm, self.get_fields())
            return risk             
        except Exception, e:
            print "STORE RISK: %s" % e
            pass
        return None
