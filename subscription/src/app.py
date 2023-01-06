import os
import boto3
import json
import logging
import jwt
from datetime import datetime;

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_REGION = "us-east-1"
sns_client = boto3.client("sns", region_name=AWS_REGION)

def handle(event, context):
    logger.info(f'Event: {event}')

    response_body, response_code = { 'message': 'ok' }, 200

    create_topic(event)

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

def create_topic(event):
    name = event.get('id')
    topic = 'Could not create SNS topic '+name
    try:
        topic = sns_client.create_topic(Name=name)
        logger.info(f'Created SNS topic {name}.')
    except Exception as e:
        logger.exception(f'Could not create SNS topic {name}.')
        raise

    return topic