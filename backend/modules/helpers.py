import datetime
import decimal
import hashlib
import os
import random
import re
import string

import bleach
import urllib.parse
from bs4 import BeautifulSoup
from sqlalchemy.dialects import mysql

#from backend.vendors.slugify import slugify


class Helper:
    @classmethod
    def generate_random_string(cls, length=15):
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(length))

    @classmethod
    def parse_decimal(cls, pstr, quantize=True):
        price_str = str(pstr).replace(',', '.').replace(' ', '')
        d = decimal.Decimal(price_str)
        if quantize:
            d = d.quantize(decimal.Decimal('1.00'))
        return d

    @classmethod
    def decimal_to_formatted_string(cls, decimal_nr, decimal_places=2, trim_trailing_zeros=False):
        decimal_str = '{0:.{1}f}'.format(decimal_nr, decimal_places)
        if trim_trailing_zeros:
            trim_ending = '.00'
            if decimal_str.endswith(trim_ending):
                decimal_str = decimal_str[:-len(trim_ending)]
        return decimal_str

    @classmethod
    def create_hash(cls, password: str, salt=""):
        m = hashlib.sha512()
        m.update(salt.encode('utf-8'))
        m.update(password.encode('utf-8'))
        return m.hexdigest()

    @classmethod
    def parse_int(cls, x):
        try:
            return int(float(str(x)))
        except:
            return 0

    @classmethod
    def create_unique_filename(cls, full_path):
        original_name = False
        i = 0
        loop_limit = 999999
        while os.path.exists(full_path) and i < loop_limit:
            parts = full_path.rsplit('.', 1)
            if not original_name:
                original_name = parts[0]
            i += 1
            parts[0] = "%s-%s" % (original_name, i)
            full_path = '.'.join(parts)
        if i >= loop_limit:
            return False
        else:
            return full_path

    @classmethod
    def print_query(cls, statement, bind=None):
        import logging
        logger = logging.getLogger()
        logger.info(str(statement.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})))

    @classmethod
    # def sanitize(cls, value, space_to_dash=True, locale='et'):
        #slug = slugify(value, only_ascii=True)
        # slug = re.sub('[^a-zA-Z0-9-]', '', slug)
        # return slug

    @classmethod
    def add_hyperlinks(cls, text):
        r = re.compile(r"((https?://|(http://)?www.)[^ ]+)")
        return r.sub(r'<a href="\1" target="_blank">\1</a>', text).replace('href="www.', 'href="http://www.')

    @classmethod
    def utc_to_local(cls, utc_dt: datetime, format):
        from datetime import timezone
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime(format)

    @classmethod
    def remove_tags(cls, text):
        if text and isinstance(text, str):
            p = re.compile("<.*?>")
            return p.sub('', text).replace('<', '').replace('>', '').replace("'", '').replace('"', '')
        else:
            return text

    @classmethod
    def clean_html(cls, content):
        if not content:
            return ""
        allowed_tags = ['a', 'b', 'blockquote', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'br', 'div', 'center', 'span',
                        'p', 'table', 'tr', 'td', 'th', 'tbody', 'colgroup', 'col', 'small', 'h1', 'h2', 'h3', 'u',
                        'av-heading', 'img', 'avrefs', 'toc']
        allowed_attributes = {'a': ['href', 'title', 'target', 'alt'],
                              '*': ['class', 'id', 'custom-style', 'type', 'style'],
                              'div': ['style'],
                              'img': ['src', 'width', 'height'],
                              'td': ['colspan', 'rowspan'],
                              'table': ['class', 'width'],
                              'av-heading': ['level', 'data-level', 'data-uid'],
                              'avrefs': ['data-reference'],
                              'span': ['style'],
                              'col': ['width']}
        allowed_styles = ['float', 'text-transform', 'text-align', 'display', 'width', 'page-break-before']
        allowed_protocols = bleach.ALLOWED_PROTOCOLS
        allowed_protocols.extend('data')
        content = bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes, styles=allowed_styles,
                               protocols=allowed_protocols)
        return content

    @classmethod
    def normalize_phone_no(cls, phone_number):
        phone_number = phone_number.strip(" ")
        if phone_number.startswith('+372'):
            phone_number = phone_number.replace('+372', '372')
        elif phone_number.startswith('372'):
            pass
        else:
            phone_number = "372%s" % phone_number
        return phone_number

    @classmethod
    def format_decimal(cls, nr):
        if not nr:
            return ""
        if nr % 1 == 0:
            return "%.0f" % nr
        else:
            return "%.2f" % nr

    @classmethod
    def getNameParts(cls, name):
        splitted_name = name.split(' ')
        data = {}
        if len(splitted_name) == 1:
            return dict(first_name=splitted_name[0], last_name="")
        try:
            data['last_name'] = splitted_name[-1].capitalize().strip()

        except:
            data['last_name'] = ''
        try:
            data['first_name'] = splitted_name[:len(splitted_name) - 1][0].capitalize().strip()
        except:
            data['first_name'] = name.strip()
            data['last_name'] = ''
        return data

    @staticmethod
    def headings_from_content(content_text):
        soup = BeautifulSoup(content_text, 'lxml')
        return soup.find_all('av-heading')
