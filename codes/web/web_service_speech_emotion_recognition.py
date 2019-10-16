#!/usr/bin/env python
# coding:utf8
"""

"""
from flask import Flask
from flask import request, jsonify
import json
from codes.model.Utils import load_model
from codes.model.SER import Predict
from codes.model.Config import Config
import requests
import os
import traceback


def download_file(url, pre_directory=Config.TEST_DATA_PATH, user_name='mirrelep_nginx', passwd='@Pxw19D#'):
    """

    :param url:
    :param pre_directory:
    :param user_name
    :param passwd
    :return:
    """
    file_name = str(url).split('/')[-1]
    r = requests.get(url, auth=(user_name, passwd),stream=True)
    if r.status_code != 200:
        raise Exception("An error was found while downloading the wav file. status code:{0} reason:{1}".format(r.status_code,
                                                                                                               r.reason))
    with open(os.path.join(pre_directory, file_name), 'wb') as w:
        for chunk in r.iter_content(chunk_size=1024):
            w.write(chunk)
    return file_name


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
    response_data = {}
    response_header = {
        'traceId': '0',
        'code': 0,
        'error': '',
        'msg': 'success',
        'msgtype': 1
    }
    try:
        json_data = json.loads(request_str)
        response_header['traceId'] = json_data['head']['traceId']
        print(json_data)
        file_name = download_file(json_data['mediaUrl'])
        predict_result = Predict(model, model_name="lstm", file_path=file_name, feature_method='o', delete=True)
        response_data["body"] = predict_result

    except Exception as e:
        response_header['code'] = 1
        response_header['error'] = str(e)
        response_header['msg'] = ""
        response_data['body'] = {}
        traceback.print_exc()
    response_data['head'] = response_header
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9600, debug=True)
    #download_file('http://119.23.74.118:8080/file/201_sad.wav')