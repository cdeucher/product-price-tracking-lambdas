import os, boto3, logging

import boto3 as boto3

TITLES_TABLE = os.environ.get('TITLES_TABLE', 'titles')
table = boto3.resource('dynamodb').Table(TITLES_TABLE)

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


def update_dynamo(url, price, title, id, event_id):
    logger.info("update_item text:%s - price:%s - id:%s - event_id:%s", title, price, id, event_id)
    try:
        update = table.update_item(
            Key={
                'site': url,
                'id': id
            },
            UpdateExpression="set title = :g, price = :p, event_id = :i",
            ExpressionAttributeValues={
                ':g': title, ':p': price, ':i': event_id
            },
            ReturnValues="UPDATED_NEW"
        )
        logger.info("update %s", update)
        return {'updated': 'ok', 'productId': id}, 200

    except Exception as e:
        logger.error("Error: %s", e)
