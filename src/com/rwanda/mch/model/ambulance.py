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
from model.enduser import Enduser
from util.record import fetch_simcard, fetch_ambulance, fetch_table, fetch_summary, migrate
from sms.api.smser import Smser


class Ambulance(RSMSRWObj):
    """An ambulance of RapidSMS with a telephone number. Ambulances have the
    following properties:

    Attributes:
        telephone: A string representing the telephone used to request for the ambulance.
        facility: A facility tracking the ambulance.
    """

    _table = 'ambulance'

    def __init__(self, telephone):
        """Return an ambulance object """
        self.telephone = self.telephone
        self.table = Ambulance._table

    @staticmethod
    def get_or_create( data):
        try:
            simcard = Enduser.get_or_create_simcard(data.get('telephone'))
            if not simcard: return ( 'Bad Telephone', None)
            telephone = simcard.msisdn
            amb = Ambulance.get_ambulance(telephone)
            if not amb:
                data.update({"simcard_pk": simcard.indexcol})
                data.update({"telephone": telephone})
                #print "SAVE DATA: ", data 
                migrate(Ambulance._table, data)
                amb = Ambulance.get_ambulance(telephone)
                sent = False
                sent = Enduser.send_message(telephone, 
                    "Twabamenyeshaga ko mumaze kwandikwa muri sisitemu ya RapidSMS Rwanda, nk'ukurikirana imbagukira gutabara, ikigo nderabuzima cya %(hc)s, ibitaro bya %(hd)s. Murakoze."
                                                % { 'hc': amb.facility_name, 'hd': amb.referral_facility_name })
                sent = Enduser.send_message(telephone, 
                    "You have been registered in RapidSMS as ambulance coordinator, in %(hc)s health centre, %(hd)s district hospital. Thanks."
                                                % { 'hc': amb.facility_name, 'hd': amb.referral_facility_name })
                   
                if not sent:    return ("Ambulance Created, but SMS not sent, please contact telephone: %(phone)s."
                                    % {'phone': amb.telephone}, amb)
                return ( 'Ambulance created', amb)
            return ( 'Ambulance exists', amb)
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def update_user(data):
        try:
            simcard = Enduser.get_or_create_simcard(data.get('telephone'))
            if not simcard: return ( 'Bad Telephone', None)
            telephone = simcard.msisdn
            old_amb = Ambulance.get_ambulance(telephone)
            ## Check ambulance registered for the telephone
            if not old_amb:
                 return ( 'Ambulance does not exist with Telephone %s' % (telephone) , None)
            else:
                data.update({"indexcol": old_amb.indexcol})
                data.update({"simcard_pk": simcard.indexcol})
                data.update({"telephone": telephone})   
                #print "UPDATE DATA: ", data 
                migrate(Ambulance._table, data)
                amb = Ambulance.get_ambulance(telephone)
                if amb:                    
                    sent = Enduser.send_message(telephone, 
                        "Twabamenyeshaga ko mumaze gukosorwa imyirondoro muri sisitemu ya RapidSMS Rwanda, nk'ukurikirana imbagukira gutabara, ikigo nderabuzima cya %(hc)s, ibitaro bya %(hd)s. Murakoze."
                                                    % { 'hc': amb.facility_name, 'hd': amb.referral_facility_name })
                    sent = Enduser.send_message(telephone, 
                        "You have been updated in RapidSMS as ambulance coordinator, in %(hc)s health centre, %(hd)s district hospital. Thanks."
                                                    % { 'hc': amb.facility_name, 'hd': amb.referral_facility_name })
                       
                    if not sent:    return ("Ambulance Updated, but SMS not sent, please contact telephone: %(phone)s."
                                        % {'phone': amb.telephone}, amb)
                    return ( 'Ambulance Updated', amb)

                else:
                    return ( 'Ambulance with telephone %s cannot be updated, contact system administrator.' % (
                                                                        old_amb.telephone) , None)
            
        except Exception, e:
            print e
            pass
        return ('Error', None)

    @staticmethod
    def update_ambulance_info(data):
        """ Not all info is update here except few supplied data info"""
        try:
            old_amb = Ambulance.get_ambulance(data.get('telephone'))
            ## Check ambulance registered for the telephone
            if not old_amb:
                 return ( 'Ambulance does not exist withtelephone %s' % ( data.get('telephone')) , None)
            else:
                #print "UPDATE DATA: ", data 
                data.update({'indexcol': old_amb.indexcol})
                migrate(Ambulance._table, data)                    
                return ( 'Ambulance updated', old_amb)            
        except Exception, e:
            print e
            pass
        return ('Error', None)


    @staticmethod
    def get_ambulance(telephone):
        return fetch_ambulance(telephone)

    @staticmethod
    def get_ambulances_summary(cnds, cols, exts):
        return fetch_summary(Ambulance._table, cnds, cols, exts)

    @staticmethod
    def fetch_ambulances_table(cnds, cols):
        return fetch_table(Ambulance._table, cnds, cols)

    



