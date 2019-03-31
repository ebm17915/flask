from flask import Flask, jsonify, request
from google.oauth2 import service_account
from google.cloud import vision
from google.protobuf.json_format import MessageToDict
# from google.appengine.ext import webapp
# from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import json
import os
import io
import ast
# import webapp2

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./gcp_key.json"
credentials = service_account.Credentials.from_service_account_file("./gcp_key.json")
client = vision.ImageAnnotatorClient(credentials=credentials)
app = Flask(__name__)

@app.route("/api/gcm", methods=["POST"])
def home():
    data = json.loads(request.get_data().decode('utf8'))
    if not data:
        return jsonify({'failure':True})
    url = data['name']

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = url

    response = client.label_detection(image=image)
    labels = response.label_annotations
    response = MessageToDict(response, preserving_proto_field_name = True)
    return jsonify(response)

# application = webapp.WSGIApplication([('/api/gcm', Handler)],
#                                      debug=False)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
application = webapp.WSGIApplication([('/api/gcm', MainPage)],debug=True)

def main():
    application = webapp.WSGIApplication([('/foo', Handler)],
                                         debug=False)
    util.run_wsgi_app(application)

if __name__ == "__main__":
    main()