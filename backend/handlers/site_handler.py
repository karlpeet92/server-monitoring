import tornado.web
import requests
import json

from tornroutes import route
from backend.modules.base_module import BaseModule
from backend.models.site import Site
from backend.modules.connection import Connection                                       
from backend.modules.config import Config

@route("/site")
class SiteHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):

        #print(args[0])
        #site_id = int(args[0])
        render_data = dict()
        BaseModule.__init__()
        bmdb = BaseModule.db
        templates_dir = Config.get_value('app', 'templates_dir')
        static_root = Config.get_value('app', 'static_root')
        render_data['site'] = bmdb.query(Site.id, Site.url, Site.name).all()
        #render_data['sites'] = json.dumps(render_data['sites'])
        # __return_sites = []
        # for site in render_data['sites']:
        #    json.dumps(site)
            
        
        print(render_data)
        render_data['config'] = dict(templates_dir=templates_dir, static_root=static_root)
        return self.render('%s/site.html' % render_data['config']['templates_dir'], **render_data)
