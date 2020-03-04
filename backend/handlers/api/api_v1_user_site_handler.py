import json

import tornado.web
from tornroutes import route

from backend.models.site import Site
from backend.models.user_site import UserSite
from backend.modules.base_module import BaseModule


@route("/api/v1/user-site/?(.*)?")
class APIV1UserSiteHandler(tornado.web.RequestHandler):
    _VIEW_TITLE_ = "UserSite"

    def get(self, args, *kwargs):
        self.set_header('Content-Type', 'application/json')
        user_id = self.get_argument("user_id")
        usersite_array = []
        if user_id:
            bmdb = BaseModule.db
            user_sites = bmdb.query(UserSite).filter(UserSite.user_id==user_id).all()
            for usersite in user_sites:
                usersite_array.append(usersite.to_dict()) 
        
        dict_usersite = dict(success=1, result=usersite_array) 
        site_id = dict_usersite['result'][0]['site_id']
                
        site_array = []
        site_data = bmdb.query(Site).filter(Site.id==site_id).all()
        for site in site_data:
            site_array.append(site.to_dict())

        json_site = json.dumps(site_array, indent=2)
        print(json_site)
        return self.write(json_site)