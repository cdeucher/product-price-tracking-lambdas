import os
import boto3
import json
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TITLES_TABLE = os.environ.get('TITLES_TABLE', 'titles')
table = boto3.resource('dynamodb').Table(TITLES_TABLE)

def handle(event, context):
    logger.info("exec_filter %s", event)
    response_body = {'error': 'Unprocessable Entity'}
    response_code = 422

    if validate_fields(event):
        for record in event['Records']:
            logger.info("record %s %s %s", record['eventID'], record['eventName'], record['dynamodb']['OldImage'])
            logger.info("record - url %s", record['dynamodb']['OldImage']['url']['S'])
            url = record['dynamodb']['OldImage']['url']['S']

            page = get_html_page(url)
            page_title = scrape_html(page)
            update_dynamo('url',url, page_title)

        response_code = 200
        response_body = callback()

    response = {
        'statusCode': response_code,
        'body': json.dumps(response_body)
    }

    logger.info("Response: %s", response)
    return response

def get_html_page(url):
    logger.info("get_html_page %s", url)
    return requests.get(url)

def scrape_html(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    page_title = soup.title
    logger.info("page title %s", soup.title)
    product_title = soup.find('span', {'id': 'productTitle'})
    logger.info("product_title %s", product_title)
    return page_title

def update_dynamo(item_key, value, page_title):
    table.update_item(
        Key={item_key: value},
        AttributeUpdates={
            'text': page_title,
        },
    )

def callback():
    response_body = {'message': 'Hello, World!'}
    logger.info("Response: %s", response_body)
    return response_body


def validate_fields(events_elements):
    logger.info("validate_fields %s %s", events_elements, type(events_elements))
    if type(events_elements) is not dict:
        return False
    if 'Records' not in events_elements:
        return False
    if type(events_elements['Records']) is not list or len(events_elements['Records']) == 0:
        return False
    return True