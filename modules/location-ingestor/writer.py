import json
import grpc

import location_pb2
import location_pb2_grpc


print("Sending sample locations...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

#Creating location payload
location_1 = location_pb2.LocationMessage(
    person_id=1,
    latitude=48.113704,
    longitude=11.637020
)

#Sending locations to server
response = stub.Create(location_1)

print("Response from gRPC server: {0}".format(response))