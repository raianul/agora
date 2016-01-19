import requests
from lxml import html


class BaseParser(object):

    def make_call(self, call_type, **kwargs):
        try:
            response = requests.get(**kwargs) if call_type == 'get' else requests.post(**kwargs)
            response.raise_for_status()
        except (requests.HTTPError, requests.RequestException) as e:
            raise
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