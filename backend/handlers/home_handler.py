import magic
from tornroutes import route

from backend.handlers.base_handler import BaseHandler


@route("/.*?")
class HomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        data = self.render_data
        return self.render('%s/home.html' % data['config']['templates_dir'], **data)
