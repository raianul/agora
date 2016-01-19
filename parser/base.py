import requests
from lxml import html

from lib import log


class BaseParser(object):

    def __init__(self, logger):
        self.logger = log.get_logger(logger)

    def make_call(self, call_type, **kwargs):
        try:
            response = requests.get(**kwargs) if call_type == 'get' else requests.post(**kwargs)
            self.logger.info("Fetching - %r" % response.url)
        except requests.RequestException as e:
            self.logger.exception('Exception %s' % e.__class__.__name__)
        else:
            return response

    def parse_html(self, content):
        return html.fromstring(content)

    def parse_node(self, response, node):
        return response.xpath(node)

    def is_parse_continue(self):
        raise NotImplemented

    def tracker(self):
        raise NotImplemented