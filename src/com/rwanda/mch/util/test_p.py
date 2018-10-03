from drupal_password_hasher import DrupalPasswordHasher

class uObj(object):
    pass_field = ""
    
account = uObj()
#account.pass_field = '$S$DGvu5o4fUw6jy0SUk1dgLPNxIHu4dOy97nrbLjWaSb0m86lAL88f';

d = DrupalPasswordHasher()
check = d.user_hash_password('chop', 15)

print "PWD " + str(check)
account.pass_field = check

check = d.user_check_password('chop', account);
print "RESULT " + str(check)

