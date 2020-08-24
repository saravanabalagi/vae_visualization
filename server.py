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


@app.route('/upload_image', methods=['POST'])
def receive_image():
   # data = request.files['image']
   # img_input = np.array(Image.open(data))
   # return jsonify({ 'embedding': img_input.shape })
   return jsonify({ 'embedding': np.random.rand(10).tolist() })


@app.route('/upload_embedding', methods=['POST'])
def receive_embedding():
   embedding = request.json['embedding']
   # do stuff with embedding to get image
   img_output = np.random.rand(100, 100)
   img_output = img_as_ubyte(img_output)
   return serve_numpy_image(img_output)


@app.route("/")
def serve_root():
   return app.send_static_file('index.html')


if __name__ == '__main__':
   app.run()