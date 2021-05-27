# Config component for global app configuration
import configparser
import logging
import os
import sys

import tornado
from tornado import locale

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)
_config = None


class CustomLogFormatter(logging.Formatter):
    def format(self, record):
        from backend.modules.base_module import BaseModule

        record.logUserId = ""
        if BaseModule.current_user:
            record.logUserId = str(BaseModule.current_user.id)
        return super().format(record)


class Config:
    @classmethod
    def load_configuration(cls, configuration_filename="test.ini", optional_files=None):
        """
        Loads configuration file. Default is test.ini from config directory
        """
        global _config
        if _config != None:
            return

        _config = configparser.RawConfigParser()
        file_name = os.path.join(os.path.dirname(__file__), "../config/%s" % configuration_filename)
        _config.read(file_name, encoding="utf-8")

        if optional_files != None and type(optional_files) == list:
            for f in optional_files:
                file_name = os.path.join(os.path.dirname(__file__), "../config/%s" % f)
                _config.read(file_name)

    @classmethod
    def get_value(cls, section, name):
        try:
            return _config[section][name]
        except:
            # Config has no value
            return False

    @classmethod
    def set_up_logging(cls):
        logdir = cls.get_value('app', 'log_dir')
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        # logdir = os.path.join(os.path.dirname(__file__), '../logs')

        logging_format = '%(asctime)s %(levelname)s FROM %(module)s.%(funcName)s: %(message)s'
        logging_format_2 = '%(asctime)s %(levelname)s FROM %(module)s.%(funcName)s - [%(logUserId)s]: %(message)s'
        base_hdlr = logging.handlers.TimedRotatingFileHandler('%s/default.log' % logdir, when='midnight',
                                                              backupCount=365,
                                                              utc=True)

        tornado_hdlr = logging.handlers.TimedRotatingFileHandler('/var/www/server-monitor/backend/tornado-server.log',
                                                                 when='midnight',
                                                                 backupCount=365,
                                                                 utc=True)
        tornado_hdlr.setFormatter(CustomLogFormatter(logging_format_2))
        logging.getLogger('tornado.log').addHandler(tornado_hdlr)
        # formatter = logging.Formatter(logging_format)
        base_hdlr.setFormatter(CustomLogFormatter(logging_format_2))
        logging.basicConfig(level=logging.INFO, format=logging_format)  # This is only debug info

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(base_hdlr)

        # E-mail logger
        # cls.add_logger('mailer')

    @classmethod
    def set_up_translations(cls) -> tornado.locale:
        locale_string = cls.get_value('app', 'default_locale')
        translations_dir = os.path.join(os.path.dirname(__file__), '../locale')
        locale.load_gettext_translations(translations_dir, 'messages')
        locale.set_default_locale('en')
        return locale

    @classmethod
    def add_logger(cls, name):
        logging_format = '%(asctime)s %(levelname)s FROM %(module)s.%(funcName)s: %(message)s'
        logdir = cls.get_value('app', 'log_dir')
        log_backup_count = cls.get_value('app', 'log_backup_count')
        if not log_backup_count:
            log_backup_count = 365
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(logging_format)
        hdlr = logging.handlers.TimedRotatingFileHandler('%s/%s.log' % (logdir, name), when='midnight',
                                                         backupCount=log_backup_count,
                                                         utc=True)

        # hdlr.setFormatter(formatter)
        hdlr.setFormatter(CustomLogFormatter(logging_format))
        logger.addHandler(hdlr)
