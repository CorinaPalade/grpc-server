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

    for line in data:
        components = line.split(',')
        json_response.append({"datetime": components[0], "meter_usage": components[1]})
    
    return json.dumps(json_response)

@app.route('/')
def get_meter_usage_json():
    # inspired from examples found at https://www.grpc.io/docs/languages/python/

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = usage_pb2_grpc.MeterUsageStub(channel)
        metrics_data = get_metrics_data(stub)

        resp = make_response(convert_to_json(metrics_data))

        return resp

if __name__ == '__main__':
    app.run()