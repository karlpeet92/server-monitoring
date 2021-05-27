import json
import tornado.web
from tornado.escape import json_decode, json_encode
from tornroutes import route
from backend.models.user import User
from backend.models.site import Site
from backend.models.user_site import UserSite
from backend.modules.base_module import BaseModule


@route("/api/v1/user-site/?(.*)?")
class APIV1UserSiteHandler(tornado.web.RequestHandler):
    _VIEW_TITLE_ = "UserSite"

    def get(self, args, *kwargs):
        self.set_header('Content-Type', 'application/json')
        user_id = self.get_argument('user_id')
        usersite_array = []
        db = BaseModule.db
        if user_id:
            user_sites = db.query(UserSite).filter(UserSite.user_id == user_id).all()
            for usersite in user_sites:
                #print(usersite)
                usersite_array.append(usersite.to_dict())

        dict_usersite = dict(success=1, result=usersite_array)
        user_sites_data = dict_usersite["result"]
        site_id = [ids["site_id"] for ids in user_sites_data]
        #print(site_id)
        site_array = []
        for id in site_id:
            site_data = db.query(Site).filter(Site.id == id).all()
            for site in site_data:
                site_array.append(site.to_dict())

        json_site = json.dumps(site_array, indent=2)
        #print(json_site)
        return self.write(json_site)

    def post(self, args, *kwargs):
        site_btn_data = dict()
        site_btn_data = json_decode(self.request.body)
        BaseModule.__init__()
        db = BaseModule.db
        site = Site(
            name=site_btn_data.get("site_name"),
            url=site_btn_data.get("site_url")
        )
        user_id = site_btn_data.get("user_id")
        print(user_id)
        user_data_array = []
        user_data = db.query(User).filter(User.id == user_id).all()
        for data in user_data:
            user_data_array.append(data.to_dict())

        user = User(
            first_name=user_data_array[0]["first_name"],
            last_name=user_data_array[0]["last_name"],
            email=user_data_array[0]["email"],
        )
        usersite = UserSite(
            site=site,
            user_id=user_id
        )

        BaseModule.db.add(usersite)
        BaseModule.db.commit()
        BaseModule.db.refresh(usersite)
        __return_data = dict()
        __return_data['site_id'] = usersite.site_id
        return self.write(json_encode(__return_data))

    def delete(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        site_id = self.get_argument('site_id')
        BaseModule.__init__()
        db = BaseModule.db
        delete_data_array = []
        get_sitedata = db.query(UserSite).filter(site_id == UserSite.site_id).all()
        for site in get_sitedata:
            delete_data_array.append(site.to_dict())

        delete_site = dict(result=delete_data_array)
        usersite_id = delete_site['result'][0]["id"]
        _delete_from_usersite = db.query(UserSite).filter(usersite_id == UserSite.id).delete()
        _delete_from_site = db.query(Site).filter(site_id == Site.id).delete()
        BaseModule.db.commit()

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