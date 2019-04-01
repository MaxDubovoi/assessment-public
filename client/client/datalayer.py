import logging
import requests as r

import pandas as pd

from client.log import get_logger
from client.config import Config

LOG = get_logger('client', 'client.log', level=logging.INFO)


class DataLayer:
    """
    Handler to make requests.
    Expects a JSON response from the server.
    """

    def __init__(self):
        self.config = Config()
        LOG.info("Building the request module.")

    def execute(self):
        LOG.info(self.test_endpoint())
        response = self.send_data()
        LOG.info(self.parse_result(response))

    def test_endpoint(self):
        LOG.info(str(self.config.url))
        return r.get(str(self.config.url))

    def send_data(self):
        with open(str(self.config.data), 'rb') as f:
            LOG.info(f)
            return r.post(
                str(self.config.url),
                files={'file': (str(self.config.data), f, 'text/csv', {'Expires': '0'})})

    def parse_result(self, response):
        return response.json()
