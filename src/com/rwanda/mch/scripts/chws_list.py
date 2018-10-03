#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import sys
from util.record import fetch_users, CHWS_HEADERS
from util.mch_util import export_data_to_xlsx
from model.download import Download


def mch_main(argv):
    larg  = len(argv)

    if larg < 5:
        sys.stderr.write('%s filters start_date end_date filename user_pk\r\n' % (argv[0], ))
        return 1

    filters     = eval(argv[1])
    #print type(filters)
    start_date  = argv[2]
    end_date    = argv[3]
    fn          = argv[4]
    user_pk     = argv[5]

    print "EXECUTING BACKGROUND COMMAND: '%s %s %s %s %s \r\n' " % (argv[0], filters, start_date, end_date, fn)

    records = fetch_users(filters)
    
    headers = CHWS_HEADERS
    def process_filename(headers, records, fn):
        filename = export_data_to_xlsx(headers, records, filename = fn)
        if filename: Download.update_download_status(int(user_pk), filename, status = "COMPLETE")

    return process_filename(headers, records, fn)

    


if __name__ == '__main__':
  bottom  = sys.exit(mch_main(sys.argv))
