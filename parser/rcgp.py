from lib.reporter import ReportGenerator
from base import BaseParser

class RCGPParser(BaseParser, ReportGenerator):

    def __init__(self):
        self.key_node = '//div[@class="search-result"]'
        logger = 'RCGP'
        self.url = 'http://www.rcgp.org.uk/learning/events-search-results.aspx?CurrentPage=%r'
        super(RCGPParser, self).__init__(logger)
        self._csv_header_columns = ["Title", "Summary"]

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
            count +=1
        return data

    def prepare_data_dict(self, item):
        data = {
            "Title": item['title'],
            "Summary": item['summary'],
        }
        return data