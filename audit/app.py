# A01053462
# Taylor Nguyen

import connexion
import yaml
import logging.config
from connexion import NoContent
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
# from base import Base
# from likes import VideoLikes
# from views import VideoViews
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import json
from flask_cors import CORS, cross_origin

# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

#DB_ENGINE = create_engine(
#    'mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password'] + '@' +
#    app_config['datastore']['hostname'] + ':' + str(app_config['datastore']['port']) + '/' + app_config['datastore'][
#        'db'])

# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

MAX_EVENTS = 10
EVENT_FILE = "events.json"


def get_total_likes(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving new likes at index %d" % index)
    try:
        count = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg["type"] == "total_likes":
                if count == index:
                    return msg["payload"], 201
                count += 1
    except:
        logger.error("No more messages found")

    logger.error("Could not find new likes at index %d" % index)
    return {"message": "Not Found"}, 404


def get_total_views(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving new views at index %d" % index)
    try:
        count = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg["type"] == "total_views":
                if count == index:
                    return msg["payload"], 201
                count += 1
    except:
        logger.error("No more messages found")

    logger.error("Could not find new views at index %d" % index)
    return {"message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("taylornguyen1-Youtube-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    logger.info(
        "Hostname: " + str(app_config['datastore']['hostname']) + " Port: " + str(app_config['datastore']['port']))
    app.run(port=8070)
