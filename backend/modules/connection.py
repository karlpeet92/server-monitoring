from sqlalchemy.orm import scoped_session, sessionmaker, Session, Query
from sqlalchemy import create_engine
from backend.modules.config import Config
import configparser

import logging
import sys

logger = logging.getLogger("init")


class LimitingQuery(Query):
    def get(self, ident):
        # override get() so that the flag is always checked in the
        # DB as opposed to pulling from the identity map. - this is optional.
        return Query.get(self.populate_existing(), ident)

    def __iter__(self):
        return Query.__iter__(self.private())

    def from_self(self, *ent):
        # override from_self() to automatically apply
        # the criterion too.   this works with count() and
        # others.
        return Query.from_self(self.private(), *ent)

    def private(self):
        mzero = self._mapper_zero()
        if mzero is not None:
            crit = mzero.class_.is_deleted == 0

            return self.enable_assertions(False).filter(crit)
        else:
            return self


class Connection:
    session = None

    @classmethod
    def create_connection(cls):
        # Set up SQL connection
        try:
            engine = create_engine("mysql+pymysql://%s:%s@%s/%s?charset=utf8" % (
                Config.get_value('mysql', 'user'), Config.get_value('mysql', 'password'),
                Config.get_value('mysql', 'host'), Config.get_value('mysql', 'database')),
                                   convert_unicode=True,
                                   echo=False,
                                   pool_recycle=360
                                   )
            logger.info(
                "Establishing MySQL connection: %s@%s" % (
                    Config.get_value('mysql', 'user'), Config.get_value('mysql', 'host')))
        except configparser.NoSectionError:
            logger.error("No section for mysql found in config file, make sure the file exists")
            sys.exit(-1)

        sess = scoped_session(sessionmaker(bind=engine, query_cls=LimitingQuery))
        cls.set_connection(sess)

    @classmethod
    def set_connection(cls, session):
        cls.session = session

    @classmethod
    def get_connection(cls) -> Session:
        return cls.session
