#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


from model.birth import Birth
from util.record import fetch_gender
from sms.api.messaging.zdmapper.mappers.mothermapper import Mothermapper

class Childmapper(object):
    """ Childmapper map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.deliv = Birth(report.nid, report.birth_date, report.child_number)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.mother = Mothermapper(report)

    def get(self):
        try:
            return self.deliv.get()
        except Exception, e:
            print "CHILD NOT FOUND: %s" % e
            pass
        return None

    def get_sex(self):
        try:
            gender = 'bo' if self.code(self.gender).lower() == 'bo' else 'gi'
            sex_code = 'M' if gender == 'bo' else 'F'
            sex = fetch_gender(sex_code)
            return sex
        except Exception, e:
            #print e
            pass
        return None

    def get_fields(self):

        try:
            
            mother = self.mother.store()
            mother_pk = mother.indexcol 

            child = self.deliv.get()
            gender= self.get_sex()
            indexcol = None
            self.recent_breastfeeding   = getattr(self, 'breastfeeding') if hasattr(self, 'breastfeeding') else None
            self.recent_child_weight   = getattr(self, 'child_weight') if hasattr(self, 'child_weight') else None
            self.recent_child_height   = getattr(self, 'child_height') if hasattr(self, 'child_height') else None
            self.recent_bmi             = getattr(self, 'bmi') if hasattr(self, 'bmi') else None
            self.recent_muac            = getattr(self, 'muac') if hasattr(self, 'muac') else None
            self.previous_child_weight = getattr(child, 'recent_child_weight') if hasattr(child, 'recent_child_weight') else None
            self.previous_child_height = getattr(child, 'recent_child_height') if hasattr(child, 'recent_child_height') else None
            self.previous_bmi           = getattr(child, 'recent_bmi') if hasattr(child, 'recent_bmi') else None
            self.previous_muac          = getattr(child, 'recent_muac') if hasattr(child, 'recent_muac') else None
            self.weight_for_age         = getattr(child, 'weight_for_age') if hasattr(child, 'weight_for_age') else None
            self.height_for_age         = getattr(child, 'height_for_age') if hasattr(child, 'height_for_age') else None
            self.weight_for_height      = getattr(child, 'weight_for_height') if hasattr(child, 'weight_for_height') else None
            self.sex                    = getattr(child, 'sex') if hasattr(child, 'sex') else None
            self.sex_pk                 = getattr(child, 'sex_pk') if hasattr(child, 'sex_pk') else None
            
            if gender:
                self.sex                    = gender.code
                self.sex_pk                 = gender.indexcol
                  
            if child:
                indexcol = child.indexcol
                self.created_at = child.created_at
                self.recent_breastfeeding   = getattr(self, 'breastfeeding') if hasattr(self, 'breastfeeding') else child.breastfeeding
                self.recent_child_weight   = getattr(self, 'child_weight') if hasattr(self, 'child_weight') else child.recent_child_weight
                self.recent_child_height   = getattr(self, 'child_height') if hasattr(self, 'child_height') else child.recent_child_height
                self.recent_bmi             = getattr(self, 'bmi') if hasattr(self, 'bmi') else child.recent_bmi
                self.recent_muac            = getattr(self, 'muac') if hasattr(self, 'muac') else child.recent_muac
                self.weight_for_age    = getattr(self, 'weight_for_age') if hasattr(self, 'weight_for_age') else child.weight_for_age
                self.height_for_age    = getattr(self, 'height_for_age') if hasattr(self, 'height_for_age') else child.height_for_age
                self.weight_for_height = getattr(self, 'weight_for_height') if hasattr(self, 'weight_for_height') else child.weight_for_height
                self.pregnancy_pk   = child.pregnancy_pk
            self.FIELDS.update( {
                                  'indexcol' : indexcol,
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
                                  'sex': self.sex,
                                  'sex_pk': self.sex_pk,

                                 'previous_child_weight': self.previous_child_weight,
                                 'previous_child_height': self.previous_child_height,
                                 'recent_child_weight': self.recent_child_weight,
                                 'recent_child_height': self.recent_child_height,
                                 'previous_bmi': self.previous_bmi,
                                 'recent_bmi': self.recent_bmi,
                                 'previous_muac': self.previous_muac,
                                 'recent_muac': self.recent_muac,
                                 'is_valid': True,
                                 'weight_for_age': self.weight_for_age,
                                 'height_for_age': self.height_for_age,
                                 'weight_for_height': self.weight_for_height 

                                
                                }
                        )
            #print self.FIELDS

        except Exception, e:
            print "FIELDS CHILD: %s" % e
            pass

        return self

    def store(self):
        try:
            
            child  =   self.deliv.get_or_create(self.orm, self.get_fields())
            return child
        except:
            print "STORE CHILD: %s" % e
            pass
        return None
 

