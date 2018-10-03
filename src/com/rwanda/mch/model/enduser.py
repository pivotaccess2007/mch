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
from util.mch_security import MchSecurity
from util.record import fetch_simcard, fetch_enduser, get_role, fetch_users, fetch_active_user, fetch_roles, fetch_users_summary, fetch_education_levels, fetch_genders, fetch_languages, fetch_location_levels, migrate, fetch_columns, fetch_user_by_nid_phone, fetch_table_users, fetch_table_cols
from sms.api.smser import Smser
from sms.api.mailer import Mailer


class Enduser(RSMSRWObj):
    """A enduser of RapidSMS with a user account. Endusers have the
    following properties:

    Attributes:
        surname: A string representing the enduser's surname.
        email: A username tracking the enduser's account.
    """

    _table = 'enduser'
    _levels =    {"NATION": ["Nation", "Igihugu"],
                 "PRV": ["Province", "Intara"],
                 "DST": ["District", "Akarere"],
                 "NRH": ["National Referral Hospital", "Ibitaro"],
                 "MH": ["Military Hospital", "Ibitaro"],
                 "HD": ["District Hospital", "Ibitaro"],
                 "HP": ["Hospital", "Ibitaro"],
                 "HC": ["Health Centre", "Ikigo nderabuzima"],
                 "CL": ["Clinic", "Ivuriro"],
                 "SEC": ["Sector", "Umurenge"],
                 "CEL": ["Cell", "Akagari"],
                 "VIL": ["Village", "Umudugudu"]}

    def __init__(self):
        """Return a Enduser object """
        self.telephone = self.user_phone
        self.national_id = self.national_id
        self.table = Enduser._table

    @staticmethod
    def send_message(telephone, message):
        try:
            cmd = Smser()
            message = message.replace("@", "¡")#; print message
            return cmd.send_message_via_kannel(telephone, message)
        except Exception, e:
            pass
        return False

    @staticmethod
    def send_email(subject, email, message):
        try:
            cmd = Mailer()
            return cmd.send_email( subject, email, message )
        except Exception, e:
            pass
        return False

    @staticmethod
    def get_or_create( data):
        try:
            simcard = Enduser.get_or_create_simcard(data.get('telephone'))
            if not simcard: return ( 'Bad Telephone',None)
            telephone = simcard.msisdn
            user = Enduser.get_active_user(telephone)
            if not user:
                if len(data.get('national_id')) != 16: return ( 'Bad National ID',None)
                if not data.get('email'):
                    data.update({"email": 'user%d@mch.moh.gov.rw' % simcard.indexcol})
                data.update({"simcard_pk": simcard.indexcol})
                data.update({"telephone": telephone})
                generated_password = MchSecurity.generatedPassword(simcard.msin)
                data.update({"salt" : generated_password[0]})
                data.update({"passwd" : generated_password[1]})
                national_id = data.get('national_id')
                #print "SAVE DATA: ", data 
                migrate(Enduser._table, data)
                #user = fetch_enduser(national_id, telephone)
                user = Enduser.get_active_user( telephone )
                sent = False
                if user.role_code == 'BINOME' or user.role_code == 'ASM' or user.language_code == 'RW':
                    sent = Enduser.send_message(telephone, 
                                                    "Twabamenyeshaga ko mumaze kwandikwa kuri list, muri sisitemu ya RapidSMS Rwanda, nka %(role)s, ku rwego rw %(level)s, %(nat)s, Intara %(prv)s, Akarere ka %(dst)s, ibitaro bya %(hp)s ikigo nderabuzima cya %(hc)s, umurenge wa %(sec)s, akagari ka %(cel)s, umudugudu wa %(vil)s. Murakoze."% {
                                    'role': user.role_name, 'hc': user.facility_name, 'sec': user.sector_name,
                                         'cel': user.cell_name , 'vil': user.village_name, 'level': Enduser._levels.get(user.location_level_code)[1],
                                          'dst': user.district_name, 'hp': user.referral_name, 'nat': user.nation_name, 'prv': user.province_name})
                else:
                    sent = Enduser.send_message(telephone, 
                    "You have been registered in RapidSMS as %(role)s, your username is: %(email)s, and password is: %(pwd)s. Thanks."
                                                % {'role': user.role_name, 'email': user.email, 'pwd': simcard.msin})
                    email = Enduser.send_email("RapidSMS Credentials", user.email, 
                        "You have been registered in RapidSMS as %(role)s, your username is: %(email)s, and password is: %(pwd)s. Thanks."
                                                % {'role': user.role_name, 'email': user.email, 'pwd': simcard.msin})
                if not sent:    return ("User Created, but SMS not sent, please contact username: %(email)s, and password: %(pwd)s"
                                    % {'email': user.email, 'pwd': simcard.msin}, user)
                return ( 'User created', user)
            return ( 'User exists', user)
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def update_user(data):
        try:
            simcard = Enduser.get_or_create_simcard(data.get('telephone'))
            if not simcard: return ( 'Bad Telephone',None) 
            telephone = simcard.msisdn
            user = Enduser.get_active_user(telephone)
            #if nid is invalid return
            if len(data.get('national_id')) != 16: return ( 'Bad National ID',None)
            national_id = data.get('national_id')
            old_user = fetch_enduser(national_id, telephone)
            ## Check national_id registered for the telephone
            if not old_user:
                 return ( 'User does not exist with NID %s and Telephone %s' % (national_id, telephone) , None)
            else:
                if (user and old_user) and old_user.indexcol != user.indexcol:
                    return ( 'User with NID %s and Telephone %s is active, please deactive him/her first.' % (
                                                                        user.national_id, user.telephone) , None)
                elif (old_user.indexcol == user.indexcol) or (old_user.indexcol == data.get('indexcol')):
                    # He is the same user, check if credentials have been updated 
                    new_passwd =  data.get('passwd')              
                    if old_user.email != data.get('email') or new_passwd:
                        if new_passwd:                            
                            generated_password = MchSecurity.generatedPassword(new_passwd)
                            data.update({"salt" : generated_password[0]})
                            data.update({"passwd" : generated_password[1]})
                        else:
                            new_passwd = simcard.msin
                            generated_password = MchSecurity.generatedPassword(new_passwd)
                            data.update({"salt" : generated_password[0]})
                            data.update({"passwd" : generated_password[1]})

                    data.update({"simcard_pk": simcard.indexcol})
                    data.update({"telephone": telephone})   
                    
                    #print "SAVE DATA: ", data 
                    migrate(Enduser._table, data)
                    user = Enduser.get_active_user( data.get('telephone') )
                    sent = False
                    if user.role_code == 'BINOME' or user.role_code == 'ASM' or user.language_code == 'RW':
                        sent = Enduser.send_message(telephone, 
                                                    "Twabamenyeshaga ko mumaze gukosorwa kuri list, muri sisitemu ya RapidSMS Rwanda, nka %(role)s, ku rwego rw %(level)s, %(nat)s, Intara %(prv)s, Akarere ka %(dst)s, ibitaro bya %(hp)s ikigo nderabuzima cya %(hc)s, umurenge wa %(sec)s, akagari ka %(cel)s, umudugudu wa %(vil)s. Murakoze."% {
                                    'role': user.role_name, 'hc': user.facility_name, 'sec': user.sector_name,
                                         'cel': user.cell_name , 'vil': user.village_name, 'level': Enduser._levels.get(user.location_level_code)[1],
                                          'dst': user.district_name, 'hp': user.referral_name, 'nat': user.nation_name, 'prv': user.province_name})
                    else:
                        sent = Enduser.send_message(telephone, 
                                "You have been updated in RapidSMS, your username is: %(email)s, and password is: %(pwd)s. Thanks."
                                                        % {'email': user.email, 'pwd': new_passwd})
                    if not sent:    return ("User updated, but SMS not sent, please contact username: %(email)s, and password: %(pwd)s"
                                        % {'email': user.email, 'pwd': data.get('passwd')}, old_user)
                    return ( 'User updated', old_user)

                else:
                    return ( 'User with NID %s and Telephone %s cannot be updated, contact system administrator.' % (
                                                                        old_user.national_id, old_user.telephone) , None)
            
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def update_user_info(data):
        """ Not all info is update here except few supplied data info"""
        try:
            old_user = fetch_enduser(data.get('national_id'), data.get('telephone'))
            ## Check national_id registered for the telephone
            if not old_user:
                 return ( 'User does not exist with NID %s and Telephone %s' % (data.get('national_id'), data.get('telephone')) , None)
            else:
                #print "UPDATE DATA: ", data
                data.update({'indexcol': old_user.indexcol}) 
                migrate(Enduser._table, data)                    
                return ( 'User updated', Enduser.get_users({'indexcol = %s ': old_user.indexcol})[0])            
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def get_or_create_simcard( phone):
        try:
            msin    = phone[len(phone)-7: ]
            if len(msin) != 7: return None
            mnc     = phone[len(phone)-9:len(phone)-7]
            mcc     = '250'
            spn     = ''
            if mnc == '78': spn     = 'MTN'
            if mnc == '73': spn     = 'AIRTEL'
            if mnc == '72': spn     = 'TIGO'      
            msisdn  = '+%(mcc)s%(mnc)s%(msin)s' % {'mcc': mcc, 'mnc': mnc, 'msin': msin}
            simcard = fetch_simcard(msisdn)
            indexcol = None
            if simcard: indexcol = simcard.indexcol
            #print  {'indexcol' : indexcol, 'phone': phone, 'mcc': mcc, 'mnc': mnc, 'msin': msin, 'msisdn': msisdn, 'spn': spn}
            if spn:
                if not simcard:
                    saved = migrate('simcard', {'indexcol' : indexcol, 'mcc': mcc, 'mnc': mnc, 'msin': msin, 'msisdn': msisdn, 'spn': spn})
                    if saved: simcard = fetch_simcard(msisdn)
            return simcard
        except Exception, e:
            print e
            pass

        return None

    @staticmethod
    def bulk_messaging(data):
        try:
            saved = migrate('bulk_sms', data)
            return saved
        except Exception, e:
            print e
            pass
        return None

    @staticmethod
    def get_active_user(telephone):
        """Return the only active user per telephone, since one sim per person."""
        user = None
        try:    user = fetch_active_user(telephone)
        except Exception, e:
            print e 
            pass
        return user

    @staticmethod
    def get_active_connection(active_user, backend):
        """Return the only active user per telephone, since one sim per person."""
        user = None
        try:    user = fetch_active_connection(active_user, backend)
        except Exception, e: pass
        return user

    @staticmethod
    def get_roles():
        """Return the only users roles."""
        roles = []
        try:    roles = fetch_roles()
        except Exception, e:
            print e
            pass
        return roles

    @staticmethod
    def get_role(pk):
        """Return the only users roles."""
        role = None
        try:    role = get_role(pk)
        except Exception, e:
            print e
            pass
        return role


    @staticmethod
    def get_role_name(pk):
        """Return the only users roles."""
        role = ""
        try:    role = get_role(pk).name
        except Exception, e:
            print e
            pass
        return role


    @staticmethod
    def get_genders():
        """Return the only users genders."""
        genders = []
        try:    genders = fetch_genders()
        except Exception, e:
            print e
            pass
        return genders

    @staticmethod
    def get_languages():
        """Return the only users languages."""
        languages = []
        try:    languages = fetch_languages()
        except Exception, e:
            print e
            pass
        return languages


    @staticmethod
    def get_education_levels():
        """Return the only users education_levels."""
        education_levels = []
        try:    education_levels = fetch_education_levels()
        except Exception, e:
            print e
            pass
        return education_levels

    @staticmethod
    def get_location_levels():
        """Return the only users education_levels."""
        location_levels = []
        try:    location_levels = fetch_location_levels()
        except Exception, e:
            print e
            pass
        return location_levels

    @staticmethod
    def get_users(cnds):
        return fetch_users(cnds)

    @staticmethod
    def get_users_summary(cnds, cols, exts):
        return fetch_users_summary(Enduser._table, cnds, cols, exts)


    @staticmethod
    def fetch_user_table(cnds, cols):
        return fetch_table_users(Enduser._table, cnds, cols)

    @staticmethod
    def get_users_cols(cnds, cols):
        return fetch_table_cols(Enduser._table, cnds, cols)

    @staticmethod
    def get_users_performance(cnds):
        records = []
        return records

    



