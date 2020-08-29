from __future__ import print_function

import logging

import grpc

import http
import socket
import json

import usage_pb2
import usage_pb2_grpc

import csv
from flask import Flask, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_metrics_data(stub):
    response = stub.GetMeterUsage(usage_pb2.MeterUsageRequest())
    return response.data

def convert_to_json(metrics_data):
    data = metrics_data.split('\n')[1:-1]
    json_response = []
    # index = 0

    for line in data:
        components = line.split(',')
        json_response.append({"datetime": components[0], "meter_usage": components[1]})
        # index += 1
    
    return json.dumps(json_response)

@app.route('/')
def get_meter_usage_json():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = usage_pb2_grpc.MeterUsageStub(channel)
        metrics_data = get_metrics_data(stub)

        resp = make_response(convert_to_json(metrics_data))

        # resp.headers['Access-Control-Allow-Origin'] = '*'
        # resp.headers[]
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

# @app.after_request
# def apply_caching(response):
#     response.headers.set('Access-Control-Allow-Origin', '*')
#     response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
#     return response

# @app.route('/')
# def get_meter_usage_json():
#     with grpc.insecure_channel('localhost:50051') as channel:
#         stub = usage_pb2_grpc.MeterUsageStub(channel)
#         return get_metrics_data(stub)

if __name__ == '__main__':
    app.run()
    # run()