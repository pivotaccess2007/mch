#!/usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

##
##
## @author Revence Kalibwani
## RIP Guru Revence, my friend.
##
## @author UWANTWALI ZIGAMA Didier
##
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

##
## The only file to use orm directly
## 

from datetime import datetime 
import json  
 
class CustomEncoderWithType(json.JSONEncoder):
  
  def default(self, o):

    if isinstance(o, datetime):
      return {'__datetime__': o.replace(microsecond=0).isoformat()}
    return {'__{}__'.format(o.__class__.__name__): o.__dict__}
  

class CustomEncoder(json.JSONEncoder):

  def default(self, o):
    if isinstance(o, datetime):
      return o.replace(microsecond=0).isoformat()
    return o.__dict__
