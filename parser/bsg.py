from lib.reporter import ReportGenerator
from base import BaseParser

class BSGParser(BaseParser, ReportGenerator):

    def __init__(self):
        self.key_node = '//tr[@class="sectiontableentry1"]'
        logger = 'BSGP'
        self.url = 'http://www.bsg.org.uk/events/index.html'
        super(BSGParser, self).__init__(logger)
        self._csv_header_columns = ["Date", "Title", "Location", "City", "Type"]

    def tracker(self):
        data = []
        response = self.make_call(call_type='post', url=self.url, data={'limit': 0})
        parse_html = self.parse_html(response.content)

        for resp in self.parse_node(parse_html, self.key_node):
            data.append({
                'date': resp.find('td[@headers="el_date"]/strong').text,
                'title': resp.find('td[@headers="el_title"]/a').text,
                'location': resp.find('td[@headers="el_location"]/a').text,
                'city': resp.find('td[@headers="el_city"]').text,
                'type': resp.find('td[@headers="el_category"]/a').text,
            })
        return data

    def prepare_data_dict(self, item):
        data = {
            "Date": item['date'],
            "Title": item['title'],
            "Location": item['location'],
            "City": item['city'],
            "Type": item['type'],
        }
        return data