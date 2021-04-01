# A01053462
# Taylor Nguyen

import connexion
import yaml
import logging.config
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from likes import VideoLikes
from views import VideoViews
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import json
import os

# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
#with open('app_conf.yml', 'r') as f:
#    app_config = yaml.safe_load(f.read())

#with open('log_conf.yml', 'r') as f:
#    log_config = yaml.safe_load(f.read())
#    logging.config.dictConfig(log_config)

#logger = logging.getLogger('basicLogger')

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
        print("In Test Environment")
        app_conf_file = "/config/app_conf.yml"
        app_conf_file = "/config/log_conf.yml"
else:
        print("In Dev Environment")
        app_conf_file = "/config/app_conf.yml"
        app_conf_file = "/config/log_conf.yml"

with open(app_conf_file, 'r') as f:
        app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
        log_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % app_conf_file)

DB_ENGINE = create_engine(
    'mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password'] + '@' +
    app_config['datastore']['hostname'] + ':' + str(app_config['datastore']['port']) + '/' + app_config['datastore'][
        'db'])

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

MAX_EVENTS = 10
EVENT_FILE = "events.json"


def total_views(body):
    """count total view of video"""
    session = DB_SESSION()
    LIST_COUNT = []

    count_views = VideoViews(body['user_id'],
                             body['timestamp'],
                             body['views'])
    session.add(count_views)
    session.commit()
    session.close()

    logger.debug("Received event views request with a unique id of " + str(body["user_id"]))

    return NoContent, 201


def total_likes(body):
    """count total likes of video"""
    session = DB_SESSION()
    LIST_COUNT = []

    count_likes = VideoLikes(body['user_id'],
                             body['timestamp'],
                             body['likes'])
    session.add(count_likes)
    session.commit()
    session.close()

    logger.debug("Received event views request with a unique id of " + str(body["user_id"]))

    return NoContent, 201


def get_total_likes(timestamp):
    session = DB_SESSION()
    readings = session.query(VideoLikes).filter(VideoLikes.date_created >= timestamp)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for video likes changes after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200


def get_total_views(timestamp):
    session = DB_SESSION()

    readings = session.query(VideoViews).filter(VideoViews.date_created >= timestamp)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for video views changes after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "total_likes":
            total_likes(payload)
        elif msg["type"] == "total_views":
            total_views(payload)
    consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("taylornguyen1-Youtube-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    logger.info(
        "Hostname: " + str(app_config['datastore']['hostname']) + " Port: " + str(app_config['datastore']['port']))
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()

    app.run(port=8090)
