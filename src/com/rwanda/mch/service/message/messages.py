#!/usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

##
## The only file to use orm directly
## 

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"


NOTIFICATION = {
                    "SMN": {
                           "en": "You have received a notification for severe malaria case, for patient(%(nid)s) from telephone %(phone)s, a CHW in %(location)s.",
                           "rw": "Mwohererejwe raporo ku kimenyetso cyangwa ibimenyetso mpuruza bya malariya y'igikatu, ku murwayi(%(nid)s) ivuye kuri telefoni %(phone)s, umujyanama wo mu %(location)s.", "fr": ""},

                    "DTH": {"en": "You have received a death notification for  patient(%(nid)s) from telephone %(phone)s, a CHW in %(location)s.",
                    "rw": "Mwohererejwe raporo mpuruza ku byago by'urupfu, ku murwayi(%(nid)s) ivuye kuri telefoni %(phone)s, umujyanama wo mu %(location)s.", "fr": ""},

                  "RSO": {
                           "en": "You have received a notification for risk of stock out, for drugs(%(drugs)s) from telephone %(phone)s, a CHW in %(location)s.",
                           "rw": "Mwohererejwe raporo ku kibazo cy'imiti yenda kurangira, iyo miti ni (%(drugs)s) ivuye kuri telefoni %(phone)s, umujyanama wo mu %(location)s.", "fr": ""},

                  "SO": {
                           "en": "You have received a notification for stock out, for drugs(%(drugs)s) from telephone %(phone)s, a CHW in %(location)s.",
                           "rw": "Mwohererejwe raporo ku kibazo cy'imiti yarangiye, iyo miti ni (%(drugs)s) ivuye kuri telefoni %(phone)s, umujyanama wo mu %(location)s.", "fr": ""},
                  "SS": {
                           "en": "You have received a notification for stock supplied, for drugs(%(drugs)s) from telephone %(phone)s, a CHW in %(location)s.",
                           "rw": "Mwohererejwe raporo ku miti yakiriwe, iyo miti ni (%(drugs)s), ivuye kuri telefoni %(phone)s, umujyanama wo mu %(location)s.", "fr": ""},

                  "WHO": {
                           "en": "You are registered in RapidSMS Rwanda, as %(role)s with telephone %(phone)s, in %(dst)s district, %(hd)s hospital, %(hc)s health centre, %(sec)s sector, %(cel)s cell, %(vil)s village. Thank you for using RapidSMS Rwanda!",
                           "rw": "Mwanditse neza muri sisitemu ya RapidSMS Rwanda, nka %(role)s ukoresha telefoni nimero %(phone)s, mu karere ka %(dst)s, ibitaro bya %(hd)s, ikigo nderabuzima cya %(hc)s, umurenge wa %(sec)s, akagari ka %(cel)s, mu mudugudu wa %(vil)s. Murakoze gukoresha RapidSMS Rwanda!", "fr": "La version française est indisponible."},


                    "RED": {
                            "rw": "Umujyanama %(chw)s atumenyeshejeko umubyeyi %(patient)s utuye mu karere ka %(district)s, umurenge wa %(sector)s, akagari ka %(cell)s, umudugudu wa %(village)s afite ikibazo cyo: (%(symptom)s). Gerageza urebe uko mwamufasha.",
                            "en": "The community health worker %(chw)s comes to report that the patient %(patient)s in the district %(district)s, sector %(sector)s, cell %(cell)s, village %(village)s has this problem: (%(symptom)s). Please follow up and help.",
                            "fr": "Un agent de sante communautaire %(chw)s vient de rapporter que le patient %(patient)s qui habite dans le district %(district)s, secteur %(sector)s, cellule %(cell)s, village %(village)s a un probleme: (%(symptom)s). Veuillez l'aider s'il vous plait."
                              
                            }

                    }

REMINDER = {
                    "SMN": {
                           "en": "Reminder for severe malaria case notification, for patient(%(nid)s) from telephone %(phone)s, a CHW in %(location)s. Please follow up, thanks!",
                           "rw": " Twabibutsaga raporo mpuruza ya malariya y'igikatu mwohererejwe, ku murwayi(%(nid)s) ivuye kuri telefoni %(phone)s, umujyanama wo mu %(location)s. Mugerageze mubikurikirane, murakoze!", "fr": ""},

                    "DTH": {"en": "Reminder for death notification, for  patient(%(nid)s) from telephone %(phone)s, a CHW in %(location)s. Please follow up, thanks!",
                    "rw": "Twabibutsaga raporo mpuruza ku byago by'urupfu mwohererejwe, ku murwayi(%(nid)s) ivuye kuri telefoni %(phone)s, umujyanama wo mu %(location)s. Mugerageze mubikurikirane, murakoze!", "fr": ""},

                    }

