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

    body = event.get('body')
    headers = event.get('headers')

    if body:
        decodedToken = jwt.decode(headers['Authorization'], algorithms=["RS256"], options={"verify_signature": False})
        email = decodedToken["email"]
        sub = json.loads(body)
        logger.info("decodedToken: %s %s", email, decodedToken)
        response_body, response_code = request_create_subscription(sub, email)
    else:
        response_body, response_code = request_create_topic(event)

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

def request_create_topic(event):
    response_body = {'error': 'Unprocessable Entity'}
    response_code = 422
    try:
        topic = create_topic(event.get('id'))
        logger.info("topic: %s", topic)
        response_body = { 'message': 'create topic ok' }
        response_code = 200
    except Exception as e:
        logger.exception(f'Could not create SNS topic.')
        raise

    return response_body, response_code

def request_create_subscription(sub, email):
    response_body = {'error': 'Unprocessable Entity'}
    response_code = 422
    try:
        topic         = create_topic(sub.get('topic'))
        subscription  = create_subscription(topic.get('TopicArn'), email)
        logger.info("subscription: %s", subscription)
        response_body = [{ 'message': sub.get('topic')+' - '+email+' ok' }]
        response_code = 200
    except Exception as e:
        logger.exception(f'Could not create subscription.')
        raise

    return response_body, response_code

def create_subscription(topic_arn, email):
    try:
        response    = sns_client.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint=email)
        subscription_arn = response["SubscriptionArn"]
        logger.info(f'Created SNS subscription {email} for topic {subscription_arn}.')
    except Exception as e:
        logger.exception(f'Could not create SNS subscription {email} for topic {subscription_arn}.')
        raise

    return response

def create_topic(name):
    topic = 'Could not create SNS topic '+name
    try:
        topic = sns_client.create_topic(Name=name)
        logger.info(f'Created SNS topic {name}.')
    except Exception as e:
        logger.exception(f'Could not create SNS topic {name}.')
        raise

    return topic