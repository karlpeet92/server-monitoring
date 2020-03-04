import datetime
import logging
from urllib.parse import urlparse

import sqlalchemy
import tornado.web
from sqlalchemy.orm import load_only

from backend.modules.base_module import BaseModule
from backend.modules.config import Config
from backend.models import User

logger = logging.getLogger("basehandler")
from backend.modules.session import Session


# BaseHandler gives basic properties to handler object: database, user, decorator functions and so on.
# Use it only on global functions/variables, other stuff should go to "modules" package!

class BaseHandler(tornado.web.RequestHandler):
    __VIEW_ID__ = ""
    __VIEW_TITLE__ = ""
    include_vue = False
    render_data = dict()
    CHECK_COOKIE = None

    def prepare(self):
        try:
            url = urlparse(self.request.full_url())
            self.hostname = '%s://%s' % (url.scheme, url.hostname)
        except:
            logger.error("Something went really really bad with parsing URL! Take a look, quickly!")
        forwarded_ip = self.request.headers.get("X-Forwarded-For", self.request.remote_ip)
        if forwarded_ip:
            forwarded_ip = forwarded_ip.replace('127.0.0.1', '').strip(' ,')

        if tornado.netutil.is_valid_ip(forwarded_ip):
            self.request.remote_ip = forwarded_ip

        #if not self.is_api_call():
        #    if not self.get_session_id():
        #        if not self.start_session():
        #            logger.info("Start session")
        #            return self.db.close()

        if self.request.uri.startswith('/api/'):
            self.set_header('Content-Type', 'application/json')
        self.set_header('X-Frame-Options', 'SAMEORIGIN')

        BaseModule.locale_code = self._get_locale()
        BaseModule._ = self._
        #BaseModule.session = self.session
        self.set_default_render_data()
        BaseModule.current_user = self.get_current_user()

        self.update_session_cookie()
        super(BaseHandler, self)

    def check_xsrf_cookie(self):

        # Except some URLs
        try:
            return super(BaseHandler, self).check_xsrf_cookie()
        except Exception as e:
            from tornado.web import HTTPError
            raise HTTPError(403, "Invalid XSRF token")

    @property
    def db(self) -> sqlalchemy.orm.Session:
        return self.application.db

    def get_current_user(self, force_refresh=False) -> User:
        user = None
        if 'user' in self.session:
            user = self.session['user']

        if force_refresh and user:
            user = self.db.query(User).get(user.id)
            self.set_current_user(user)
        return user

    def regenerate_session_token(self):
        sess = Session(self.application.session_store, self.session.sessionid)
        # Get the session info and redirect it to new session Key
        nk = sess.change_session_key()
        expires = self.get_cookie_expiry_date()
        self.set_secure_cookie(self.get_session_cookie_name(), sess.sessionid, expires=expires, path='/',
                               domain=self.get_cookie_domain(), secure=True,
                               httponly=True)

    def set_current_user(self, user):
        self.session['user'] = user
        BaseModule.current_user = user

    def get_cookie_domain(self):
        domain = self.hostname.replace('http://', '')
        domain = domain.replace('https://', '')
        return domain

    def update_session_cookie(self):
        """
        Checks if cookie is expiring, if not, does nothing, if is, then move expires date
        :return:
        """
        sid = self.get_session_cookie_name()
        if sid in self.request.cookies:
            expires = self.get_cookie_expiry_date()
            will_expire = datetime.datetime.now() + datetime.timedelta(hours=1)
            if 'expires_at' not in self.session or (
                    'expires_at' in self.session and self.session['expires_at'] <= will_expire):
                # Set expires
                self.session['expires_at'] = expires
                self.set_secure_cookie(self.get_session_cookie_name(), self.session.sessionid, expires=expires,
                                       path='/',
                                       domain=self.get_cookie_domain(), secure=True,
                                       httponly=True)

    def start_session(self):
        domain = self.get_cookie_domain()
        if not self.get_session_id() and self.get_secure_cookie(
                self.get_session_cookie_name()) and '/api/login' not in self.request.full_url():
            logger.info(
                "Should clear up cookie as there is no sess id, but cookie exists. SessID: %s" % self.get_session_id())
        logger.info("Setting secure cookie for domain %s with name %s" % (domain, self.get_session_cookie_name()))
        expires = self.get_cookie_expiry_date()
        print(domain)
        self.set_secure_cookie(self.get_session_cookie_name(), self.session.sessionid, expires=expires, path='/',
                               domain=domain, secure=False,
                               httponly=True)
        self.session['expires_at'] = expires
        self.db.close()
        if not self.is_bot() and not self.get_argument("up", None):
            return self.redirect(self.request.uri)
        return True

    def get_cookie_expiry_date(self):
        session_length_in_hours = Config.get_value('app', 'session_length_in_hours')
        if not session_length_in_hours:
            # Set default Session length
            session_length_in_hours = 3
        elif session_length_in_hours.isdigit():
            session_length_in_hours = int(session_length_in_hours)

        expires = datetime.datetime.now() + datetime.timedelta(hours=session_length_in_hours)
        return expires

    def get_session_id(self):
        if self.get_secure_cookie(self.get_session_cookie_name(), max_age_days=0.08):
            return self.get_secure_cookie(self.get_session_cookie_name(), max_age_days=0.08).decode("utf8")
        else:
            return None

    def get_session_cookie_name(self):
        cookie_name = Config.get_value('app', 'session_cooke_name')
        if cookie_name:
            return cookie_name
        else:
            return "wpsid"

    #@property
    #def session(self):
    #    session_sid = self.get_secure_cookie(self.get_session_cookie_name())
    #    if session_sid:
    #        return Session(self.application.session_store, session_sid.decode("utf8"))
    #    else:
    #        return Session(self.application.session_store, session_sid)

    def is_user_logged_in(self):
        return True if self.session and 'user' in self.session else False

    def is_api_call(self):
        return self.CHECK_COOKIE == "SKIP" or self.request.headers.get(
            "X-Requested-With") == "XMLHttpRequest" or 'api/v1/' in self.request.full_url()

    def is_bot(self):
        bot_array = ["googlebot", "twitterbot", "facebookexternalhit", "google.com/bot.html", "tweetmemebot",
                     "sitebot", "msnbot", "robot", "google.com", "yahoo", "bingbot", "TweetedTimes Bot",
                     "Google-Site-Verification"]
        if not 'User-Agent' in self.request.headers:
            return True

        for bot in bot_array:
            if bot in self.request.headers["User-Agent"]:
                return True
        return False

    def get_user_locale(self):
        return tornado.locale.get(self._get_locale())

    def _get_locale(self):
        return 'en'

    @property
    def _(self):
        return self.get_user_locale().translate

    def reload_user_session(self):
        current_user = self.get_current_user()
        user = self.db.query(User).get(current_user.id)
        self.set_current_user(user)

    def set_default_render_data(self):
        """
        Sets default data that can be used in view files
        :return:
        """
        self.render_data['config'] = {}
        self.render_data['features'] = {}
        self.render_data['xsrf_token'] = self.xsrf_token
        self.render_data['_'] = self._
        self.render_data['config']['static_root'] = Config.get_value('app', 'static_root')
        self.render_data['config']['url'] = Config.get_value('app', 'url')
        self.render_data['config']['templates_dir'] = Config.get_value('app', 'templates_dir')
        self.render_data['config']['use_minified_resources'] = Config.get_value('app',
                                                                                'use_minified_resources') == 'True'

    def get_template_path(self):
        """ Override for parent template
        :return: string
        """
        return Config.get_value('app', 'templates_dir')

    def check_for_unsupported_browser(self):
        user_agent_header = self.request.headers.get("User-Agent")
        is_internet_explorer = 'MSIE' in user_agent_header or 'Trident' in user_agent_header
        if is_internet_explorer:
            return self.render(
                template_name='%s/admin/unsupported-browser.html' % self.render_data['config']['templates_dir'],
                **self.render_data)

    def on_finish(self):
        self.db.flush()
        self.db.close()
        import sys
        sys.stdout.flush()
