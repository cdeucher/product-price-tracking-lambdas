import os
import boto3
import json
import logging
import requests
from bs4 import BeautifulSoup
from lxml import etree

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO) #INFO

TITLES_TABLE = os.environ.get('TITLES_TABLE', 'titles')
SUB_LAMBDA   = os.environ.get('SUB_LAMBDA', '')

if SUB_LAMBDA:
    lambda_client = boto3.client('lambda')

table = boto3.resource('dynamodb').Table(TITLES_TABLE)

def handler(event, context):
    logger.info("exec_filter %s", event)
    response_body = {'error': 'Unprocessable Entity'}
    response_code = 422

    if validate_fields(event):
        for record in event['Records']:
            if 'OldImage' in record['dynamodb'] :
                d_data = record['dynamodb']['OldImage']
            else:
                d_data = record['dynamodb']['NewImage']
            url  = d_data['url']['S']
            id   = d_data['id']['S']
            logger.info("url %s", url)
            page = get_html_page(url)
            logger.info("page %s", page)
            price, title = scrape_html(page.text)
            item = update_dynamo(url, price, title, id,record['eventID'])

        response_code = 200
        response_body = {'message': price + " " + title}

    response = {
        'statusCode': response_code,
        'body': json.dumps(response_body)
    }

    logger.info("Response: %s", response)
    return response

def get_html_page(url):
    logger.info("get_html_page %s", url)
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                'Accept-Language': 'en-US, en;q=0.5'})
    return requests.get(url,headers=HEADERS)

def scrape_html(webpage):
    soup = BeautifulSoup(webpage, "html.parser")
    dom = etree.HTML(str(soup))

    price = dom.xpath('//*[@class="a-price-whole"]')[0].text
    title = dom.xpath('//*[@id="productTitle"]')[0].text
    logger.info("%s %s", price, title)
    return price, title

def update_dynamo(url, price, title, id, event_id):
    logger.info("update_item text:%s", title)
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
    return update

def validate_fields(events_elements):
    logger.info("validate_fields %s %s", events_elements, type(events_elements))
    if type(events_elements) is not dict:
        return False
    if 'Records' not in events_elements:
        return False
    if type(events_elements['Records']) is not list or len(events_elements['Records']) == 0:
        return False
    return True

if __name__ == '__main__':
    page = get_html_page("https://www.amazon.com.br/Controle-DualSenseTM-Edi%C3%A7%C3%A3o-limitada-Ragnarok/dp/B0BL1WCP2K")
    price, title = scrape_html(page.text)
    logger.error("%s %s", price, title)