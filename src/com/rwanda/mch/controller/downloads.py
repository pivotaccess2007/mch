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
from model.download import Download
import datetime

class DownloadController(RSMSRWController):
    
    def __init__(self, navb):
        self.navb = navb

    def download_file(self):

        cnds    = self.navb.conditions()
        tmn     = datetime.datetime.now()
        tm      =  '%s_%s_%s_%s_%s_%s' % (tmn.year, tmn.month, tmn.day, tmn.hour, tmn.minute, tmn.second)

        export  = self.navb.kw.get('export')
        name = command = description = 'export'
        msg  = ""
        download = Download.get_by_id(self.navb.kw.get('download'))
        if export:
            if export == 'performance':
                name = 'chws_performance'
                description = 'Chws performance'
                command = 'performance'
            elif export == 'chws':
                name = 'chws_list'
                description = 'Chws list'
                command = 'chws_list'
            else:
                return msg, download

            filename = '%(name)s_%(tm)s_from_%(start)s_to_%(end)s.xlsx' % { 'name': name,
                                                                                    'start': self.navb.start.date(),
                                                                                    'end': self.navb.finish.date(),
                                                                                    'tm': tm
                                                                                   }

            dwn = Download.process_download(self.navb.user, command, description = description, filename = filename,
                                 filters = cnds, start = self.navb.start.date(), end = self.navb.finish.date())
            if dwn:
                msg, download = ("Export file is being processed, once done you will be able to see download link available. ", dwn)

            else:
                msg, download = ("Export file failed to process. Please try again.", None)

        return msg, download

    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) <= '%s'" % (self.navb.finish) : ''})
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : ''})#;print cnds         
        exts = {}
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('description', 'Description'),
                                              ('status', 'Status'),
                                              ('created_at', 'Creation Date'),
                                              ('filename', 'Filename'),
                                              ('indexcol', 'ID')
                                              
                                            ])

        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/exportsdash?download=%s">Download File</a>' % (x), })
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])
        dcols = [x[0] for x in cols]
        cnds.update({'user_pk = %s': self.navb.user.indexcol})
        nat = Download.fetch_log_downloads(cnds, dcols)
        desc  = 'Exported files list'
        
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)
