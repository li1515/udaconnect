import json, os
import psycopg2
import logging

from kafka import KafkaConsumer
from schema import LocationSchema
from typing import Dict

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

# Configure logging level to INFO 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-consumer-saver")

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

messages = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])


def add_to_location(location):
    # Verify dictionary
    try:
        location_dict : Dict = json.loads(location)
    except:
        logger.warning(
            "Location format is non-dictionary: {0}".format(location))
        return

    # Validate the provided data
    validation_result: Dict = LocationSchema().validate(location_dict)
    if validation_result:
        logger.warning(
            "Unexpected data format in payload: {0}, reason: {1}".format(location, validation_result))
        return
    
    # insert data into database
    with psycopg2.connect(
        database = DB_NAME,
        user = DB_USERNAME,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    ) as conn:
        person_id = int(location_dict["person_id"])

        with conn.cursor() as cursor:
            try:
                query = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, location_dict["latitude"], location_dict["longitude"])
                cursor.execute(query)
            except Exception as e:
                logger.error("Unable to save location data to the database. reason: {1}".format(e))