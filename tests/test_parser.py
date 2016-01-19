import httpretty
import requests
from nose.tools import eq_, raises

from parser.base import BaseParser

URL = 'http://www.rcgp.org.uk/learning/events-search-results.aspx?CurrentPage=1'
HEADERS = {'content-type': 'text/html; charset=utf-8', 'Content-Length': '36551',}
PAYLOAD = "<head></head><body><h1>This is Test Data</h1></body>"


def raise_connection_timeout(request, uri, headers):
    request.url = uri
    raise requests.Timeout(request=request)


def setup_module():
    httpretty.enable()


def teardown_module():
    httpretty.disable()


def test_make_call_as_get_request():
    httpretty.register_uri(httpretty.GET, URL, body=PAYLOAD, status=200)
    parser = BaseParser('test')
    response = parser.make_call(call_type='get', url=URL, headers=HEADERS)
    eq_(PAYLOAD, response.content)


def test_make_call_as_post_request():
    httpretty.register_uri(httpretty.POST, URL, body=PAYLOAD, status=200)
    parser = BaseParser('test')
    response = parser.make_call(call_type='post', url=URL, headers=HEADERS)
    eq_(PAYLOAD, response.content)
