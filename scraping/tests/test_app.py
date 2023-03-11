import pytest
import simplejson as json
import requests
import logging

from tests.fixtures import *
from tests.mock.mock_request import MockRequest
from src.app import handler
from src.dynamodb import get_product

from src.dynamodb import update_product

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


def test_sessionstart():
    update_product('21032023025828', 'fails', 0)
    update_product('21032023025828', 'title', 'comming soon')
    update_product('21032023025828', 'active', 1)
    pass


def test_handler_kabum_fail(sqs_payload_kabum, mocker, request_kabum_fail):
    mocker.patch.object(requests, 'get', return_value=MockRequest(request_kabum_fail))

    request = handler(json.loads(sqs_payload_kabum), None)
    code = request.get('statusCode')
    assert code == 422


def test_handler_kabum_success(sqs_payload_kabum, mocker, request_kabum_success):
    mocker.patch.object(requests, 'get', return_value=MockRequest(request_kabum_success))

    request = handler(json.loads(sqs_payload_kabum), None)
    code = request.get('statusCode')
    assert code == 200


def test_handler_amazon_success(sqs_payload_amazon, mocker, request_amazon_success):
    mocker.patch.object(requests, 'get', return_value=MockRequest(request_amazon_success))

    request = handler(json.loads(sqs_payload_amazon), None)
    code = request.get('statusCode')
    assert code == 200


def test_handler_amazon_fail(sqs_payload_amazon, mocker, request_amazon_fail):
    mocker.patch.object(requests, 'get', return_value=MockRequest(request_amazon_fail))

    request = handler(json.loads(sqs_payload_amazon), None)
    code = request.get('statusCode')
    assert code == 422


def test_handler_update_product(sqs_payload_amazon, mocker, request_amazon_success):
    mocker.patch.object(requests, 'get', return_value=MockRequest(request_amazon_success))
    payload = json.loads(sqs_payload_amazon)
    body: str = payload.get('Records')[0].get('body')
    product_id: int = json.loads(body).get('id')

    request = handler(json.loads(sqs_payload_amazon), None)
    code = request.get('statusCode')

    product = get_product(product_id)

    assert 'Apple' in product.get('title')
    assert '17.999' in product.get('price')
    assert int(product.get('active')) == 1
    assert code == 200


def test_handler_disable_product_after_3_fails(sqs_payload_amazon_fails, mocker, request_amazon_fail):
    mocker.patch.object(requests, 'get', return_value=MockRequest(request_amazon_fail))
    payload = json.loads(sqs_payload_amazon_fails)
    body: str = payload.get('Records')[0].get('body')
    product_id: int = json.loads(body).get('id')

    request = handler(payload, None)
    code = request.get('statusCode')

    product = get_product(product_id)

    assert int(product.get('fails')) > 3
    assert int(product.get('active')) == 0
    assert code == 422


def pytest_sessionfinish(exitstatus):
    assert exitstatus == 0


"""
def test_handler_send_user_alert(sqs_payload_amazon, mocker, request_amazon_success):
    mocker.patch.object(requests, 'get', return_value=MockRequest(request_amazon_success))
    payload = json.loads(sqs_payload_amazon)
    body: str = payload.get('Records')[0].get('body')
    product_id: int = json.loads(body).get('id')

    request = handler(json.loads(sqs_payload_amazon), None)
    code = request.get('statusCode')

    product = get_product(product_id)

    assert 'Apple' in product.get('title')
    assert int(product.get('active')) == 1
    assert code == 200
"""
