# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from model.departure import Departure
from sms.api.messaging.zdmapper.mappers.mothermapper import Mothermapper

class Depmapper(object):
    """ Depmapper map the sms report appropriately to db columns structure """

    def __init__(self, report):
        self.dep = Departure(report.nid, pregnancy_pk = report.pregnancy_pk, birth_date = None, child_number = None)
        self.__dict__.update(report.__dict__)
        self.FIELDS = {}
        self.mother = Mothermapper(report)

    def get_unique_query(self):
        try:
            child_pk = getattr(self, 'child_pk') if hasattr(self, 'child_pk') else None
            pregnancy_pk = getattr(self, 'pregnancy_pk') if hasattr(self, 'pregnancy_pk') else None
            self.UNIQUE_QUERY =  {"created_at >= %s" : self.rectifier.nine_months_ago(),                                            
                                            "national_id = %s" : self.nid }
            self.UNIQUE_QUERY.update( {"pregnancy_pk %s" % ("= %s" % pregnancy_pk if pregnancy_pk else "IS NULL"): '',
                                            "child_pk %s" % (" = %s" % child_pk if child_pk else "IS NULL") : '' })
        except Exception, e:
            print "UNIQUE DEP: %s" % e
            pass
        return self

    def get_fields(self):

        try:
            mother = self.mother.store()
            mother_pk = mother.indexcol
            birth_date = getattr(self, 'birth_date') if hasattr(self, 'birth_date') else None
            child_number = getattr(self, 'child_number') if hasattr(self, 'child_number') else None
            child_pk = getattr(self, 'child_pk') if hasattr(self, 'child_pk') else None
      
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
                                  'child_pk' : child_pk,

                                  'message' : self.message.text,
                                  'is_valid' : True
                                }
                        )

        except Exception, e:
            print "FIELDS DEP: %s " % e
            pass

        return self

    def store(self):
        try:    
            dep  =   self.dep.save(self.orm, self.get_fields())
            return dep             
        except Exception, e:
            print "STORE: %s" % e
            pass
        return None
