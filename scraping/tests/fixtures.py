import pytest

@pytest.fixture
def sqs_payload_kabum():
    file = open('mock/fixtures/sqs-payload-kabum.json', 'r')
    contents = file.read()
    file.close()
    return contents


@pytest.fixture
def sqs_payload_amazon():
    file = open('mock/fixtures/sqs-payload-amazon.json', 'r')
    contents = file.read()
    file.close()
    return contents


@pytest.fixture
def sqs_payload_amazon_fails():
    file = open('mock/fixtures/sqs-payload-amazon-3-fails.json', 'r')
    contents = file.read()
    file.close()
    return contents


@pytest.fixture
def request_kabum_success():
    file = open('mock/fixtures/response-kabum-success.html', 'r')
    contents = file.read()
    file.close()
    return contents


@pytest.fixture
def request_kabum_fail():
    file = open('mock/fixtures/response-request-kabum-fail.html', 'r')
    contents = file.read()
    file.close()
    return contents


@pytest.fixture
def request_amazon_success():
    file = open('mock/fixtures/response-request-amazon-success.html', 'r')
    contents = file.read()
    file.close()
    return contents


@pytest.fixture
def request_amazon_fail():
    file = open('mock/fixtures/response-request-amazon-fail.html', 'r')
    contents = file.read()
    file.close()
    return contents