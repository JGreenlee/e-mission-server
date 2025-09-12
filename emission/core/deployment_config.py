import os
import logging
import json
import requests

STUDY_CONFIG = os.getenv('STUDY_CONFIG', "stage-program")
DOWNLOAD_URL = "https://raw.githubusercontent.com/e-mission/nrel-openpath-deploy-configs/main/configs/%s.nrel-op.json"
DEV_DOWNLOAD_URL = "http://localhost:9090/configs/%s.nrel-op.json" # use this if testing with locally hosted configs

deployment_config = None

def get_deployment_config(default=None):
    """
    Fetch the deployment config from the GitHub repository

    :param default: Default value to return if the config cannot be fetched.
    :return: Deployment config dictionary or default value.
    """
    global deployment_config
    if deployment_config is not None:
        logging.debug("Returning cached deployment config for %s at version %s" % (STUDY_CONFIG, deployment_config['version']))
        return deployment_config
    logging.debug("No cached deployment config for %s, downloading from server" % STUDY_CONFIG)
    download_url = DEV_DOWNLOAD_URL % (STUDY_CONFIG)
    logging.debug("About to download config from %s" % download_url)
    r = requests.get(download_url)
    if r.status_code != 200:
        logging.debug(f"Unable to download study config, status code: {r.status_code}")
        return default
    else:
        deployment_config = json.loads(r.text)
        logging.debug(f"Successfully downloaded config with version {deployment_config['version']} "\
            f"for {deployment_config['intro']['translated_text']['en']['deployment_name']} "\
            f"and data collection URL {deployment_config['server']['connectUrl']}")
        return deployment_config
