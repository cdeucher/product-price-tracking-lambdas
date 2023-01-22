import os
import boto3
from boto3.dynamodb.conditions import Key,Attr
import json
import logging
import jwt
from datetime import datetime;

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TITLES_TABLE = os.environ.get('TITLES_TABLE', 'titles')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'titles')

table = boto3.resource('dynamodb').Table(TITLES_TABLE)
sqs   = boto3.resource('sqs').get_queue_by_name(QueueName=QUEUE_NAME)

def handle(event, context):
    body = event.get('body')
    headers = event.get('headers')
    logger.info("Headers: %s", headers)

    titles = get_titles()

    logger.info("Titles: %s", titles)
    response_code = 200
    response_body = {
        'titles': titles
    }

    response = {
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'statusCode': response_code,
        'body': json.dumps(response_body)
    }

    logger.info("Response: %s", response)
    return response

def get_titles():
    titles = []
    response = table.scan(
         FilterExpression=Attr('active').eq(1)
    )
    for item in response['Items']:
        titles.append({
            'title': item['title'],
            'price': item['price'],
            'symbol': item['symbol'],
            'url': item['url'],
            'type': item['type'],
            'date': item['date'],
            'price_target': item['price_target'],
            'id': item['id'] if 'id' in item else ''
        })
        send_message(json.dumps({"title":item['title'], "url":item['url'], "price_target":item['price_target'], "id":item['id']}))
    return titles

def send_message(message):
    response = sqs.send_message(MessageBody=message)
    return response