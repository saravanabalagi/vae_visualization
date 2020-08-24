from flask import Flask, send_file, jsonify, request
from skimage import img_as_ubyte
from PIL import Image
import numpy as np
import io

app = Flask(__name__, static_url_path='', static_folder='public')


def serve_numpy_image(numpy_arr):
   # convert numpy array to PIL Image
   pil_img = Image.fromarray(numpy_arr.astype('uint8'))

   # write to Byte Stream
   img_io = io.BytesIO()
   pil_img.save(img_io, 'PNG')

   img_io.seek(0)
   return send_file(img_io, mimetype='image/PNG')


@app.route('/upload', methods=['POST'])
def receive_image():
   data = request.files['file']
   return jsonify({"status":"ok"})


@app.route('/hello_post', methods=['POST'])
def hello_post():
   data = request.json
   return jsonify({'status': data['hello']})


@app.route('/get_image')
def serve_image():
   img = np.random.rand(100, 100)
   img = img_as_ubyte(img)
   return serve_numpy_image(img)


@app.route("/")
def serve_root():
   return app.send_static_file('index.html')


if __name__ == '__main__':
   app.run()