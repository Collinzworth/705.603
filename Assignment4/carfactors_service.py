from flask import Flask
from flask import request
import os

from carsfactors import carsfactors

app = Flask(__name__)

# http://localhost:8786/infer?transmission=automatic&color=blue&odometer=12000&year=2020&bodytype=suv&price=20000

@app.route('/stats', methods=['GET'])
def getStats():
    print("here")
    return str(cf.model_stats())

@app.route('/infer', methods=['GET'])
def getInfer():
    args = request.args
    transmission = args.get('transmission')
    color = args.get('color')
    odometer = int(args.get('odometer'))
    year = int(args.get('year'))
    bodytype = args.get('bodytype')
    price = int(args.get('price'))
    return "Inference = " + str(cf.model_infer(transmission, color, odometer, year, bodytype, price))


if __name__ == "__main__":
    flaskPort = 8786
    cf = carsfactors()
    print('starting server...')
    app.run(port=flaskPort, debug=True, host='0.0.0.0')