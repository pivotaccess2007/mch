#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import MySQLdb
from time import strftime


import MySQLdb

if __name__ == "__main__":
    conn = MySQLdb.connect (host='mail.rwanda.mch.org',
                            user='mch.org',
                            passwd='ykex731',
                            db='mch_v1_0')
    cursor = conn.cursor()

    file_path = 'unsubscribe.txt'

    f = open(file_path, 'r')
    for email in f:
        email = email.rstrip()
        if email:
            query = "UPDATE subscriber SET SubscriberStatus = 2, UnsubscribedOn = '%s' where emailaddress = '%s'"
            cursor.execute(query % (strftime("%Y-%m-%d"), email))
        #print (query % (1, email))

    conn.commit()
    conn.close()

