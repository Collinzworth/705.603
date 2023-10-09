from flask import Flask
from flask import request
from Object_Detection import ObjectDetection
import os


app = Flask(__name__)


# Use postman to generate the post with a graphic of your choice
@app.route('/post', methods=['POST'])
def detection():

    args = request.args
    name = args.get('name')
    location = args.get('description')
    imagefile = request.files.get('imagefile', '')

    print("Image: ", imagefile.filename)
    imagefile.save(imagefile.filename)
    img = ot.read_image(imagefile.filename)


    # The file is now downloaded and available to use with your detection class
    detections = ot.determine_object(img)

    detect_str = ""
    for i, detection in enumerate(detections):
        detect_str = detect_str + f'Object {i}: {detection[0]} with confidence of {detection[1]:.2f}\n'

    return detect_str

if __name__ == "__main__":
    flaskPort = 8786
    ot = ObjectDetection()
    print('starting server...')
    app.run(host = '0.0.0.0', port = flaskPort)

