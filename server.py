import logging
import sys
import redis

#import redis
import tornado.ioloop
import tornado.locale
import tornado.web
from tornroutes import route

from backend.handlers import *
from backend.modules.base_module import BaseModule
from backend.modules.connection import Connection
from backend.modules.config import Config
from backend.modules.session import RedisSessionStore

BaseModule.__init__()
logger = logging.getLogger("init")


# Set up routes
class Application(tornado.web.Application):
    routes = route.get_routes()

    def __init__(self):
        debug = False
        if Config.get_value('app', 'debug') == 'True':
            logger.warning("Server started with debug mode!")
            debug = True
        tornado.web.Application.__init__(self, self.routes, debug=debug,
                                         cookie_secret=Config.get_value('secrets', 'cookie_secret'),
                                         xsrf_cookies=True, serve_traceback=debug
                                         )
        self.redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0,
                                       password=Config.get_value('redis', 'password'))
        self.session_store = RedisSessionStore(self.redis)
        self.db = Connection.get_connection()  # scoped_session(sessionmaker(bind=engine))

   

if __name__ == "__main__":
    app = Application()
    port = Config.get_value('server', 'port')
    if sys.argv and len(sys.argv) > 1:
        port = sys.argv[1]

    print("Starting server on port %s" % port)
    app.listen(port)
    loop = tornado.ioloop.IOLoop.instance().start()
