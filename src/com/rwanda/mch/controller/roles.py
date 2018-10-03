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
from model.role import Role
from util.mch_util import average, makedict, makecol 


class RoleController(RSMSRWController):
    
    def __init__(self, navb):
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Role.get_roles_summary(cnds, cols)[0]
        self.navb.kw = {}
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cols    = ['COUNT(*) AS total']
        exts    = {}
        attrs   = []
        nat     = Role.get_roles_summary(cnds, cols)
        self.navb.kw = {}
        return [nat, attrs]

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

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=role&id=%s">View</a>' % (x), })
            
        DESCRI = []
        INDICS = []
        group = "Role"
        title = "Role List"

        dcols = [x[0] for x in cols]
        nat = Role.fetch_roles_table(cnds, dcols)
        desc  = 'Roles%s' % (' (%s)' % (self.navb.find_descr(DESCRI + INDICS ,
                                                                        self.navb.kw.get('role')
                                                                    ) 
					                            )
                                    ) 
        #print INDICS, title, group, attrs, "NAT: ", nat[0].__dict__
        self.navb.kw = {}
        return (title, desc, group, attrs, markup, cols, nat)


    def register_role(self):
        cnds    = self.navb.conditions()
        message = ''
        role = None
        if self.navb.kw.get("rolename") and self.navb.kw.get('rolecode'):
            formdata = {    
                            "code": self.navb.kw.get('rolecode'), 
                            "name": self.navb.kw.get('rolename')
                        }

            #print "\nFORM: ", formdata, "\n"
            message, role = Role.get_or_create(formdata)
            self.navb.kw = {}
        
        return [message, role]

