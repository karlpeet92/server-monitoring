import tornado.web
import tornado.ioloop
import mysql.connector


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world!!")

class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/servermonitor",staticRequestHandler)
    ])



    app.listen(9001)
    print("I'm listening on port 9001")
    tornado.ioloop.IOLoop.current().start()