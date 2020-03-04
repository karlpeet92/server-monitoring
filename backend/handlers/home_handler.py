"""
@route("/")
class HomeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        render_data = dict()
        ## Tee query useritele, anna tmeplate'i kaasa ja kuva templates need tsüklis välja               
        BaseModule.__init__()
        bmdb = BaseModule.db
        templates_dir = Config.get_value('app', 'templates_dir')
        static_root = Config.get_value('app', 'static_root')
        render_data['user_name'] = bmdb.query(User.id, User.first_name, User.last_name).all()
        __return_users = []
        for user in render_data['user_name']:
            __return_users.append(user)
        
        render_data["user_name_list"] = __return_users
        render_data['config'] = dict(templates_dir=templates_dir, static_root=static_root)
        return self.render('%s/home.vue' % render_data['config']['templates_dir'], **render_data)

"""
from tornroutes import route

from backend.handlers.base_handler import BaseHandler


@route("/.*")
class HomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        data = self.render_data
        data['xsrf_token'] = self.xsrf_token
        return self.render('%s/dist/index.html' % data['config']['static_path'], **data)
