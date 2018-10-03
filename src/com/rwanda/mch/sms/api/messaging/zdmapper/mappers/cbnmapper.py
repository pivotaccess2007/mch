# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.nutrition import Nutrition
from sms.api.messaging.zdmapper.mappers.childmapper import Childmapper
import datetime

class Cbnmapper(object):
    """ Nutrition map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.cbn = Nutrition(report.nid, report.birth_date, report.child_number)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.child = Childmapper(report)

    def get_unique_query(self):
        try:
            child = self.child.get()
            self.child_pk = child.indexcol
            self.mother_pk = child.mother_pk
            self.pregnancy_pk = child.pregnancy_pk

            cbn_created_at = self.created_at - datetime.timedelta(days = 15)
            self.nutr_dict = {
                                    'breastfeeding' : self.code(self.breastfeeding)
                                    }

            self.UNIQUE_QUERY = self.filters_of_dict_keys(self.nutr_dict)
            self.UNIQUE_QUERY.update( {"created_at > %s" : cbn_created_at,                                            
                                            "child_weight = %s" : self.child_weight,
                                            "muac = %s" : self.muac,
                                            "child_pk = %s": self.child_pk })

        except Exception, e:
            print "UNIQUE CBN: %s" % e
            pass
        return self

    def get_fields(self):

        try:
            indexcol = None
            self.get_unique_query()
            cbn = self.cbn.get(self.UNIQUE_QUERY)
            if cbn:
                indexcol = cbn.indexcol
                self.created = cbn.created_at

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

                                 'breastfeeding' : self.code(self.breastfeeding),
                                 'child_weight': self.child_weight,
                                 'muac' : self.muac,
                                 
                                 'message' : self.message.text,
                                 'is_valid': True 

                                
                                }
                        )
            #print self.FIELDS
        except Exception, e:
            print "FIELDS CBN: %s" % e
            pass

        return self

    def store(self):
        try:    
            cbn  =   self.cbn.save(self.orm, self.get_fields())
            return cbn             
        except Exception, e:
            print "STORE CBN: %s" % e
            pass
        return None
