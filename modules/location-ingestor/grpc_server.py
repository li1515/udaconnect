import os
import grpc
import location_pb2
import location_pb2_grpc
import logging
import json

from kafka import KafkaProducer
from concurrent import futures

# Configure logging level to INFO 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-ingestor")

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

logger.info("Topic: {0}, Server: {1}".format(TOPIC_NAME, KAFKA_SERVER))
print("Starting gRPC server on port 5005...")


producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])

def publish_location(location_data):

    print("Non Encrypted Data, {0}, to send to kafka.".format(location_data))

    encoded_data = json.dumps(location_data).encode('utf-8')
    print(" utf-8 Data, {0}, to be sent to kafka.".format(encoded_data))
    producer.send(TOPIC_NAME, encoded_data)
    producer.flush()

    logger.info("Published data, {0}, to kafka successful.".format(location_data))


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        print("Received a message!")
        request_value = {
            'person_id': request.person_id,
            'longitude': request.longitude,
            'latitude': request.latitude
        }
        
        publish_location(request_value)
        
        return location_pb2.LocationMessage(**request_value)

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("Starting gRPC server on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()

# Keep thread alive
server.wait_for_termination()