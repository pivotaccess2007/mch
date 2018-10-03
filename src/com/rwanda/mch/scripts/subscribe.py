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


if __name__ == "__main__":
    conn = MySQLdb.connect (host='mail.rwanda.mch.org',
                            user='mch.org',
                            passwd='ykex731',
                            db='mch_v1_0')
    cursor = conn.cursor()

    file_path = 'subscribe.txt'

    f = open(file_path, 'r')
    for line in f:
        email = None
        fullname = None
        
        if line:
            tokens = line.split()
            email = tokens[len(tokens) - 1].rstrip()

            tokens.pop()
            fullname = ' '.join(tokens)

        if email:
            query = "INSERT INTO subscriber (SubscriberStatus, emailaddress, Name, SubscribedOn) VALUES (%d, '%s', '%s', '%s')"
            cursor.execute(query % (1, email, fullname, strftime("%Y-%m-%d")))
            #print (query % (1, email))

    conn.commit()
    conn.close()

