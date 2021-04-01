# A01053462
# Taylor Nguyen

import connexion
import yaml
from connexion import NoContent
import requests
import logging.config
import datetime
import json
from pykafka import KafkaClient
import os

MAX_EVENTS = 10
EVENT_FILE = "events.json"

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


def total_views(body):
    """count total view of video"""
    LIST_COUNT = []

    read_file = open(EVENT_FILE, "r")
    readlines = read_file.readlines()

    for lines in readlines:
        LIST_COUNT.append(lines)

    LIST_COUNT.append(str(body) + "\n")

    if len(LIST_COUNT) > MAX_EVENTS:
        LIST_COUNT.pop(0)
        new_file = open(EVENT_FILE, "w")
        for line in LIST_COUNT:
            new_file.write(str(line))
        new_file.close()
    else:
        new_file = open(EVENT_FILE, "w")
        for line in LIST_COUNT:
            new_file.write(str(line))
        new_file.close()

    client = KafkaClient(hosts="%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"]))
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "total_views",
           "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    status_code = 201

    # status_code = requests.post('http://localhost:8090/tracker/views', json=body).status_code

    logger.info("Returned event views request with a unique id of" + str(body["user_id"]))
    logger.info("Returned event views response (Id:" + str(body["user_id"]) + ") with status" + str(status_code))

    return NoContent, 201


def total_likes(body):
    """count total likes of video"""
    LIST_COUNT = []

    read_file = open(EVENT_FILE, "r")
    readlines = read_file.readlines()

    for lines in readlines:
        LIST_COUNT.append(lines)

    LIST_COUNT.append(str(body) + "\n")

    if len(LIST_COUNT) > MAX_EVENTS:
        LIST_COUNT.pop(0)
        new_file = open(EVENT_FILE, "w")
        for line in LIST_COUNT:
            new_file.write(str(line))
        new_file.close()
    else:
        new_file = open(EVENT_FILE, "w")
        for line in LIST_COUNT:
            new_file.write(str(line))
        new_file.close()

    client = KafkaClient(hosts="%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"]))
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "total_likes",
           "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    status_code = 201

    # status_code = requests.post('http://localhost:8090/tracker/likes', json=body).status_code

    logger.info("Returned event likes request with a unique id of" + str(body["user_id"]))
    logger.info("Returned event likes response (Id:" + str(body["user_id"]) + ") with status" + str(status_code))

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("taylornguyen1-Youtube-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
