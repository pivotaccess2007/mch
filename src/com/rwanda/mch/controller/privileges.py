#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from controller.main import RSMSRWController
from model.privilege import Privilege
from model.role import Role
from util.mch_util import average, makedict, makecol 


class PrivilegeController(RSMSRWController):
    
    def __init__(self, navb):
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Privilege.get_privileges_summary(cnds, cols)[0]
        self.navb.kw = {}
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cols    = ['COUNT(*) AS total']
        exts    = {}
        attrs   = []
        nat     = Privilege.get_privileges_summary(cnds, cols)
        roles   = Role.get_roles()
        privileges = Privilege.get_privileges()
        self.navb.kw = {}
        return [roles, privileges, nat, attrs]

    def get_tables(self):
        cnds    = self.navb.conditions()#;print cnds
        if self.navb.kw.get("search") and self.navb.kw.get("identity"):
            mkw     = self.navb.kw.get('identity').strip()
            if self.navb.kw.get("search") == 'code': cnds.update({"code = %s": mkw })        
        exts = {}
        attrs = []
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('indexcol', 'ID'),
                                              ('code',              'Code'),
                                              ('name', 'Name'),
                                              
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=privilege&id=%s">View</a>' % (x), })
            
        DESCRI = []
        INDICS = []
        group = "Privilege"
        title = "Privilege List"

        dcols = [x[0] for x in cols]
        nat = Privilege.fetch_privileges_table(cnds, dcols)
        desc  = 'Privileges%s' % (' (%s)' % (self.navb.find_descr(DESCRI + INDICS ,
                                                                        self.navb.kw.get('privilege')
                                                                    ) 
					                            )
                                    ) 
        #print INDICS, title, group, attrs, "NAT: ", nat[0].__dict__
        self.navb.kw = {}
        return (title, desc, group, attrs, markup, cols, nat)


    def register_privileges(self):
        cnds    = self.navb.conditions()
        message = ''
        privilege = None
        privileges = self.navb.kw.get("privileges")
        if type(privileges) in [str, unicode]: privileges = [privileges]
        assigned_privileges = [] 
        for p in privileges:
            if self.navb.kw.get("role") or self.navb.kw.get('pk'):
                formdata = {    
                                "privilege_pk": int(p), 
                                "user_pk": int(self.navb.kw.get('pk')) if self.navb.kw.get('pk') else None,
                                "role_pk": int(self.navb.kw.get('role')) if self.navb.kw.get('role') else None,
                            }

                #print "\nFORM: ", formdata, "\n"
                message, privilege = Privilege.get_or_assign(formdata)
                assigned_privileges.append(privilege)
        
        return [message, assigned_privileges]

