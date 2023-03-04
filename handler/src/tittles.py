import os
from datetime import datetime;
from boto3.dynamodb.conditions import Key,Attr
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_titles(db_table):
    response_body = {'error': 'Unprocessable Entity'}
    response_code = 422
    try:
        titles = []
        response = db_table.scan(
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

def create_title(db_table, title):
    response_body = {'error': 'Unprocessable Entity'}
    response_code = 422
    try:
        saved_product = save_title(db_table, title)
        response_body = {'created': 'ok', 'productId': saved_product['id'] }
        response_code = 200

    except Exception as e:
        logger.error("Error: %s", e)
    return response_body, response_code, saved_product

def save_title(db_table, title):
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    id = datetime.now().strftime("%d%m%Y%H%M%S")
    db_table.put_item(
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
