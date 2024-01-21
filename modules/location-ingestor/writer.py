import json
import grpc

import location_pb2
import location_pb2_grpc


print("Sending sample location...")

channel = grpc.insecure_channel("127.0.0.1:5005")
stub = location_pb2_grpc.LocationServiceStub((channel))

#Creating locations
location_1 = location_pb2.LocationMessage(
    person_id=1,
    latitude=48.113704,
    longitude=11.637020
)


location_2 = location_pb2.LocationMessage(
    person_id=2,
    latitude=-48.138397,
    longitude=11.573719
)

#Sending locations to server
stub.Create(location_1)
stub.Create(location_2)