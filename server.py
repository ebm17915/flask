from flask import Flask,render_template, jsonify, request
from google.oauth2 import service_account

import json
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./gcp_key.json"
import io
from google.cloud import vision
import ast
from google.protobuf.json_format import MessageToDict

credentials = service_account.Credentials.from_service_account_file("./gcp_key.json")
client = vision.ImageAnnotatorClient(credentials=credentials)

app = Flask(__name__)

@app.route('/api/gcm/', methods=["POST"])
def home():
    request = request.data
    if not request.photo:
        return jsonify({'failure':True})
    uri = request.photo

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    response = MessageToDict(response, preserving_proto_field_name = True)
    return jsonify(response)


if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3333, debug = True)