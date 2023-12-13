from flask import Flask, send_from_directory, abort
from flask import request
from remix_generator import remix_generator
from dataset_generator import generate_dataset
import os


app = Flask(__name__)


@app.route('/generate_dataset', methods=['GET'])
def gen_dataset():

    args = request.args
    num_samples = args.get('num_samples')

    generated_dataset = generate_dataset(num_samples)
    generated_dataset.create_dataset()
    generated_dataset.fit_nn("nn_model.pkl")
    generated_dataset.create_pca_dataset(20)
    generated_dataset.fit_nn("pca_nn_model.pkl")

    return "Dataset Generated!"

@app.route('/listcwd', methods=['GET'])
def listcwd():
    return str(os.listdir(os.getcwd()))

@app.route('/getcwd', methods=['GET'])
def getcwd():
    return str(os.getcwd())


@app.route('/generate', methods=['GET'])
def getInfer():
    args = request.args
    file_name = args.get('file_name')
    jump_rate = float(args.get('jump_rate'))
    num_beats = int(args.get('num_beats'))
    faded = bool(args.get('faded'))

    rg.generate_remix(file_name, jump_rate, num_beats, faded)

    return_str = "Remix generated at " + os.path.join("/generated_outputs", file_name)

    return str(return_str)

if __name__ == "__main__":
    flaskPort = 8786
    rg = remix_generator()
    print('starting server...')
    app.run(host = '0.0.0.0', port = flaskPort)

