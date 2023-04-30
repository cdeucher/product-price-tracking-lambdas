import json
from scraping import scrap
from message import message
from dynamodb import update_dynamo, update_product
import logging

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


def handler(event, context) -> dict:
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


def update_from_cron_product(event) -> (dict, int):
    logger.info("exec_filter %s", event)
    body: str = event.get('Records')[0].get('body')
    logger.info("Body: %s", body)
    product = json.loads(body)
    logger.info("Product: %s", product)

    try:
        new_price, title, image = scrap(product.get('url'))
        logger.info("New price: %s - Title: %s", new_price, title)

        #if float(new_price) <= float(product.get('price_target')):
        message(product.get('id'), product.get('url') + " - Price changed to " + new_price)

        msg, code = update_dynamo(product.get('id'), new_price, title, image)

        return msg, code
    except Exception as e:
        update_fails_product(product)

        logger.error(f'{e}.')
        raise


def update_fails_product(product: dict) -> None:
    fails = (1 if product.get('fails') is None else int(product.get('fails')) + 1)
    update_product(product.get('id'), 'fails', fails)
    if fails > 3:
        update_product(product.get('id'), 'active', 0)


def update_from_insert_product(event: dict) -> (dict, int):
    try:
        url, id, eventID = dynamodb_stream_data(event)
        price, title, image = scrap(url)
        item = update_dynamo(id, price, title, image)
        logger.info(f'Updated DynamoDB item {item}.')
        return {'updated': 'ok', 'productId': id}, 200
    except Exception as e:
        logger.exception(f'Unable to update DynamoDB item {id}.')
        raise


def dynamodb_stream_data(event: dict) -> (str, str, str):
    for record in event.get('Records'):
        if 'OldImage' in record['dynamodb']:
            d_data = record['dynamodb']['OldImage']
        else:
            d_data = record['dynamodb']['NewImage']
        url: str = d_data['url']['S']
        id: str = d_data['id']['S']

        return url, id, record.get('eventID')

if __name__ == '__main__':
    file = open('tests/mock/fixtures/sqs-payload.json', 'r')
    contents = file.read()
    file.close()
    handler(json.loads(contents), None)
