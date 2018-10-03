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
from model.enduser import Enduser

from util.mch_util import average, makedict, makecol, process_import_file, datetime, upload_users_indb, export_data_to_xlsx
from util.mch_security import MchSecurity

from xlrd import open_workbook

class EnduserController(RSMSRWController):
    
    def __init__(self, navb):
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Enduser.get_users_summary(cnds, cols, exts)[0]
        return total

    def get_users(self):
        cnds    = self.navb.conditions()
        if self.navb.kw.get('q'):
            mkw     = "%%%s%%" % self.navb.kw.get('q')
            cnds    = {"telephone LIKE %s OR national_id LIKE %s": (mkw, mkw)}
            print cnds
            return Enduser.get_users(cnds)        
        return []


    @staticmethod
    def reset_password(email):
        try:        
            user, otp, token = MchSecurity.get_otp(email)
            #print "OTP: ",  otp
            sent = Enduser.send_message(user.telephone, "Your OTP to change password , now, is: %s" % otp)
            return (token, sent)
        except Exception, e:
            print e
        return (None, False)

    @staticmethod
    def change_password(email, tkn, otp, new_passwd):
        message = None
        if tkn and otp:
            try:
                seen = MchSecurity.verify_otp(tkn, otp)#;print "SEEN: ", seen
                if seen:
                    #print "SEEN: ", otp, new_passwd
                    user = MchSecurity.get_user_by_email(email)
                    formdata = {
                            "indexcol": user.indexcol,     
                            "telephone": user.telephone, 
                            "national_id":  user.national_id,
                            "email":      email,
                            "passwd":      new_passwd
                        }

                    #print "\nFORM: ", formdata, "\n"
                    message, user = Enduser.update_user(formdata)                    
                return (message, True)
            except Exception, e:
                print e
                message = e
            
        return (message, False)

    def get_stats(self):
        cnds    = self.navb.conditions()
        #print "CNDS: ", cnds
        attrs   = [ (x.indexcol, x.code.lower(), x.name) for x in Enduser.get_roles() ]
        cols    = ['COUNT(*) AS total']
        exts    = {}
        for attr in attrs:  exts.update({attr[1].lower() : ('COUNT(*)', 'role_pk = %d' % attr[0]) })
        nat     = Enduser.get_users_summary(cnds, cols, exts)
        avg     = average 
        return [attrs, avg, nat]

    def get_tables(self):
        cnds    = self.navb.conditions()#;print cnds
        if self.navb.kw.get("search") and self.navb.kw.get("identity"):
            mkw     = "%%%s%%" % self.navb.kw.get('identity').strip()
            if self.navb.kw.get("search") == 'nid': cnds.update({"national_id LIKE %s": mkw })
            if self.navb.kw.get("search") == 'sim': cnds.update({"telephone LIKE %s": mkw })        
        exts = {}
        attrs   = [ (x.indexcol, x.code.lower(), x.name) for x in Enduser.get_roles() ]
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('indexcol', 'ID'),
                                              ('national_id', 'National ID'),
                                              ('telephone',              'Telephone'),
                                              ('surname', 'Surname'),
                                              ('given_name',              'Given Name'),
                                              ('role_pk', 'Role'),
                                              ('email',              'Email'),                                              
                                              ('is_active',              'Is Active'),
                                              #('last_seen', 'Last Seen'),
                                              ('province_pk', 'Province'),
                                              ('district_pk', 'District'),
                                              ('referral_facility_pk', 'Hospital'),
                                              ('facility_pk', 'Health Centre'),
                                              ('sector_pk', 'Sector'),
                                              ('cell_pk', 'Cell'),
                                              ('village_pk', 'Village'),
                                              
                                            ])

        markup.update({'action': lambda x, _, __: '<a href="/dashboards/updateuser?id=%s">Edit %s</a>' % (x, x), })
        markup.update({'role_pk': lambda x, _, __: '%s' % (Enduser.get_role_name(x)) })
        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=chw&id=%s">View</a>&nbsp;&#124;&nbsp;\
                                                     <a href="/dashboards/activate?action=activate&id=%s">Activate</a>&nbsp;&#124;&nbsp;\
                                                     <a href="/dashboards/activate?action=deactivate&id=%s">Deactivate</a>' % (x,x,x), })
            
        sc      = self.navb.kw.get('subcat')
        #print cnds, markup, cols, sc, attrs

        DESCRI = []
        USERDICT = {y[1]: (y[0], y[2]) for y in attrs}
        INDICS = []
        group = "User"
        title = "User List"

        if self.navb.kw.get('subcat') and self.navb.kw.get('subcat') in [makecol(x[1]) for x in attrs]:
            cnds.update({ 'role_pk = %s': USERDICT[self.navb.kw.get('subcat')][0] })
            INDICS = [(self.navb.kw.get('subcat'), USERDICT[self.navb.kw.get('subcat')][1])]
            group  = USERDICT[self.navb.kw.get('subcat')][1]

        dcols = [x[0] for x in cols]
        #print cnds
        nat = Enduser.fetch_user_table(cnds, dcols)
        #DESCRI.append((group, title))
        desc  = 'Users%s' % (' (%s)' % (self.navb.find_descr(DESCRI + INDICS,
                                                                        sc or self.navb.kw.get('subcat')
                                                                    ) 
					                            )
                                    ) 
        #print INDICS, title, group, attrs, "NAT: ", nat[0].__dict__
        return (title, desc, group, attrs, markup, cols, nat)


    def register_user(self):
        cnds    = self.navb.conditions()
        message = ''
        user = None
        if self.navb.kw.get("nid") and self.navb.kw.get('telephone_moh'):
            nid = nid = self.navb.kw.get('nid')
            phone = self.navb.kw.get('telephone_moh')
            formdata = {    
                            "telephone": phone, 
                            "national_id":  nid,
                            "email":      self.navb.kw.get('email'),
                            "surname":      self.navb.kw.get('surname'),
                            "given_name":   self.navb.kw.get('given_name'),
                            "sex_pk":   self.navb.kw.get('sex'),
                            "role_pk":  self.navb.kw.get('role'),
                            "education_level_pk":    self.navb.kw.get('edu_level'),
                            "date_of_birth" :  self.navb.make_time(self.navb.kw.get('dob')), 
                            "join_date": self.navb.make_time(self.navb.kw.get('djoin')),
                            "language_pk": self.navb.kw.get('language'),
                            "nation_pk": self.navb.kw.get('user_nation'),
                            "province_pk": self.navb.kw.get('user_province'),
                            "district_pk": self.navb.kw.get('user_district'),
                            "referral_facility_pk": self.navb.kw.get('user_hospital'),
                            "facility_pk" : self.navb.kw.get('user_facility'),
                            "location_level_pk": self.navb.kw.get('user_area_level'),                            
                            "sector_pk": self.navb.kw.get('user_sector'),
                            "cell_pk": self.navb.kw.get('user_cell'),
                            "village_pk": self.navb.kw.get('user_village'),
                            "is_active": True,
                            "is_correct": True

                        }

            #print "\nFORM: ", formdata, "\n"
            message, user = Enduser.get_or_create(formdata)
            self.navb.kw = {}
        
        genders = Enduser.get_genders()
        roles   = Enduser.get_roles()
        langs   = Enduser.get_languages()
        education_levels = Enduser.get_education_levels()
        area_levels = Enduser.get_location_levels()        
        return [genders, roles, education_levels, area_levels, langs, message, user]


    def update_user(self):
        cnds    = self.navb.conditions()
        message = ''
        user = None
        #print "IDS: ",self.navb.kw, self.navb.kw.get('id') , self.navb.kw.get('pk')
        if self.navb.kw.get('id') or self.navb.kw.get('pk'):
            mkw     = "%s" % self.navb.kw.get('id') or self.navb.kw.get('pk')
            cnds    = {"indexcol = %s": mkw}
            user    =  Enduser.get_users(cnds)[0]
 
        if self.navb.kw.get("pk") and self.navb.kw.get('nid') and self.navb.kw.get('telephone_moh'):
            cnds    = {"indexcol = %s": self.navb.kw.get("pk")}
            indexcol = self.navb.kw.get('pk')
            nid = self.navb.kw.get('nid')
            phone = self.navb.kw.get('telephone_moh')
            formdata  = {    
                            "indexcol": indexcol,
                            "telephone": phone, 
                            "national_id":  nid,
                            "email":      self.navb.kw.get('email'),
                            "surname":      self.navb.kw.get('surname'),
                            "given_name":   self.navb.kw.get('given_name'),
                            "sex_pk":   self.navb.kw.get('sex'),
                            "role_pk":  self.navb.kw.get('role'),
                            "education_level_pk":    self.navb.kw.get('edu_level'),
                            "date_of_birth" :  self.navb.make_time(self.navb.kw.get('dob')), 
                            "join_date": self.navb.make_time(self.navb.kw.get('djoin')),
                            "language_pk": self.navb.kw.get('language'),
                            "nation_pk": self.navb.kw.get('user_nation'),
                            "province_pk": self.navb.kw.get('user_province'),
                            "district_pk": self.navb.kw.get('user_district'),
                            "referral_facility_pk": self.navb.kw.get('user_hospital'),
                            "facility_pk" : self.navb.kw.get('user_facility'),
                            "location_level_pk": self.navb.kw.get('user_area_level'),                            
                            "sector_pk": self.navb.kw.get('user_sector'),
                            "cell_pk": self.navb.kw.get('user_cell'),
                            "village_pk": self.navb.kw.get('user_village'),
                            "is_active": True,
                            "is_correct": True

                        }

            #print "\nFORM: ", formdata, "\n"
            message, user = Enduser.update_user(formdata)
            if user: user    =  Enduser.get_users(cnds)[0]
            self.navb.kw = {"id": self.navb.kw.get("pk")}
        
        sectors = self.navb.auth.auth_filter_locations("sec", user.district_pk)
        cells = self.navb.auth.auth_filter_locations("cel", user.sector_pk)
        villages = self.navb.auth.auth_filter_locations("vil", user.cell_pk)
        genders = Enduser.get_genders()
        roles   = Enduser.get_roles()
        langs   = Enduser.get_languages()
        education_levels = Enduser.get_education_levels()
        area_levels = Enduser.get_location_levels() 
        #print user.__dict__       
        return [sectors, cells, villages, genders, roles, education_levels, area_levels, langs, message, user]





    def group_messaging(self):
        cnds    = self.navb.conditions()
        message = ''
        if self.navb.kw.get("send") and self.navb.kw.get('text'):
            text = self.navb.kw.get('text')
            group = self.navb.kw.get('group')
            cnds.update({'is_active': ''})
            if group and group != 'all':   cnds.update({'role_pk = %s': group}) 
            users   = Enduser.get_users_cols(cnds, cols = ['telephone'])
            unsents = []
            bulk_sms_data = {
                        "message": text ,
                        "to_group": group,
                        "user_phone": self.navb.user.telephone,
                        "user_pk": self.navb.user.indexcol,
                        "nation_pk":  self.navb.user.nation_pk,
                        "province_pk":  self.navb.kw.get('province'),
                        "district_pk": self.navb.kw.get('district'),
                        "referral_facility_pk": self.navb.kw.get('hd'),
                        "facility_pk": self.navb.kw.get('hc'),
                        "sector_pk": self.navb.kw.get('sector'),
                        "cell_pk": self.navb.kw.get('cell'),
                        "village_pk": self.navb.kw.get('village')
                    }
            saved = Enduser.bulk_messaging(bulk_sms_data)

            for user in users:
                try:
                    #print user.telephone, text
                    sent = Enduser.send_message(user.telephone, text)
                except Exception, e:
                    unsents.append(user.telephone)
                    continue
            
            if len(unsents) > 0:
                message = ','.join(u for u in unsents)
                message = 'The message has not been delivered to: %s' % message
            else:
                message = 'The message you sent has been delivered successfully. Thanks.'
            
            #print "\nRESPONSE: ", message, "\n", cnds, "\n"
            self.navb.kw = {}
        
        roles   = Enduser.get_roles()
        return [roles, message]

    def upload_users(self):
        cnds    = self.navb.conditions()
        message = ''
        errors  = []           
        if self.navb.kw.get("users_list"):
            file_of_users = self.navb.kw.get('users_list')
            try:
                #print "File: ", file_of_users.file, file_of_users.file.name
                ourfile = process_import_file(file_of_users, self.navb.user.indexcol, datetime.datetime.now())
                #print "OUR FILE ON DISK: " , ourfile 
                errs = upload_users_indb(ourfile[1])
                errors = errs
            except Exception, e:
                print "Error: ", e
                errors.append({'row': 'All', 'who': 'All', 'errors': [('All', 'Invalid file template', e.message)] })
            
            if len(errors) > 0:
                message = 'The list has failed to upload, please correct your list and try again.'
            else:
                message = 'The list has been uploaded successfully. Thanks.'
            
            #print "\nRESPONSE: ", message, "\n", cnds, "\n"
            self.navb.kw = {}
        
        #print "ERRORS: ", errors
        return [errors, message]



    def register_ambulance(self):
        cnds    = self.navb.conditions()
        message = ''
        amb = None
        if self.navb.kw.get("amb_facility") and self.navb.kw.get('telephone_moh'):
            fac     = self.navb.kw.get('amb_facility')
            phone   = self.navb.kw.get('telephone_moh')
            formdata = {    
                            "telephone": phone, 
                            "coordinator":  nid,
                            "nation_pk": self.navb.kw.get('amb_nation'),
                            "province_pk": self.navb.kw.get('amb_province'),
                            "district_pk": self.navb.kw.get('amb_district'),
                            "referral_facility_pk": self.navb.kw.get('amb_hospital'),
                            "facility_pk" : self.navb.kw.get('amb_facility')
                        }

            #print "\nFORM: ", formdata, "\n"
            message, amb = Enduser.create_ambulance(formdata)
            self.navb.kw = {}
        
        return [message, amb]

    def activate(self):
        cnds    = self.navb.conditions()
        message = ''
        user    = None
        action  = self.navb.kw.get('action')
        try:
            status = True
            if action.strip() == 'deactivate': status = False
            user   = Enduser.get_users({'indexcol = %s': self.navb.kw.get('id')})[0]
            data   = {
                            'telephone': user.telephone,
                            'national_id': user.national_id,
                            'is_active': status
                            }
            ## TODO
            ## CHECK ALL USERS WITH TELEPHONE
            message, user   = Enduser.update_user_info(data)
            if status == False: message = "User %s successfully deactivated." % user.surname
            else:    message = "User %s successfully activated." % user.surname   
        except Exception, e:
            pass
        
        return message, user


