#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from django.http import HttpResponse
from com.rwanda.mch.model.models import MchPlatformFunction
from com.rwanda.mch.model.models import MchPlatformStatistic
from com.rwanda.mch.model.models import LoginAudit
import time
from django.db import connection

class MchSessionAuthMiddleware:
    
    def  __init__(self):
        self.omitActions = ['index', 'logout', 'authenticate', 'serve', 'passwordForget', 'saveUser']
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        
        if request.session.get('user', 0):
            #seems the user is already logged in, log this access for statistic purposes
            if 'serve' != view_func.func_name and '/filterCriteria/list/' != request.path:
                #check to see if this function is already in the database
                self.mch_plaform_function_check(request.path)
                
                self.log_access(request.session['login_audit_id'], request.path)
                
            return None
        else:   
            if view_func.func_name in self.omitActions:
                return None
            
            return HttpResponse('login_redirection')
        
    def log_access(self, login_audit_id, request_path):
        #get today's date
        todays_date = time.strftime('%Y-%m-%d')
        function_obj = MchPlatformFunction.objects.filter(function_name = request_path)
        
        stat = MchPlatformStatistic.objects.filter(login_audit = login_audit_id, 
        platform_function = function_obj[0].id, 
        access_date = todays_date)
        
        if stat:
            current_count = stat[0].access_count + 1
            
            stat[0].access_count = current_count
            stat[0].save()
        else:
            login_audit_obj = LoginAudit.objects.filter(id = login_audit_id)
            
            stat = MchPlatformStatistic(login_audit = login_audit_obj[0],
            platform_function = function_obj[0],
            access_date = todays_date,
            access_count = 1)
            
            stat.save()
        
    def mch_plaform_function_check(self, request_path):
        
        function_name = MchPlatformFunction.objects.filter(function_name = request_path)

        if not function_name:
            func = MchPlatformFunction(function_name = request_path)
            func.save()

