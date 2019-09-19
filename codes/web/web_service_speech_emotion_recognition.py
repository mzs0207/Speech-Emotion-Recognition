#!/usr/bin/env python
# coding:utf8
"""

"""
from flask import Flask
from flask import request, jsonify
import json
from codes.model.Utils import load_model
from codes.model.SER import Predict

model = load_model(load_model_name="LSTM_OPENSMILE", model_name="lstm" )


app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    """

    :return:
    """
    return "hell world"


@app.route('/speech_emotion_recognition', methods=["POST"])
def speech_emotion_recognition():
    """

    :return:
    """
    request_str = request.data
    json_data = json.loads(request_str)
    print(json_data)
    predict_result = Predict(model, model_name="lstm", file_path=json_data['file_name'], feature_method='o')

    response_data = {"code": 0, "result": predict_result}
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9600, debug=True)