# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.refusal import Refusal
from sms.api.messaging.zdmapper.mappers.mothermapper import Mothermapper

class Refmapper(object):
    """ Refmapper map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.ref = Refusal(report.nid, report.created_at)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.mother = Mothermapper(report)


    def get_unique_query(self):
        try:
            
            self.UNIQUE_QUERY =  {"created_at >= %s" : self.rectifier.nine_months_ago(),                                            
                                            "national_id = %s" : self.nid }
        except Exception, e:
            print "UNIQUE REF: %s" % e
            pass
        return self

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

                                  'message' : self.message.text,
                                  'is_valid' : True
                                }
                        )

        except Exception, e:
            print e
            pass

        return self

    def store(self):
        try:    
            ref  =   self.ref.save(self.orm, self.get_fields())
            return ref             
        except Exception, e:
            print e
            pass
        return None
