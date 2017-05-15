import tornado.ioloop
import tornado.web
import tornado.websocket

class Home(tornado.web.RequestHandler):
    def get(self):
        with open('index.html', encoding="utf-8") as file:
            self.write(file.read())

class StaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

class ChatPage(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/")
    def post(self):
        with open('chat.html', encoding="utf-8") as file:
            self.write(file.read())

class Chat(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True


app = tornado.web.Application([
    (r"/", Home),
    (r"/assets/(.*)", StaticFileHandler, {'path': 'assets'}),
    (r"/%F0%9F%92%AC", ChatPage),
    (r"/ws", Chat)
])

app.listen(8888)
tornado.ioloop.IOLoop.current().start()
