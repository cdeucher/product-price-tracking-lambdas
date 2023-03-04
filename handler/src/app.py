import os
import boto3
import json
import logging
from tittles import get_titles, create_title

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TITLES_TABLE = os.environ.get('TITLES_TABLE', 'titles')
SUB_LAMBDA   = os.environ.get('SUB_LAMBDA', '')

lambda_client = boto3.client('lambda')
db_table = boto3.resource('dynamodb').Table(TITLES_TABLE)

def handle(event, context):
    body = event.get('body')
    headers = event.get('headers')
    logger.info("Headers: %s", headers)
    logger.info("Body: %s", body)

    if body:
        payload = json.loads(body)
        logger.info("Payload: %s", payload)

        if payload['action'] == 'new':
            response_body, response_code, saved_product = create_title(db_table, payload['product'])
            call_lambda(SUB_LAMBDA, saved_product)
        elif payload['action'] == 'subscribe':
            response_body, response_code = get_titles(db_table)

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

def call_lambda(function_name, function_params):
    logger.info("call_lambda %s", function_name)
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(function_params)
    )
    logger.info("call_lambda %s", response)
    return response