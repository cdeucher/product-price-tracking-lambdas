import os, boto3, logging

TITLES_TABLE = os.environ.get('TITLES_TABLE', 'titles')

if os.environ.get('AWS_OFFLINE'):
    table = boto3.resource('dynamodb', endpoint_url='http://localhost:4566').Table(TITLES_TABLE)
else:
    table = boto3.resource('dynamodb').Table(TITLES_TABLE)

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


def update_dynamo(id, price, title, image):
    logger.info("update_item text:%s - price:%s - id:%s", title, price, id)
    try:
        update = table.update_item(
            Key={
                'id': id
            },
            UpdateExpression="set title = :g, price = :p, image_url = :i",
            ExpressionAttributeValues={
                ':g': title, ':p': price, ':i': image
            },
            ReturnValues="UPDATED_NEW"
        )
        logger.info("update %s", update)
        return {'updated': 'ok', 'productId': id}, 200

    except Exception as e:
        logger.error("Error: %s", e)


def update_product(id, field, value):
    logger.info("update_item id:%s - field:%s - value:%s", id, field, value)
    try:
        update = table.update_item(
            Key={
                'id': id
            },
            UpdateExpression="set " + field + " = :g",
            ExpressionAttributeValues={
                ':g': value
            },
            ReturnValues="UPDATED_NEW"
        )
        logger.info("update %s", update)

        return {'updated': 'ok', 'productId': id}, 200
    except Exception as e:
        logger.error("Error: %s", e)


def get_product(id) -> dict:
    logger.info("get_item id:%s", id)
    try:
        response = table.get_item(
            Key={
                'id': id
            }
        )
        logger.info("get %s", response)
        return response['Item']
    except Exception as e:
        logger.error("Error: %s", e)
