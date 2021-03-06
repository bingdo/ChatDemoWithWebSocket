#-*- coding:utf-8 -*-
from tornado import web, websocket, ioloop
import json
from tornado.options import options

options.define("port", default=8888, type=int)

cl = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html");

class SocketHandler(websocket.WebSocketHandler):
    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

    def on_message(self, message):
        #data = {"message": message}
        #data = json.dumps(data, ensure_ascii=False)
        print("Client(%s) said: %s" % (cl.index(self), message))
        for c in cl:
            if c != self:
                c.write_message(message)

app = web.Application([
    (r"/", IndexHandler),
    (r"/ws", SocketHandler),
])

if __name__ == "__main__":
    app.listen(options.port)
    ioloop.IOLoop.instance().start()




