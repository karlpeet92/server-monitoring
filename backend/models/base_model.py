import datetime
import decimal
import logging

import sqlalchemy
from sqlalchemy import Column, MetaData, DateTime, func, text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, relationship, deferred
from tornado.escape import json_encode

mymetadata = MetaData()
Base = declarative_base(metadata=mymetadata)
console = logging.getLogger("print")

class BaseModel(object):
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_default charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
    __forbidden_fields__ = ['_sa_instance_state', 'is_deleted', 'password']
    created_at = Column(DateTime, default=func.UTC_TIMESTAMP())
    updated_at = Column(DateTime, default=func.UTC_TIMESTAMP(), onupdate=text('UTC_TIMESTAMP'))
    is_deleted = Column(Boolean, default=0)

    def get_fields(self):
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, sqlalchemy.orm.ColumnProperty)]

    def to_dict(self, without_children=False):
        import json
        # Here we allow fields what are serializable
        result = {}
        # try:
        if not self.__forbidden_fields__:
            print(self.__class__)
            print(self.__forbidden_fields__)
        for name in self.__dict__.keys():

            if name not in self.__forbidden_fields__:
                r = getattr(self, name)
                if isinstance(r, dict):
                    result[name] = r
                    continue
                if r or isinstance(r, int) or isinstance(r, str):
                    if isinstance(r, list):
                        result[name] = []
                        for i in r:
                            if not without_children and isinstance(i, Base):
                                result[name].append(i.to_dict())
                            else:
                                result[name].append(i)
                    elif not without_children and isinstance(r, Base):
                        result[name] = r.to_dict()
                    elif isinstance(r, datetime.date) \
                            or isinstance(r, datetime.datetime) \
                            or isinstance(r, decimal.Decimal) \
                            or isinstance(r, datetime.time):
                        result[name] = str(r).strip()
                    # elif name in self.__json_fields__:
                    #     if r:
                    #         result[name] = json.loads(r)
                    #     else:
                    #         result[name] = dict()
                    elif name == 'content':
                        ## DO NOT STRIP CHOICE CONTENT!
                        result[name] = r
                    else:
                        try:
                            result[name] = r.strip()
                        except:
                            result[name] = r
                elif isinstance(r, bool):
                    result[name] = r if r else False
                elif not r:
                    result[name] = None
        return result
        # return json.dumps(result, check_circular=True)


    def populate_from_dict(self, data):
        db_object_fields = self.get_fields()
        for name in data:
            if name not in ['id', 'updated_at', 'updated_by']:
                if name in db_object_fields:
                    attr = getattr(self, name)
                    if not isinstance(attr, Base) and not isinstance(attr, list):
                        value = data[name]
                        if isinstance(value, dict) and not name == 'reminder_tree':
                            value = json_encode(value)
                        if isinstance(attr, int):
                            if value == "":
                                value = 0
                            elif value:
                                value = int(value)
                        setattr(self, name, value)

    def __repr__(self):
        return "%s" % self.__dict__

    def duplicate(self):
        arguments = dict()
        for name, column in self.__mapper__.columns.items():
            if not (column.primary_key or column.unique):
                arguments[name] = getattr(self, name)
        return self.__class__(**arguments)
