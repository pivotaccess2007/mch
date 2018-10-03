# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.redalert import Redresult
from sms.api.messaging.zdmapper.mappers.mothermapper import Mothermapper
from sms.api.messaging.zdmapper.mappers.redmapper import Redmapper
import datetime

class Rarmapper(object):
    """ Redresult map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.rar = Redresult(report.nid, pregnancy_pk = report.pregnancy_pk,  birth_date = None, child_number = None )
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.mother = Mothermapper(report)
        self.redmapper =  Redmapper(report)

    def get_unique_query(self):
        try:
            self.child_pk = getattr(self, 'child_pk') if hasattr(self, 'child_pk') else None
            self.pregnancy_pk = getattr(self, 'pregnancy_pk') if hasattr(self, 'pregnancy_pk') else None
            self.red_pk = getattr(self, 'report_pk') if hasattr(self, 'report_pk') else None
            self.red_symptom_dict = {
                            'red_symptom_ads' : self.codes(self.red_symptoms, 'ads'),
                            'red_symptom_cdg' : self.codes(self.red_symptoms, 'cdg'),
                            'red_symptom_co' : self.codes(self.red_symptoms, 'co'),
                            'red_symptom_con' : self.codes(self.red_symptoms, 'con'),
                            'red_symptom_hbt' : self.codes(self.red_symptoms, 'hbt'),
                            'red_symptom_hfp' : self.codes(self.red_symptoms, 'hfp'),
                            'red_symptom_iuc' : self.codes(self.red_symptoms, 'iuc'),
                            'red_symptom_lbt' : self.codes(self.red_symptoms, 'lbt'),
                            'red_symptom_mc' : self.codes(self.red_symptoms, 'mc'),
                            'red_symptom_nbf' : self.codes(self.red_symptoms, 'nbf'),
                            'red_symptom_ncb' : self.codes(self.red_symptoms, 'ncb'),
                            'red_symptom_nhe' : self.codes(self.red_symptoms, 'nhe'),
                            'red_symptom_nsc' : self.codes(self.red_symptoms, 'nsc'),
                            'red_symptom_nuf' : self.codes(self.red_symptoms, 'nuf'),
                            'red_symptom_pa' : self.codes(self.red_symptoms, 'pa'),
                            'red_symptom_ps' : self.codes(self.red_symptoms, 'ps'),
                            'red_symptom_rv' : self.codes(self.red_symptoms, 'rv'),
                            'red_symptom_sbp': self.codes(self.red_symptoms, 'sbp'),
                            'red_symptom_sfh': self.codes(self.red_symptoms, 'sfh'),
                            'red_symptom_shb': self.codes(self.red_symptoms, 'shb'),
                            'red_symptom_shp': self.codes(self.red_symptoms, 'shp'),
                            'red_symptom_sp': self.codes(self.red_symptoms, 'sp'),
                            'red_symptom_wu': self.codes(self.red_symptoms, 'wu'),
                            'red_symptom_ys': self.codes(self.red_symptoms, 'ys'),
                            'red_symptom_ap': self.codes(self.red_symptoms, 'ap'),
                            'red_symptom_bsp': self.codes(self.red_symptoms, 'bsp'),
                            'red_symptom_cop': self.codes(self.red_symptoms, 'cop'),
                            'red_symptom_he': self.codes(self.red_symptoms, 'he'),
                            'red_symptom_la': self.codes(self.red_symptoms, 'la'),
                            'red_symptom_sc': self.codes(self.red_symptoms, 'sc'),
                            'red_symptom_sl': self.codes(self.red_symptoms, 'sl'),
                            'red_symptom_nt': self.codes(self.red_symptoms, 'nt'),
                            'red_symptom_rsb': self.codes(self.red_symptoms, 'rsb'),
                            'red_symptom_un': self.codes(self.red_symptoms, 'un')
                        }
            self.UNIQUE_QUERY = self.filters_of_dict_keys(self.red_symptom_dict)
            self.UNIQUE_QUERY.update( { "national_id = %s" : self.nid })
            if self.red_pk: self.UNIQUE_QUERY.update( { "red_pk = %s" : self.red_pk })
            if self.pregnancy_pk: self.UNIQUE_QUERY.update( { "pregnancy_pk = %s": self.pregnancy_pk })
            if self.child_pk:   self.UNIQUE_QUERY.update( { "child_pk = %s" : self.child_pk })

        except Exception, e:
            print "UNIQUE RAR: %s" % e
        return self

    def get_fields(self):

        try:
            mother = self.mother.store()
            mother_pk = mother.indexcol
            birth_date = getattr(self, 'birth_date') if hasattr(self, 'birth_date') else None
            child_number = getattr(self, 'child_number') if hasattr(self, 'child_number') else None
            self.child_pk = getattr(self, 'child_pk') if hasattr(self, 'child_pk') else None
            self.pregnancy_pk = getattr(self, 'pregnancy_pk') if hasattr(self, 'pregnancy_pk') else None
            self.red_pk = getattr(self, 'report_pk') if hasattr(self, 'report_pk') else None
            self.health_status = getattr(self, 'mother_status') if hasattr(self, 'mother_status') else None
            if not self.health_status: self.health_status = getattr(self, 'child_status') if hasattr(self, 'child_status') else None
            
            self.get_unique_query()            
            #print self.UNIQUE_QUERY
            self.FIELDS.update(self.red_symptom_dict)
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

                                  'birth_date' : birth_date,
                                  'child_number' : child_number,
                                  'pregnancy_pk' : self.pregnancy_pk,
                                  'child_pk' : self.child_pk,
                                  'red_pk': self.red_pk,

                                  'location' : self.code(self.location),
                                  'intervention': self.code(self.intervention),
                                  'health_status': self.code(self.health_status), 

                                  'message' : self.message.text,
                                  'is_valid' : True
                                }
                        )

        except Exception, e:
            print "FIELDS RAR: %s" % e
            pass

        return self

    def store(self):
        try:    
            rar  =   self.rar.save(self.orm, self.get_fields())
            return rar             
        except Exception, e:
            print "STORE RAR: %s" % e
            pass
        return None
