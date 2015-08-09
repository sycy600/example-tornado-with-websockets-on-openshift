import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.escape
import tornado.httpserver

web_socket_connections = []
log_max_last_messages = 20
last_messages = []

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate(last_messages=last_messages))

class ChatWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        web_socket_connections.append(self)

    def on_message(self, message):
        if last_messages and (len(last_messages) == log_max_last_messages):
            del last_messages[0]
        last_messages.append(message)
        for web_socket_connection in web_socket_connections:
            web_socket_connection.write_message(tornado.escape.xhtml_escape(message))

    def on_close(self):
        web_socket_connections.remove(self)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", ChatWebSocketHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"})
])

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
