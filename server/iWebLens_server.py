from flask import Flask, jsonify, request
import json
import base64

import object_detection_modified


app = Flask(__name__)

# use for debugging. need to comment
# app.config["DEBUG"] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/")
def hello():
    return "Welcome to iWebLens! By Hao Xu (FIT5225) \n"


@app.route("/api/object_detection", methods=['POST'])
def do_detection():
    image_json = json.loads(request.json)
    image_id = image_json['id']
    image_file = base64.b64decode(image_json['image'])
    returned_dict = object_detection_modified.detection(image_file, image_id)
    response = jsonify(returned_dict)

    return response


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0')
