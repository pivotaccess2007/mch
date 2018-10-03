#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import os.path
import time

from datetime import datetime
import logging
import os
import settings
import urllib2
from urllib2 import URLError

class Downloader:

    def __init__(self, connection, localRepoDir):

        self.logger = logging.getLogger("mch")

        self.connection = connection
        self.localRepoDir = localRepoDir
    
    def __recentDownload(self, downloadType):
        """
        Fetch the most recent successfull download from the db records
        """
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT file_size, file_modification_time FROM download_audit WHERE download_type =  %(dtype)s AND download_completion_time IS NOT NULL ORDER BY id DESC LIMIT 1", {'dtype': downloadType})
        record = cursor.fetchone()
        cursor.close ()
        
        return record

    def __auditFileRequest(self, params, recordId=None):
        """
        Log the remote file access operation
        """

        query = None
                
        params['last_updated'] = datetime.now()
        
        cursor = self.connection.cursor()
        
        if recordId:
            values = ', '.join(['%s = %%(%s)s' % (x, x) for x in params])

            query = 'UPDATE download_audit SET %s WHERE id = %d' % (values, recordId)
        else:
            params['date_created'] = datetime.now()
            
            fields = ', '.join(params.keys())
            values = ', '.join(['%%(%s)s' % x for x in params])
            
            query = 'INSERT INTO download_audit (%s) VALUES (%s)' % (fields, values)
        
        cursor.execute(query, params)
        recordId = cursor.lastrowid

        self.connection.commit()
        cursor.close ()
        
        return recordId

    def __download(self, downloadType):
        """
            Download module for any particular url.
            It will download and check if the remote file is more recent than the local file
            """

        downloadAudit = {}
        downloadAudit['download_type'] = downloadType
        downloadAudit['remote_url'] = self.remoteUrl#get the url that is being requested
        downloadAudit['download_start_time'] = datetime.now()#capture the date when the url was accessed
        #first make an entry into the db stating that a download operation is to be attempted
        downloadAudit['comment'] = 'Starting download operation'
        newRecordId = self.__auditFileRequest(downloadAudit)

        downloadAudit = {}
        try:
            req = urllib2.Request(self.remoteUrl)
            r = urllib2.urlopen(req)
        except URLError, urle:
            if hasattr(urle, 'reason'):
                downloadAudit['comment'] = urle.reason
            else:
                downloadAudit['comment'] = urle.__str__()
                
            self.__auditFileRequest(downloadAudit, newRecordId)
            
            return None #just return since there has been an error in connecting with the remote server

        try:
            downloadAudit['local_file_path'] = '/' + self.localRepoDir + '/' + downloadType + '/' + downloadType + '-' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.xls'

            file = open(settings.APPLICATION_SETTINGS['MCH_HOME'] + downloadAudit['local_file_path'], 'wb')
            file.write(r.read())

            #headerInfo = r.info()

            isFileToBeProcessed = False #default is not to process file

            #before downloading, check to see if the remote file is more recent than the last file that was downloaded, whose
            #information is in the db
            latestFetch = self.__recentDownload(downloadType)

            if latestFetch:
                downloadAudit['file_size'] = latestFetch[0]
                file.flush()#make sure all the content is written to file 
                os.fsync(file.fileno())
                if latestFetch[0] != os.path.getsize(file.name):
                    isFileToBeProcessed = True
            else:
                isFileToBeProcessed = True

            if isFileToBeProcessed:
                downloadAudit['file_size'] = os.path.getsize(file.name)
                downloadAudit['file_modification_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                downloadAudit['download_completion_time'] = datetime.now()
                #now make an audit entry into the database
                downloadAudit['comment'] = 'New file to be processed.'
            else:
                os.remove(file.name)#remove the file since it looks like it has already been downloaded and processed
                #now make an audit entry into the database
                downloadAudit['comment'] = 'File already downloaded, purged it from the file system.'

            self.__auditFileRequest(downloadAudit, newRecordId)
            file.close()
        except Exception as e:
            self.logger.exception('\n Unknown fatal error occured during the downloading of the raw files. %s' % str(e))

        return newRecordId

    def downloadFile(self, remoteUrl, type):

        self.remoteUrl = remoteUrl
        #first check to see if the dir exists and if not create one
        self.__checkRepoDir(type)

        newRecordId = self.__download(type)

        return newRecordId

    def __checkRepoDir(self, dir):

        dir = settings.APPLICATION_SETTINGS['MCH_HOME'] + '/' + self.localRepoDir + '/' + dir

        if not os.path.exists(dir):
            os.makedirs(dir)

