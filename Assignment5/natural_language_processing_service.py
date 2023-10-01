from flask import Flask
from flask import request
import os

from natural_language_processing import Sentiment

app = Flask(__name__)

# http://localhost:8786/infer?sentence="This place is really bad absolutly the worse"
# http://localhost:8786/infer?sentence="fantastic, great place I love it"

@app.route('/stats', methods=['GET'])
def getStats():
    return str(st.model_stats())

@app.route('/infer', methods=['GET'])
def getInfer():
    args = request.args
    sentence = args.get('sentence')
    return str(st.model_infer(sentence))

if __name__ == "__main__":
    flaskPort = 8786
    st = Sentiment()
    print('starting server...')
    app.run(host = '0.0.0.0', port = flaskPort)

