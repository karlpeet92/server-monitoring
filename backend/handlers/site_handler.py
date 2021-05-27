import tornado.web
import sched, time, requests, pytz
from datetime import datetime
from tornado.escape import json_decode
from tornroutes import route
from backend.modules.base_module import BaseModule
from backend.models.site import Site
from backend.modules.config import Config

BaseModule.__init__()
db = BaseModule.db
s = sched.scheduler(time.time, time.sleep)
site = Site()


@route("/site")
class SiteHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        site_id = self.get_argument('id')
        site_url = self.get_argument("url")
        conn_interval = self.get_argument("interval")

        response_code = requests.get(site_url).status_code
        response_time = requests.get(site_url).elapsed.total_seconds()
        # response_time_array = []
        # response_time_array.append(response_time)

        locate_site = db.query(Site).get(site_id)
        locate_site.status_code = response_code
        locate_site.response_time = response_time
        locate_site.interval = conn_interval

        _tz_TLL = pytz.timezone('Europe/Tallinn')
        _TLL_time = datetime.now(_tz_TLL)
        current_time = _TLL_time.strftime("%H:%M:%S")

        print(site_id, response_code, response_time, current_time, conn_interval)
        # s.enter(5, 1, self.post)
        # s.run()

        BaseModule.db.commit()
        return self.write(dict(id=site_id, response_code=response_code, response_time=response_time, time=current_time))

    def post(self, *args, **kwargs):
        site_data = dict()
        site_data = json_decode(self.request.body)
        site_id = site_data.get("id")
        find_site = db.query(Site).get(site_id)
        print(find_site)
        find_site.name = site_data.get("name")
        find_site.url = site_data.get("url")

        BaseModule.db.add(site)
        BaseModule.db.commit()
        BaseModule.db.refresh(site)

        #site_id = int(args[0])
        #render_data = dict()
        #templates_dir = Config.get_value('app', 'templates_dir')
        #static_root = Config.get_value('app', 'static_root')
        #render_data['site'] = db.query(Site.id, Site.url).all()
        #render_data['sites'] = json.dumps(render_data['sites'])
        # __return_sites = []
        # for site in render_data['sites']:
        #    json.dumps(site)
        #render_data['config'] = dict(templates_dir=templates_dir, static_root=static_root)
        #return self.render('%s/site.vue' % render_data['config']['templates_dir'], **render_data)

    def set_default_headers(self) -> None:
        # TODO :: CHECK THE DOMAINS

        self.set_header("Access-Control-Allow-Origin", "%s" % self.request.headers['Origin'])
        self.set_header('Access-Control-Allow-Credentials', "true")
        self.set_header('Access-Control-Allow-Methods', "GET, POST, PUT, OPTIONS, DELETE")
        self.set_header('Access-Control-Expose-Headers', "Content-Type, X-Jwt")
        self.set_header('Access-Control-Allow-Headers',
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control, X-Jwt")
        self.set_header('Access-Control-Max-Age', 600)

    def check_xsrf_cookie(self) -> None:
        return True

    def options(self, *args, **kwargs):
        pass