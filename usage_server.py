# inspired from examples found at https://www.grpc.io/docs/languages/python/

import grpc
import csv
import os

from concurrent import futures
import usage_pb2
import usage_pb2_grpc

class UsageServer(usage_pb2_grpc.MeterUsageServicer):
     METER_FILE_PATH = "data/meterusage.csv"

     def GetMeterUsage(self, request, context):
        if not os.path.isfile(self.METER_FILE_PATH):
            return usage_pb2.MeterUsageResponse(data=None)
        
        file = open(self.METER_FILE_PATH, 'r')
        file_content=file.read();
        
        return usage_pb2.MeterUsageResponse(data=file_content)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usage_pb2_grpc.add_MeterUsageServicer_to_server(
        UsageServer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()