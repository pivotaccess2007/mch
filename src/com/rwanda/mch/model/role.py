# -*- coding: utf-8 -*-
#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from model.rsmsrwobj import RSMSRWObj
from util.record import fetch_role, fetch_roles, fetch_table_cols, fetch_table_cols_qry, migrate

class Role(RSMSRWObj):
    """An role of RapidSMS with a telephone number. Roles have the
    following properties:

    Attributes:
        code: A string representing the code used to request for the role.
        name: A name for the role.
    """

    _table = 'role'

    def __init__(self, code):
        """Return an role object """
        self.code = self.code
        self.table = Role._table

    @staticmethod
    def get_or_create( data):
        try:
            code = data.get('code')
            role  = Role.get_role(code)
            if not role:
                #print "SAVE DATA: ", data 
                migrate(Role._table, data)
                role = Role.get_role(code)
                if not role:    return ("Role has failed to be created, try again.", None)
                return ( 'Role created', role)
            return ( 'Role exists', role)
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def update_role(data):
        try:
            code = data.get('code')
            old_role = Role.get_role(code)
            ## Check role registered for the code
            if not old_role:
                 return ( 'Role does not exist with code %s' % (code) , None)
            else:
                data.update({"indexcol": old_role.indexcol})
                #print "UPDATE DATA: ", data 
                migrate(Role._table, data)
                role = Role.get_role(code)
                if role:                    
                    return ( 'Role Updated', role)
                else:
                    return ( 'Role with code %s cannot be updated, contact system administrator.' % (
                                                                        old_role.code) , None)
            
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def update_role_info(data):
        """ Not all info is update here except few supplied data info"""
        try:
            old_role = Role.get_role(data.get('code'))
            ## Check role registered for the code
            if not old_role:
                 return ( 'Role does not exist with code %s' % ( data.get('code')) , None)
            else:
                #print "UPDATE DATA: ", data 
                data.update({'indexcol': old_role.indexcol})
                migrate(Role._table, data)                    
                return ( 'Role updated', old_role)            
        except Exception, e:
            print e
            pass
        return ('Error', None)


    @staticmethod
    def get_role(code):
        return fetch_role(code)

    @staticmethod
    def get_roles():
        return fetch_roles()

    @staticmethod
    def get_roles_summary(cnds, cols):
        return fetch_table_cols(Role._table, cnds, cols)

    @staticmethod
    def fetch_roles_table(cnds, cols):
        return fetch_table_cols_qry(Role._table, cnds, cols)

    



