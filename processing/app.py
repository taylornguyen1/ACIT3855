# A01053462
# Taylor Nguyen
# I added the num_comments as another json stat

import connexion
import os
import yaml
import logging.config
import json
from apscheduler.schedulers.background import BackgroundScheduler
from connexion import NoContent
import datetime
import requests
from flask_cors import CORS, cross_origin
import os
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
        logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % app_conf_file)


def get_stats():
    logger.info("Getting stats starting")
    if os.path.exists(app_config["datastore"]["filename"]):
        f = open(app_config["datastore"]["filename"], 'r')
        file = f.read()
        data = json.loads(file)
        f.close()
    else:
        logger.error("Stats do not exist")
        return NoContent, 404
    logger.debug(data)
    logger.info("Request done")
    return data, 200


def populate_stats():
    logger.info("Start periodic processing")
    if os.path.exists(app_config["datastore"]["filename"]):
        f = open(app_config["datastore"]["filename"], 'r')
        file = f.read()
        data = json.loads(file)
        f.close()
    else:
        data = {
            "timestamp": "2021-01-01 03:44:42.797237-08:00",
            "views": 0,
            "likes": 0,
            "num_comments": 0
        }

    now_time = str(datetime.datetime.now())
    json_time = data["timestamp"]

    view_query = requests.get(app_config["eventstore"]["url"] + "/get/views?timestamp=" +
                              str(json_time))
    if view_query.status_code == 200:
        logger.info("The number of view events received are: " + str(len(view_query.json())))
    else:
        logger.error("Error: " + str(view_query))

    like_query = requests.get(app_config["eventstore"]["url"] + "/get/likes?timestamp=" +
                              str(json_time))
    if like_query.status_code == 200:
        logger.info("The number of like events received are: " + str(len(like_query.json())))
    else:
        logger.error("Error: " + str(like_query))

    comment_query = requests.get(app_config["eventstore"]["url"] + "/get/likes?timestamp=" +
                              str(json_time))
    if comment_query.status_code == 200:
        logger.info("The number of comments events received are: " + str(len(comment_query.json())))
    else:
        logger.error("Error: " + str(comment_query))

    data["timestamp"] = now_time
    data["views"] = data["views"] + len(view_query.json())
    data["likes"] = data["likes"] + len(like_query.json())
    data["num_comments"] = data["num_comments"] + len(comment_query.json())

    with open(app_config["datastore"]["filename"], 'w') as f:
        f.write(json.dumps(data))
        f.close()

    logger.debug("Updated stats: " + json.dumps(data))
    logger.info("Periodic processing has ended")


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("taylornguyen1-Youtube-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)
