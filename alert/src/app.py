import os
import boto3
from boto3.dynamodb.conditions import Key,Attr
import json
import logging
import jwt
from datetime import datetime;

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUEUE_NAME = os.environ.get('QUEUE_NAME', 'titles')
sqs   = boto3.resource('sqs').get_queue_by_name(QueueName=QUEUE_NAME)

AWS_REGION = "us-east-1"
sns_client = boto3.client("sns", region_name=AWS_REGION)

def handler(event, context):
    logger.info("Event: %s", event)

    body = json.loads(event.get('Records')[0].get('body'))
    logger.info("Body: %s", body)

    msg = create_sns_message(body.get('id'), body.get('title'))

    response_code = 200
    response_body = {'message': msg }

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

def create_sns_message(id, message):
    send = 'Could not create SNS message '+id
    try:
        topic = create_topic(id)
        send  = sns_client.publish(
            TargetArn=topic.get('TopicArn'),
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        logger.info(f'Created SNS message {id}.')
    except Exception as e:
        logger.exception(f'Could not create SNS message {id}.')
        raise

    return send

def create_topic(name):
    topic = 'Could not create SNS topic '+name
    try:
        topic = sns_client.create_topic(Name=name)
        logger.info(f'Created SNS topic {name}.')
    except Exception as e:
        logger.exception(f'Could not create SNS topic {name}.')
        raise

    return topic