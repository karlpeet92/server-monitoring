import hashlib
import tornado.web
from tornado.escape import json_decode
from tornroutes import route
from backend.modules.base_module import BaseModule
from backend.models.user import User
from backend.modules.config import Config
salt = Config.get_value("app", "password_salt")
BaseModule.__init__()
db = BaseModule.db


@route("/user(.*)")
class UserHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        form_data = dict()
        form_data = json_decode(self.request.body)
        print(form_data)
        user = User()
        form = form_data.get("form")

        # User register
        if form == "registration":
            input_email = form_data.get("email")
            emails = db.query(User).filter(User.email == input_email).all()

            if emails == [] :
                user.first_name = form_data.get("first_name")
                user.last_name = form_data.get("last_name")
                user.email = form_data.get("email")
                users_pass = form_data.get("password")

                pw_hash = self.create_hash(users_pass, salt)
                print(pw_hash)
                user.password = pw_hash

                self.set_secure_cookie("myCookie", Config.get_value("secrets", "cookie_secret"))

                BaseModule.db.add(user)
                BaseModule.db.commit()
                BaseModule.db.refresh(user)
                print("You created a new user!")
                return self.write(dict(success=1, user=user.to_dict()))
            elif emails != []:
                print("This user is already in use!")
                return self.write(dict(success=0, status="User is already in use!"))

        # User login and password check-up
        elif form == "login" or form == "password-check":
            self.set_header('Content-Type', 'application/json')
            login_email = form_data.get('email')
            login_password = form_data.get('password')
            _hashed_pw = pw_hash = self.create_hash(login_password, salt)

            user_array = []
            emails = db.query(User).filter(User.email == login_email).all()
            passwords = db.query(User.password).filter(User.email == login_email, User.password == _hashed_pw).all()

            if emails != []:
                for user in emails:
                    user_array.append(user.to_dict())
                user_id = user_array[0]["id"]

                if passwords != []:
                    return self.write(dict(success=1, email_pass=True, pass_pass=True, id=user_id))
                else:
                    print("Wrong password!")
                    return self.write(dict(success=0, email_pass=True, pass_pass=False))
            else:
                print("Email is not in use!")
                return self.write(dict(success=0, email_pass=False, pass_pass=False))


        # Password change
        else:
            self.set_header('Content-Type', 'application/json')
            user_email = form_data.get('email')

            user_data = db.query(User).filter(User.email == user_email).all()
            user_array = []
            for email in user_data:
                user_array.append(email.to_dict())

            user_id = user_array[0]['id']
            find_user = db.query(User).get(user_id)
            new_pass = form_data.get('password')
            pw_hash = self.create_hash(new_pass, salt)
            db.query(User).filter(User.email == user_email, User.password)
            find_user.password = pw_hash
            print('NEW password ' + pw_hash)

            BaseModule.db.commit()

    def create_hash(cls, password=None, salt=None):
        m = hashlib.sha512()
        m.update(salt.encode('utf-8'))
        m.update(password.encode('utf-8'))
        return m.hexdigest()

    def set_default_headers(self) -> None:
        # TODO :: CHECK THE DOMAINS

        self.set_header("Access-Control-Allow-Origin", "%s" % self.request.headers['Origin'])
        self.set_header('Access-Control-Allow-Credentials', "true")
        self.set_header('Access-Control-Allow-Methods', "GET, POST, PUT, OPTIONS")
        self.set_header('Access-Control-Expose-Headers', "Content-Type, X-Jwt")
        self.set_header('Access-Control-Allow-Headers',
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control, X-Jwt")
        self.set_header('Access-Control-Max-Age', 600)

    def check_xsrf_cookie(self) -> None:
        return True

    def options(self, *args, **kwargs):
        pass