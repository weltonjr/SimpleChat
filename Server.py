import tornado.ioloop
import tornado.web
import tornado.websocket

Users = []

class Home(tornado.web.RequestHandler):
    def get(self):
        with open('index.html', encoding="utf-8") as file:
            self.write(file.read())

class ChatPage(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/")
    def post(self):
        with open('chat.html', encoding="utf-8") as file:
            self.write(file.read())

class ChatSend(tornado.web.RequestHandler):
    def post(self):
        for user in Users:
            user.write_message("self.request.body")

class Chat(tornado.websocket.WebSocketHandler):
    def open(self):
        print('open')
        Users.append(self)

    def on_message(self, message):
        print(message)
        for item in Users:
            item.write_message(message)

    def on_close(self):
        print('closed')
        Users.remove(self)

    def check_origin(self, origin):
        return True

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", Home),
        (r"/assets/(.*)", tornado.web.StaticFileHandler, {'path': 'assets'}),
        (r"/%F0%9F%92%AC", ChatPage),
        (r"/chat", ChatSend),
        (r"/ws", Chat)
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
