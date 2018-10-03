#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


class RSMSRWObj(object):
    """A Rapidsms Rwanda Main Object of RapidSMS. RSMSRWObj has the
    following properties:

    Attributes: TODO
        
    """

    def __init__(self, user_phone = None, national_id = None):
        """Return a Pregnancy object which lmp is *lmp* """
        self.user_phone = user_phone
        self.national_id = national_id

    def set_location(self):
        return


    def union_records(self, cols, tables):
        try:
            qrs = []
            for tbl in tables:
                qrs.append( 'SELECT %(cols)s FROM %(tbl)s' % {'cols': ', '.join(cols), 'tbl': tbl} )
        except Exception, e:
            print e
            pass
        return None  

