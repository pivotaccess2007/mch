#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import ast
from com.rwanda.mch.exception.mch_critical_error import MchCriticalError
from datetime import datetime
from decimal import Decimal
import logging
import settings
import ordereddict
import simplejson as json

class BaseService:

    def __init__(self):
        logging.config.fileConfig(settings.APPLICATION_SETTINGS['MCH_HOME'] + '/src/log.conf')
        self.logger = logging.getLogger("mch")

    def setSortLimitParameters(self, params):

        sortLimitParameters = {}

        sortLimitParameters['multipleSort'] = ['-id']
        if(params.get('defaultIdSort')):
            sortLimitParameters['multipleSort'] = [params.get('defaultIdSort')]
            
        if params.get('multipleSortInfo') and '[]' != params.get('multipleSortInfo'):
            sortLimitParameters['multipleSort'] = ast.literal_eval(params.get('multipleSortInfo'))
        elif params.get('sort'):
            sortLimitParameters['multipleSort'] = [params.get('sort')]

        sortLimitParameters['sort'] = 'id'
        if params.get('sort'):
            sortLimitParameters['sort'] = params.get('sort')
        
        sortLimitParameters['dir'] = '-'
        if params.get('dir'):
            if 'asc' == params.get('dir').lower():
                sortLimitParameters['dir'] = ''

        sortLimitParameters['start'] = 0
        if params.get('start'):
            sortLimitParameters['start'] = int(params.get('start'))

        sortLimitParameters['limit'] = 10000000000
        if params.get('limit'):
            limit = params.get('limit')
            sortLimitParameters['limit'] = sortLimitParameters['start'] + int(limit)

        return sortLimitParameters

    def updateRecord(self, record):
        
        if not record.id:
            record.date_created = datetime.now()
        record.last_updated = datetime.now()
        
        record.full_clean(exclude=['id'])

        record.save()

        return record

    def decodeDataToExport(self, data, exportProperties):
        #This is my star code, enyewe I had done some nice stuff during my time. Five stars for this, hata mimi am impressed by myself
        #quickly get the available columns from this resultset data structure
        records = data['records']
        if not records:
            raise MchCriticalError({'message' : "Sorry, no data to export."})

        if not exportProperties:
            raise MchCriticalError({'message' : "Sorry, no export properties specified for export."})

        result = []
        
        exportProperties = json.loads(exportProperties, object_pairs_hook=ordereddict.OrderedDict)#ast.literal_eval(exportProperties)
        exportColumns = exportProperties.keys()#this will hold the export columns as per the data names e.g gf_grant__grant_number
        
        for record in records:            
            
            d = ordereddict.OrderedDict()
            
            for entityProperty in exportColumns:
                
                    if entityProperty in record:
                    
                        if isinstance(record[entityProperty], Decimal):
                            d[exportProperties[entityProperty]] = round(record[entityProperty], 4)
                        elif isinstance(record[entityProperty], unicode):
                            d[exportProperties[entityProperty]] = record[entityProperty].encode('utf-8')
                        else:
                            d[exportProperties[entityProperty]] = record[entityProperty]

            result.append(d)
        #now decode the field names aka headers
        headers = exportProperties.values()
        formatted_headers = []
        
        for header in headers:
            h = header.replace("<br/>", " ")
            formatted_headers.append(h)
        
        return formatted_headers, result
