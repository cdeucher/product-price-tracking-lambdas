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
SUB_LAMBDA   = os.environ.get('SUB_LAMBDA', '')

lambda_client = boto3.client('lambda')
table = boto3.resource('dynamodb').Table(TITLES_TABLE)

def handle(event, context):
    #logger.info("Authorization: %s", headers['Authorization'])
    body = event.get('body')
    headers = event.get('headers')
    logger.info("Headers: %s", headers)

    if body:
        response_body, response_code, event = request_post(body, headers)
        call_lambda(SUB_LAMBDA, event)
    else:
        response_body, response_code = request_get(body, headers)

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

def request_get(body, headers):
    response_body = {'error': 'Unprocessable Entity'}
    response_code = 422
    try:
        titles = []
        response = table.scan(
           FilterExpression=Attr('active').eq(1)
        )
        #response = table.query(
        #    KeyConditionExpression=Key('active').eq(1) & Key('site').eq('')
        #)
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
        response_body = titles
        response_code = 200
    except Exception as e:
        logger.error("Error: %s", e)
    return response_body, response_code

def request_post(body, headers):
    response_body = {'error': 'Unprocessable Entity'}
    response_code = 422
    try:
        # decodedToken = jwt.decode(headers['Authorization'], algorithms=["RS256"], options={"verify_signature": False})
        if validate_fields(json.loads(body)):
            titles = json.loads(body)
            event = save_title(titles[0])
            response_body = {'list': 'ok', 'count': titles.__len__() } #, 'username': decodedToken["cognito:username"]}
            response_code = 200

    except Exception as e:
        logger.error("Error: %s", e)
    return response_body, response_code, event

def save_title(title):
    event = {}
    if not os.environ.get('IS_OFFLINE'):
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        id = datetime.now().strftime("%d%m%Y%H%M%S")
        response = table.put_item(
            Item={
                'id': id,
                'site': title['url'],
                'active': 1,
                'title': 'comming soon',
                'price': '',
                'symbol': '',
                'url': title['url'],
                'type': '',
                'date': date_now,
                'price_target': title['price_target']
            }
        )
    return { 'url':title['url'], 'id': id }

def call_lambda(function_name, function_params):
    logger.info("call_lambda %s", function_name)
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(function_params)
    )
    logger.info("call_lambda %s", response)
    return response

def validate_fields(body_elements):
    if type(body_elements) is not list:
        return False

    list_fields = ['url', 'price_target']

    for elements in body_elements:
        for key in elements:
            if key not in list_fields:
                return False
    return True
