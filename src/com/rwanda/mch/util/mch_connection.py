#!/usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


### 
### None should call any settings variables 
### Out of of this module
### all settings should be called and initialized here
###

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import mch_settings as MCH_SETTINGS
import MySQLdb
import psycopg2
from orm.postgresql import orm

__mysql_connection__ = MySQLdb.connect(
                                        host = MCH_SETTINGS.MySQL_HOST,
                                        port = MCH_SETTINGS.MySQL_PORT,
                                        user = MCH_SETTINGS.MySQL_USER, 
                                        passwd = MCH_SETTINGS.MySQL_PASSWORD, 
                                        db = MCH_SETTINGS.MySQL_DATABASE
                                       )

__mysql_connection1__ = MySQLdb.connect(
                                        host = MCH_SETTINGS.MySQL_HOST1,
                                        port = MCH_SETTINGS.MySQL_PORT1,
                                        user = MCH_SETTINGS.MySQL_USER1, 
                                        passwd = MCH_SETTINGS.MySQL_PASSWORD1, 
                                        db = MCH_SETTINGS.MySQL_DATABASE1
                                       )

__postgresql_connection__ = psycopg2.connect(
                                              host = MCH_SETTINGS.PSQL_HOST,
                                              port = MCH_SETTINGS.PSQL_PORT,
                                              user = MCH_SETTINGS.PSQL_USER,
                                              password = MCH_SETTINGS.PSQL_PASSWORD,
                                              dbname  = MCH_SETTINGS.PSQL_DATABASE
                                              
                                             )


orm.ORM.connect(
                  host = MCH_SETTINGS.PSQL_HOST,
                  port = MCH_SETTINGS.PSQL_PORT,
                  user = MCH_SETTINGS.PSQL_USER,
                  password = MCH_SETTINGS.PSQL_PASSWORD,
                  dbname  = MCH_SETTINGS.PSQL_DATABASE
                  
                 )




MCONN = __mysql_connection__
MCONN1 = __mysql_connection1__
PCONN = __postgresql_connection__

SALT_STRENGTH = MCH_SETTINGS.SALT_STRENGTH
AUTH_HOME = MCH_SETTINGS.AUTH_HOME

APP_DATA = MCH_SETTINGS.APP_DATA
WEBAPP = MCH_SETTINGS.WEBAPP
SECRET = MCH_SETTINGS.SECRET
GESTATION = MCH_SETTINGS.GESTATION
NBC_GESTATION = MCH_SETTINGS.NBC_GESTATION
PNC_GESTATION = MCH_SETTINGS.PNC_GESTATION
TRACKING_DAYS = MCH_SETTINGS.TRACKING_DAYS

ANC_GAP         = MCH_SETTINGS.ANC_GAP
BMI_MIN         = MCH_SETTINGS.BMI_MIN
BMI_MAX         = MCH_SETTINGS.BMI_MAX
MIN_WEIGHT      = MCH_SETTINGS.MIN_WEIGHT
MAX_WEIGHT      = MCH_SETTINGS.MAX_WEIGHT

INC_ID = MCH_SETTINGS.INC_ID
FACILITIES = MCH_SETTINGS.FACILITIES

