#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


from model.mother import Mother

class Mothermapper(object):
    """ Mothermapper map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.mother = Mother(report.nid)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}

    def get(self):
        try:
            return self.mother.get()
        except Exception, e:
            print "Mother NOT FOUND: %s" % e
            pass
        return None

    def get_fields(self):

        try:
            mother = self.mother.get()
            indexcol = None
            telephone = getattr(self, 'mother_phone') if hasattr(self, 'mother_phone') else None
            self.recent_mother_weight   = getattr(self, 'mother_weight') if hasattr(self, 'mother_weight') else None
            self.recent_mother_height   = getattr(self, 'mother_height') if hasattr(self, 'mother_height') else None
            self.recent_bmi             = getattr(self, 'bmi') if hasattr(self, 'bmi') else None
            self.recent_muac            = getattr(self, 'muac') if hasattr(self, 'muac') else None
            self.recent_lmp             = getattr(self, 'lmp') if hasattr(self, 'lmp') else None
            self.previous_mother_weight = getattr(mother, 'recent_mother_weight') if hasattr(mother, 'recent_mother_weight') else None
            self.previous_mother_height = getattr(mother, 'recent_mother_height') if hasattr(mother, 'recent_mother_height') else None
            self.previous_bmi           = getattr(mother, 'recent_bmi') if hasattr(mother, 'recent_bmi') else None
            self.previous_muac          = getattr(mother, 'recent_muac') if hasattr(mother, 'recent_muac') else None
            self.previous_lmp           = getattr(mother, 'recent_lmp') if hasattr(mother, 'recent_lmp') else None
                  
            if mother:
                indexcol = mother.indexcol
                self.created_at = mother.created_at
                self.recent_mother_weight   = getattr(self, 'mother_weight') if hasattr(self, 'mother_weight') else mother.recent_mother_weight
                self.recent_mother_height   = getattr(self, 'mother_height') if hasattr(self, 'mother_height') else mother.recent_mother_height
                self.recent_bmi             = getattr(self, 'bmi') if hasattr(self, 'bmi') else mother.recent_bmi
                self.recent_muac            = getattr(self, 'muac') if hasattr(self, 'muac') else mother.recent_muac
                self.recent_lmp             = getattr(self, 'lmp') if hasattr(self, 'lmp') else mother.recent_lmp

            self.FIELDS.update( {
                                  'indexcol' : indexcol,
                                  'created_at' : self.created_at,
                                  'updated_at' : self.updated_at,
                                  'telephone' : telephone,
                                  'national_id' : self.national_id,
                                  'user_phone' : self.user_phone,
                                  'user_pk' : self.user_pk,
                                  'nation_pk' : self.nation_pk,
                                  'province_pk' : self.province_pk,
                                  'district_pk' : self.district_pk,
                                  'referral_facility_pk' : self.referral_facility_pk,
                                  'facility_pk' : self.facility_pk,
                                  'sector_pk' : self.sector_pk,
                                  'cell_pk' : self.cell_pk,
                                  'village_pk' : self.village_pk,

                                 'previous_mother_weight': self.previous_mother_weight,
                                 'previous_mother_height': self.previous_mother_height,
                                 'recent_mother_weight': self.recent_mother_weight,
                                 'recent_mother_height': self.recent_mother_height,
                                 'previous_bmi': self.previous_bmi,
                                 'recent_bmi': self.recent_bmi,
                                 'previous_muac': self.previous_muac,
                                 'recent_muac': self.recent_muac,
                                 'is_valid': True,
                                 'recent_lmp': self.recent_lmp,
                                 'previous_lmp': self.previous_lmp 

                                
                                }
                        )

        except Exception, e:
            print "MOTHER FIELDS: %s" % e
            pass

        return self

    def store(self):
        try:
            mother  =   self.mother.get_or_create(self.orm, self.get_fields())
            return mother
        except:
            print "STORE MOTHER : %s" % e
            pass
        return None
 

