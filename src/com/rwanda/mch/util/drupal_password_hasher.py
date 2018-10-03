import math
import hashlib
from decimal import Decimal
from random import randint

class DrupalPasswordHasher():
    
    DRUPAL_HASH_COUNT = 15

    DRUPAL_MIN_HASH_COUNT = 7

    DRUPAL_MAX_HASH_COUNT = 30

    DRUPAL_HASH_LENGTH = 55

    def user_check_password(self, password, account):
        
        if account.pass_field[:2] == 'U$':
          # This may be an updated password from user_update_7000(). Such hashes
          # have 'U' added as the first character and need an extra md5().
          stored_hash = account.pass_field[1:]
          m = hashlib.md5()
          m.update(password)
          password = m.hexdigest()#.encode('utf-8')
        else:
          stored_hash = account.pass_field

        type = stored_hash[:3]
        
        if '$S$' == type:
            # A normal Drupal 7 password using sha512.
            hash = self._password_crypt('sha512', password, stored_hash)
        elif '$H$' == type:
            pass
        elif '$P$' == type:
            # A phpass password generated using md5.  This is an
            # imported password or from an earlier Drupal version.
            hash = self._password_crypt('md5', password, stored_hash)
        
        return (hash and stored_hash == hash)

    def _password_crypt(self, algo, password, setting):
        # The first 12 characters of an existing hash are its setting string.
        setting = setting[:12]
        
        if setting[0] != '$' or setting[2] != '$':
          return False
        
        count_log2 = self._password_get_count_log2(setting)
        # Hashes may be imported from elsewhere, so we allow != DRUPAL_HASH_COUNT
        if count_log2 < self.DRUPAL_MIN_HASH_COUNT or count_log2 > self.DRUPAL_MAX_HASH_COUNT:
          return False
        
        salt = setting[4: 12]
        
        # Hashes must have an 8 character salt.
        if len(salt) != 8:
          return False
        
        # Convert the base 2 logarithm into an integer.
        count = 1 << count_log2

        # We rely on the hash() function being available in PHP 5.2+.
        hash = hashlib.sha512(salt + password).digest()
        
        for i in range(count):
            hash = hashlib.sha512(hash + password.encode("utf-8")).digest()
        
        hash_length = len(hash)
        
        output =  setting + self._password_base64_encode(hash, hash_length)
        # _password_base64_encode() of a 16 byte MD5 will always be 22 characters.
        # _password_base64_encode() of a 64 byte sha512 will always be 86 characters.
        expected = Decimal('12') + Decimal(str(math.ceil((Decimal('8') * Decimal(str(hash_length))) / Decimal('6'))))
        
        if len(output) == expected:
            return output[:self.DRUPAL_HASH_LENGTH]
        
    def _password_get_count_log2(self, setting):
        
        itoa64 = self._password_itoa64()
        
        return itoa64.index(setting[3])
      
    def _password_itoa64(self):
        return './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    
    def _password_base64_encode(self, input, count):

        output = ''
        i = 0
        itoa64 = self._password_itoa64()
        
        while i < count:
            
          value = ord(input[i])
          i = i + 1
          
          output += itoa64[value & 0x3f]
          
          if i < count:
            value |= ord(input[i]) << 8
          
          output += itoa64[(value >> 6) & 0x3f]
          
          if i >= count:
            break          
          i += 1
          
          if i < count:
            value |= ord(input[i]) << 16
          
          output += itoa64[(value >> 12) & 0x3f]
          
          if i >= count:
            break
          i += 1
          
          output += itoa64[(value >> 18) & 0x3f]
        
        return output
    
    def user_hash_password(self, password, count_log2):
        
        return self._password_crypt('sha512', password, self._password_generate_salt(count_log2))
    
    def _password_generate_salt(self, count_log2):
        output = '$S$'
        # We encode the final log2 iteration count in base 64.
        itoa64 = self._password_itoa64()
        output += itoa64[count_log2]
        
        #6 bytes is the standard salt for a portable phpass hash.
        v = randint(1, 15)
        z = v + 6
        output += self._password_base64_encode(itoa64[v: z], 6)
        
        return output
