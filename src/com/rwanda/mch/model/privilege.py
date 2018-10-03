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
from util.record import fetch_privilege, fetch_privileges, fetch_assigned_privilege, fetch_table_cols, fetch_table_cols_qry, migrate

class Privilege(RSMSRWObj):
    """An privilege of RapidSMS. Privileges have the
    following properties:

    Attributes:
        code: A string representing the code used to request for the privilege.
        name: A name for the privilege.
    """

    _table = 'privilege'
    _usertable = 'user_privilege'

    def __init__(self, code):
        """Return an privilege object """
        self.code = self.code
        self.table = Privilege._table

    @staticmethod
    def get_or_create( data):
        try:
            code = data.get('code')
            privilege  = Privilege.get_privilege(code)
            if not privilege:
                #print "SAVE DATA: ", data 
                migrate(Privilege._table, data)
                privilege = Privilege.get_privilege(code)
                if not privilege:    return ("Privilege has failed to be created, try again.", None)
                return ( 'Privilege created', privilege)
            return ( 'Privilege exists', privilege)
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def get_or_assign( data):
        try:
            pk = data.get('privilege_pk')
            user_pk = data.get('user_pk')
            role_pk = data.get('role_pk')
            privilege  = Privilege.get_assigned_privilege(pk, user_pk, role_pk)
            if not privilege:
                #print "SAVE DATA: ", data 
                migrate(Privilege._usertable, data)
                privilege = Privilege.get_assigned_privilege(pk, user_pk, role_pk)
                if not privilege:    return ("Privilege has failed to be assigned, try again.", None)
                return ( 'Privilege assigned', privilege)
            return ( 'Privilege assignment exists', privilege)
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def update_privilege(data):
        try:
            code = data.get('code')
            old_privilege = Privilege.get_privilege(code)
            ## Check privilege registered for the code
            if not old_privilege:
                 return ( 'Privilege does not exist with code %s' % (code) , None)
            else:
                data.update({"indexcol": old_privilege.indexcol})
                #print "UPDATE DATA: ", data 
                migrate(Privilege._table, data)
                privilege = Privilege.get_privilege(code)
                if privilege:                    
                    return ( 'Privilege Updated', privilege)
                else:
                    return ( 'Privilege with code %s cannot be updated, contact system administrator.' % (
                                                                        old_privilege.code) , None)
            
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def update_privilege_info(data):
        """ Not all info is update here except few supplied data info"""
        try:
            old_privilege = Privilege.get_privilege(data.get('code'))
            ## Check privilege registered for the code
            if not old_privilege:
                 return ( 'Privilege does not exist with code %s' % ( data.get('code')) , None)
            else:
                #print "UPDATE DATA: ", data 
                data.update({'indexcol': old_privilege.indexcol})
                migrate(Privilege._table, data)                    
                return ( 'Privilege updated', old_privilege)            
        except Exception, e:
            print e
            pass
        return ('Error', None)


    @staticmethod
    def get_privilege(code):
        return fetch_privilege(code)

    @staticmethod
    def get_assigned_privilege(pk, user_pk, role_pk):
        return fetch_assigned_privilege(pk, user_pk, role_pk)

    @staticmethod
    def get_privileges():
        return fetch_privileges()

    @staticmethod
    def get_privileges_summary(cnds, cols):
        return fetch_table_cols(Privilege._table, cnds, cols)

    @staticmethod
    def fetch_privileges_table(cnds, cols):
        return fetch_table_cols_qry(Privilege._table, cnds, cols)

    



