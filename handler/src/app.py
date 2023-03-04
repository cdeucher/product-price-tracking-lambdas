import os
import boto3
import json
import logging
from tittles import get_titles, create_title
from subscriptions import subscription, request_create_topic

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TITLES_TABLE = os.environ.get('TITLES_TABLE', 'titles')
db_table = boto3.resource('dynamodb').Table(TITLES_TABLE)

def handler(event, context):
    body = event.get('body')
    headers = event.get('headers')
    logger.info("Headers: %s", headers)
    logger.info("Body: %s", body)
    response_code = 422
    response_body = {'error': 'Unprocessable Entity'}

    if body:
        payload = json.loads(body)
        logger.info("Payload: %s", payload)

        if payload.get('action') == 'new':
            try:
                response_body, response_code, saved_product = create_title(db_table, payload.get('product'))
            except Exception as e:
                logger.exception(f'Could not create title.')
                raise

            try:
                response_body, response_code = request_create_topic(saved_product)
            except Exception as e:
                logger.exception(f'Could not create SNS topic.')

        elif payload.get('action') == 'subscribe':
            try:
                response_body, response_code = subscription(headers.get('Authorization'), payload.get('topic'))
            except Exception as e:
                logger.exception(f'Could not create subscription.')

    else:
        response_body, response_code = get_titles(db_table)

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