import argparse
import os
import io
from typing import Union

from wsgiref.handlers import format_date_time
import argparse
import torch
import numpy as np
import os
from PIL import Image

from flask import Flask, send_file, jsonify, request, send_from_directory

HOST = 'localhost'
PORT = 5000
VAE_VISUALIZATION_CLIENT_PATH = 'path_to_repo/public'
assert os.path.isdir(VAE_VISUALIZATION_CLIENT_PATH), f'{VAE_VISUALIZATION_CLIENT_PATH} does not exist'
app = Flask(__name__, static_url_path='', static_folder=VAE_VISUALIZATION_CLIENT_PATH)

paths = {
    'images': '/images',
    'embeddings': '/embeddings',
    'decoded_img': '/decoded_img',
}


@app.route(paths['images'] + '/', defaults={'path': ''}, methods=['GET'])
@app.route(paths['images'] + '/<path:path>', methods=['GET'])
def serve_files(path):
    required_path = os.path.join(img_dir, path)
    if os.path.exists(required_path):
        if os.path.isdir(required_path): # for directories
            files = os.listdir(required_path)
            files.sort()
            files_json = [get_json(os.path.join(required_path, f)) for f in files]
            return jsonify(files_json)
        else: # for files
            if 'info' in request.args:
                return get_json(required_path)
            elif 'processed' in request.args:
                img_formats = ['.png', '.jpg', '.jpeg']
                ext = os.path.splitext(required_path)[-1]
                if ext not in img_formats:
                    return jsonify({'error': f'file extension {ext} not in {img_formats}, file {required_path}'})
                transform = experiment.data_transforms()
                transform_inverse = experiment.data_transforms_inverse()
                img = Image.open(required_path)
                img_transformed = transform(img)
                img_transformed_inverse = transform_inverse(img_transformed)
                return serve_img(img_transformed_inverse)
            else:
                return send_from_directory(img_dir, path)
    return jsonify({'error': f'dir {path} not found in images; try /images to get the list of all files'})


@app.route(paths['embeddings'], methods=['POST'])
def send_embedding_for_custom_img():
    data = request.files['image']
    img = np.fromfile(data, np.uint8)
    img = Image.fromarray(img, mode='RGB')
    transform = experiment.data_transforms()
    img_transformed = transform(img)
    imgs_torch = torch.stack([img_transformed]).to(device)
    embeddings = experiment.model.encode(imgs_torch)
    return jsonify({ 'embedding': embeddings.cpu().detach().numpy()[0].tolist() })


@app.route(paths['embeddings'] + '/<path:path>', methods=['GET'])
def send_embedding_for_img(path):
    required_path = os.path.join(img_dir, path)
    if os.path.exists(required_path):
        img = Image.open(required_path)
        transform = experiment.data_transforms()
        img_transformed = transform(img)
        imgs_torch = torch.stack([img_transformed]).to(device)
        embedding, log_var = experiment.model.encode(imgs_torch)
        return jsonify({ 'embedding': embedding.cpu().detach().numpy()[0].tolist() })
    return jsonify({'error': f'file images/{path} not found'})


@app.route(paths['decoded_img'], methods=['POST'])
def send_decoded_img():
    embedding = request.json['embedding']
    embedding = np.array(embedding)
    embeddings = torch.FloatTensor(embedding).unsqueeze(0).to(device)
    imgs = experiment.model.decode(embeddings)
    imgs = imgs.cpu().detach()
    transform_inverse = experiment.data_transforms_inverse()
    imgs = [transform_inverse(i) for i in imgs]
    img = imgs[0]
    return serve_img(img)


@app.route('/paths', methods=['GET'])
def serve_paths():
    paths_extra = {'ckpt_path': ckpt_path, 'img_dir_path': img_dir}
    paths_to_send = {**paths, **paths_extra}
    return jsonify(paths_to_send)


@app.route("/", methods=['GET'])
def serve_root():
    return app.send_static_file('index.html')


def serve_img(img: Union[Image.Image, np.ndarray]):
    try:
        if isinstance(img, np.ndarray):
            assert len(img.shape) == 3, f'img should be 3 dimensions, given {img.shape}'
            img = Image.fromarray(img, mode='RGB')
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/JPG')
    except:
        return jsonify({'error': f'could not convert image'})


def get_json(fpath):
    ftype = 'others'
    if os.path.isdir(fpath): ftype = 'directory'
    elif os.path.isfile(fpath): ftype = 'file'

    stats = {
        'name': os.path.basename(fpath),
        'mtime': format_date_time(os.path.getmtime(fpath)),
        'type': ftype,
    }

    if ftype == 'file':
        stats['size'] = os.path.getsize(fpath)
    return stats


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ckpt_path', help='path to checkpoint file')
    parser.add_argument('img_dir', help='path to dir containing imgs')
    args = parser.parse_args()

    ckpt_path = args.ckpt_path
    img_dir = args.img_dir
    exp_path = os.path.dirname(os.path.dirname(ckpt_path))

    # Load params, model and ptmodule_instance
    model = your_model(model_params)
    experiment = PytorchLightningModule.load_from_checkpoint(ckpt_path, vae_model=model, params=config)
    experiment.freeze()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    torch.set_grad_enabled(False)

    app.run(host=HOST, port=PORT)
