import json
import logging
from scraping import scrap
from message import message
from dynamodb import update_dynamo

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


def handler(event, context):
    logger.info("exec_filter %s", event)
    msg = {'error': 'Unprocessable Entity'}
    code = 422

    try:
        if event.get('Records')[0].get('eventSource') == 'aws:sqs':
            msg, code = update_from_cron_product(event)
        else:
            msg, code = update_from_insert_product(event)
    except Exception as e:
        logger.exception(f'{e}.')

    response = {
        'statusCode': code,
        'body': json.dumps(msg)
    }
    logger.info("Response: %s", response)
    return response


def update_from_cron_product(event):
    logger.info("exec_filter %s", event)
    try:
        product = json.loads(event.get('Records')[0].get('body'))
        logger.info("Product: %s", product)

        new_price, title = scrap(product.get('url'))
        logger.info("New price: %s - Title: %s", new_price, title)

        if float(new_price) <= float(product.get('price_target')):
            message(product, product.get('url')+" - Price changed to " + new_price)

        msg, code = update_dynamo(product.get('url'), new_price, title, product.get('id'), product.get('event_id'))

        return msg, code
    except Exception as e:
        logger.exception(f'{e}.')
        raise


def update_from_insert_product(event):
    try:
        url, id, eventID = dynamodb_stream_data(event)
        price, title = scrap(url)
        item = update_dynamo(url, price, title, id, eventID)
        logger.info(f'Updated DynamoDB item {item}.')
        return {'updated': 'ok', 'productId': id}, 200
    except Exception as e:
        logger.exception(f'Unable to update DynamoDB item {id}.')
        raise


def dynamodb_stream_data(event):
    for record in event.get('Records'):
        if 'OldImage' in record['dynamodb']:
            d_data = record['dynamodb']['OldImage']
        else:
            d_data = record['dynamodb']['NewImage']
        url = d_data['url']['S']
        id = d_data['id']['S']

        return url, id, record.get('eventID')
