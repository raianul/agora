import csv
import abc
from StringIO import StringIO

import requests

import log
from settings import EMAIL_INFO
from email_tools import EmailConnection, Email


class ReportGenerator(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.logger = log.get_logger('ReportGenerator')
        self._csv_header_columns = ["Title", "Summary"]

    @property
    def csv_header_columns(self):
        return self._csv_header_columns

    @csv_header_columns.setter
    def csv_header_columns(self, columns):
        self._csv_header_columns = columns

    def get_dict_writer_and_csv_file(self):
        csv_file = StringIO()
        csv_dict_writer = csv.DictWriter(csv_file, fieldnames=self.csv_header_columns)
        return csv_dict_writer, csv_file

    @staticmethod
    def get_unicode_dict(data):
        return {str(key): unicode(value).encode('utf8') for key, value in data.items()}

    def write_csv_data_rows(self, csv_dict_writer, items):
        for item in items:
            data = self.prepare_data_dict(item)
            csv_dict_writer.writerow(self.get_unicode_dict(data))
        self.logger.info("Finished preparing contents")

    @abc.abstractmethod
    def prepare_data_dict(self, image_license, forked_guid, publish_event, organization_maps):
        """Returns data for each row"""

    def prepare_content(self, data):
        csv_dict_writer, csv_file = self.get_dict_writer_and_csv_file()
        csv_dict_writer.writeheader()
        if not data:
            self.logger.info("No data found !")
            return None

        self.write_csv_data_rows(csv_dict_writer, data)
        return csv_file.getvalue()

    def prepare_report(self, data):
        self.logger.info("Preparing Content as CSV")
        filename = "list.csv"
        content = self.prepare_content(data) if len(data) else None
        return content, filename

    def send_report(self, content, filename):
        connection = EmailConnection(EMAIL_INFO['sender'], EMAIL_INFO['password'])
        message = 'Data Scrapping from %r' % self.url
        email = Email(from_=EMAIL_INFO['user_name'],
            to=EMAIL_INFO['receiver'],
            subject=EMAIL_INFO['subject'],
            message=message,
            attachments=None if content is None else {filename: content})

        self.logger.info("Sending Email...")
        connection.send(email)

    def report(self, data):
        content, filename = self.prepare_report(data)
        self.send_report(content, filename)
        self.logger.info("---Done---")
