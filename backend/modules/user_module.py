import datetime
import hashlib
import os
import re
import sys
import traceback
import urllib.parse
from operator import or_, and_

from backend.models import User
from backend.modules.base_module import BaseModule
from backend.modules.config import Config
from backend.modules.helpers import Helper


class UserModule(BaseModule):   
    @classmethod
    # TODO :: First check if user with same e-mail exists, if does, raise an exception
    def create_user(cls, data): 
        BaseModule.__init__()
        db = BaseModule.db

        salt = Config.get_value('app', 'password_salt')  
        mypass = data.get("password")   
        pw_hash = cls.create_hash(mypass, salt)
        print(pw_hash)
        if db.query(User).filter(User.email==data.get("email")).all():
            raise ValueError("Email is not unique")
    # TODO :: if user does not exist, add it to database
        else:           
            new_user = User(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                password=pw_hash,
                phone_number=data.get("phone_number"),
            )
        db.add(new_user)
        db.commit()
        
    # Hash the password with salt that is read from config file Config.get_value('app', 'password_salt'); Use sha512.
    # If necessary google "How to hash string in Python with sha 512"; hashlib is the library for it.
    @classmethod
    def create_hash(cls, password=None, salt=None):
        m = hashlib.sha512()
        m.update(salt.encode('utf-8'))
        m.update(password.encode('utf-8'))
        return m.hexdigest()
          
    # Add the user to database
    # user = User()
    # user.first_name = data.get('first_name') and so on...
