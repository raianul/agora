import requests
from lxml import html

import log


class BaseParser(object):

    def __init__(self, logger):
        self.logger = log.get_logger(logger)

    def make_call(self, call_type, **kwargs):
        try:
            response = requests.get(**kwargs) if call_type == 'get' else requests.post(**kwargs)
            self.logger.info("Fetching - %r" % response.url)
            response.raise_for_status()
        except (requests.HTTPError, requests.RequestException) as e:
            self.logger.exception('Exception %s' % e.__class__.__name__)
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


class RCGPParser(BaseParser):

    def __init__(self):
        self.key_node = '//div[@class="search-result"]'
        logger = 'RCGP'
        self.url = 'http://www.rcgp.org.uk/learning/events-search-results.aspx?CurrentPage=%r'
        super(RCGPParser, self).__init__(logger)

    def is_parse_continue(self, content, count):
        try:
            response = self.parse_node(content, '//div[@class="pagination centered"]')[0]
        except KeyError:
            return False
        else:
            current_page = int(response.find('ul/li[@class="active"]').text)
            if current_page != count:
                return False

        return True

    def tracker(self):
        count = 1
        data = []

        while True:
            url = self.url % count
            response = self.make_call(call_type='get', url=url)
            parse_html = self.parse_html(response.content)
            parse_continue = self.is_parse_continue(parse_html, count)
            if not parse_continue:
                break

            for resp in self.parse_node(parse_html, self.key_node):
                data.append({
                    'title': resp.find('h3/a').text,
                    'summary': resp.find('div[@class="summary-col"]/p').text,
                })
        return data


class BSGParser(BaseParser):

    def __init__(self):
        self.key_node = '//tr[@class="sectiontableentry1"]'
        logger = 'BSGP'
        self.url = 'http://www.bsg.org.uk/events/index.html'
        super(BSGParser, self).__init__(logger)
