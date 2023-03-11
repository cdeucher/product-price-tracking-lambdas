import os
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUEUE_NAME = os.environ.get('QUEUE_NAME', 'titles')
sqs = boto3.resource('sqs').get_queue_by_name(QueueName=QUEUE_NAME)

AWS_REGION = "us-east-1"
sns_client = boto3.client("sns", region_name=AWS_REGION)


def message(id, message) -> None:
    logger.info("Product: %s - Message: %s", id, message)

    try:
        topicArn = create_sns_message(id, message)
        logger.info("Response: %s", topicArn)
    except Exception as e:
        logger.exception(f'{e}.')
        raise

def create_sns_message(id, message):
    send = 'Could not create SNS message ' + id
    try:
        topic = create_topic(id)
        send = sns_client.publish(
            TargetArn=topic.get('TopicArn'),
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        logger.info(f'Created SNS message {send}.')
    except Exception as e:
        logger.exception(f'Could not create SNS message {send}.')
        raise

    return topic.get('TopicArn')


def create_topic(name):
    topic = 'Could not create SNS topic ' + name
    try:
        topic = sns_client.create_topic(Name=name)
        logger.info(f'Created SNS topic {name}.')
    except Exception as e:
        logger.exception(f'Could not create SNS topic {name}.')
        raise

    return topic
