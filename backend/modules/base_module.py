import inspect
import os

from sqlalchemy.orm import load_only

# Load all the Models for Connection
from backend.models import *

from backend.modules.connection import Connection
from backend.modules.config import Config


class BaseModule(object):
    db = False
    """:type: UserCompany"""
    current_user = None
    """:type: User"""
    inited = False
    locale_code = 'en'
    locale = None
    """ :type: tornado.locale.Locale """

    session = None
    debug = False
    translations = False

    @classmethod
    def __init__(cls):
        if not cls.inited:
            mod = False
            frm = inspect.stack()[1]
            if frm:
                mod = inspect.getmodule(frm[0])

            cls.inited = True
            try:
                environment = os.environ["SM_ENVIRONMENT"]
            except:
                environment = 'test'

            print("SETTING ENVIRONMENT TO %s" % environment)

            Config.load_configuration('%s.ini' % environment)
            Connection.create_connection()
            cls.db = Connection.get_connection()
            Config.set_up_logging()
            cls.translations = Config.set_up_translations().get(cls.locale_code)
            cls.locale = Config.set_up_translations().get(cls.locale_code)

            if mod and hasattr(mod, "__CRON_NAME__"):
                Config.add_logger(mod.__CRON_NAME__)

    @classmethod
    def __(cls, *args):
        locale = cls.translations.get(cls.locale_code)
        return locale.translate(*args)

    @classmethod
    def get_current_user(cls):
        """
        Returns new object with DB session
        """
        return cls.db.query(User).get(cls.current_user.id)
