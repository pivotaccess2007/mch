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
from util.record import migrate, fetch_summary, fetch_download, fetch_download_by_id, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError
import datetime


class Download(RSMSRWObj):
    """A Download report from RapidSMS. Downloads have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'download'

    def __init__(self, user_pk, filename):
        """Return a Download object with *filename* and *user_pk* """
        self.user_pk	  = user_pk
        self.filename     = filename


    def get(self):
        """ Retrieve a download object and return download record """
        try:
            err = fetch_download(self.user_pk, self.filename)
            return err
        except:
            raise MchCriticalError(Exception('Download cannot be fetched'))
        return None

    def save(self, user = None, FIELDS = {}):
        """ Save a download object and return indexcol """
        try:
            if user:
                FIELDS.update({
                                    "user_pk":  user.indexcol,
                                    "user_phone":  user.telephone, 
                                    "nation_pk":    user.nation_pk,
                                    "province_pk":  user.province_pk,
                                    "district_pk":  user.district_pk,
                                    "referral_facility_pk": user.referral_facility_pk,
                                    "facility_pk":  user.facility_pk,
                                    "sector_pk":    user.facility_pk,
                                    "cell_pk":  user.facility_pk,
                                    "village_pk":   user.facility_pk, 
                                })
                print "FIELDS: ", FIELDS            
                dwn = migrate(Download._table, FIELDS)
                return dwn
            else:
                raise MchCriticalError(Exception('Download cannot be saved'))
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Download cannot be saved'))
        return None

    @staticmethod
    def get_by_id(byid):
        return fetch_download_by_id(byid)

    @staticmethod
    def process_download(user, command, description = 'Download', filename = 'exports.xlsx',
                             filters = {}, start = datetime.datetime.now(), end = datetime.datetime.now()):
        import subprocess
        
        command = './rw.py %(command)s "%(cnds)s" "%(start)s" "%(end)s" "%(file)s" "%(user_pk)s" ' % {
                    'command': command,
                    'cnds': filters,
                    'start':  start,
                    'end':  end,
                    'file': filename,
                    'user_pk': user.indexcol
                    }

        fields = {'filename': filename, 'filters': '"%s"' % filters, 'description' : description, 'start_date': start, 'end_date' : end}
        dwn = Download(user.indexcol, filename)
        dwnsv = dwn.save(user = user, FIELDS = fields)
        print "COMMAND: ", command
        subprocess.Popen(command, shell=True)        
        if dwnsv:
            dwnfile = Download(user.indexcol, filename)
            return dwnfile.get()
        
        return None

    @staticmethod
    def update_download_status(user_pk, filename, status = "COMPLETE"):
        """ Not all info is update here except few supplied data info"""
        try:
            download = fetch_download(user_pk, filename)
            if not download:
                 return ( 'Download does not exist with user_pk %s and filename %s' % (user_pk, filename) , None)
            else:
                #print "UPDATE DATA: ", data
                data = {'indexcol': download.indexcol, 'status': status} 
                migrate(Download._table, data)                    
                return ( 'Download updated', download)            
        except Exception, e:
            print e
            pass
        return ('Error', None)


    @staticmethod
    def fetch_downloads(cnds, cols, exts):
        return fetch_summary(Download._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_downloads(cnds, cols):
        return fetch_table(Download._table, cnds, cols)

    @staticmethod
    def fetch_downloads_by_location(cnds, group_by = [], INDICS = []):
        data = []#; print cnds, group_by, INDICS
        for INDIC in INDICS:
            #print "CNDS: ", cnds
            cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
            curr_cnds = {INDIC[1]: ''}
            if INDIC[1] == 'total':
                cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
                curr_cnds = {}           
            curr_cnds.update(cnds)
            #print cols
            data.append(fetch_table_by_location(Download._table, curr_cnds, cols, group_by))
        return data
