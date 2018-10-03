#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


## MAP SMS_REPORT_KEYS TO MCH TABLES FIELDS
## E.G: pregnancy FIELDS


from model.pregnancy import Pregnancy
from sms.api.messaging.zdmapper.mappers.mothermapper import Mothermapper

class Premapper(object):
    """ Premapper map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.pre = Pregnancy(report.nid, report.lmp)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.mother = Mothermapper(report)
        #print "PREGNANCY: ",  self.pre.__dict__

    def get_fields(self):

        try:
            mother = self.mother.store()
            mother_pk = mother.indexcol
            
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

                                  'lmp' : self.lmp,
                                  'anc2_date' : self.anc2_date,
                                  'gravidity' : self.gravidity,
                                  'parity' : self.parity,
                                  
                                  'prev_pregnancy_gs' : self.codes(self.previous_symptoms, 'gs'),
                                  'prev_pregnancy_hd' : self.codes(self.previous_symptoms, 'hd'),
                                  'prev_pregnancy_kx' : self.codes(self.previous_symptoms, 'kx'),
                                  'prev_pregnancy_lz' : self.codes(self.previous_symptoms, 'lz'),
                                  'prev_pregnancy_mu' : self.codes(self.previous_symptoms, 'mu'),
                                  'prev_pregnancy_nr' : self.codes(self.previous_symptoms, 'nr'),
                                  'prev_pregnancy_ol' : self.codes(self.previous_symptoms, 'ol'),
                                  'prev_pregnancy_rm' : self.codes(self.previous_symptoms, 'rm'),
                                  'prev_pregnancy_yg' : self.codes(self.previous_symptoms, 'yg'),
                                  'prev_pregnancy_yj' : self.codes(self.previous_symptoms, 'yj'),    
            
                                  'symptom_af' : self.codes(self.current_symptoms, 'af'),
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
                                  
                                  'location' : self.code(self.location),
                                  'mother_weight' : self.mother_weight,
                                  'mother_height' : self.mother_height,

                                  'toilet' : self.code(self.toilet),
                                  'handwash' : self.code(self.handwashing),    

                                  'bmi': self.bmi,
                                  'muac' : self.muac,
                                  'message' : self.message.text,
                                  'is_valid' : True
                                
                                }
                        )
            
        except Exception, e:
            print "FIELDS: %s" % e
            pass

        return self

    def store(self):
        try:    
            preg  =   self.pre.save(self.orm, self.get_fields())
            return preg             
        except Exception, e:
            print "Store: %s" % e
            pass
        return None
 

