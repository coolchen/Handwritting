import tornado.ioloop
import tornado.web
import mnist_loader
import network
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class PostImageArray(tornado.web.RequestHandler):
    def post(self):
        imgArray = self.get_argument('image')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/image", PostImageArray),
    ])

if __name__ == "__main__":
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper();
    net = network.Network([784, 30, 10])
    net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()