import tornado.ioloop
import tornado.web
import mnist_loader
import network
import simplejson as json
import numpy as np
from PIL import Image

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class PostImageArray(tornado.web.RequestHandler):
    def set_default_headers(self):
        # print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        imgData = self.get_argument('image')
        imgJsonMap = json.loads(imgData)['data']
        width = int(self.get_argument('width'))
        height = int(self.get_argument('height'))
        img2DArray = []
        imageArray = []
        rgb_array = np.zeros((height, width, 3), 'uint8')
        for y in xrange(height):
            new = []
            for x in xrange(width):
                i = y*width + x
                ii = str(i*4).decode('utf-8')
                rgb_array[y, x, 0] = imgJsonMap[str(i*4+3).decode('utf-8')]
                rgb_array[y, x, 1] = imgJsonMap[str(i*4+3).decode('utf-8')]
                rgb_array[y, x, 2] = imgJsonMap[str(i*4+3).decode('utf-8')]
            # img2DArray.append(new)

        img = Image.fromarray(rgb_array)

        # img = Image.new('L', (width, height))
        # img.putdata(imageArray)
        size = 28, 28
        # img.thumbnail(size)
        img = img.resize(size)
        print img.size
        data = np.asarray(img)
        x1 = np.reshape(data[:, :, 0], (784, 1))
        x1 = x1.astype(float)
        x = [a/255 for a in x1]
        result = net.doRecognize(np.reshape(x, (784, 1)))
        print "result is %d" % result 
        img.save('my.png')
        # img.show()
        # img2dArray = np.reshape(imgArray, (width, height))
        # net.doRecognize(img2dArray)
        self.write(str(result))
        


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/image", PostImageArray),
    ])

if __name__ == "__main__":
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper();
    # imgTest = Image.fromarray(np.reshape(test_data[0], (28, 28)));
    net = network.Network([784, 30, 10])
    net.SGD(training_data, 10, 10, 3.0, test_data=test_data)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    print "start web service!"