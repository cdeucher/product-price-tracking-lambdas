import logging, requests
from bs4 import BeautifulSoup
from lxml import etree


logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


def scrap(url):
        logger.info("url %s", url)
        page = get_html_page(url)
        logger.info("page %s", page)
        price, title = scrape_html(page.text)

        return price, title


def get_html_page(url):
    logger.info("get_html_page %s", url)
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    return requests.get(url, headers=HEADERS)


def scrape_html(webpage):
    soup = BeautifulSoup(webpage, "html.parser")
    dom = etree.HTML(str(soup))
    logger.info("dom %s", dom)

    price = dom.xpath('//*[@class="a-price-whole"]')[0].text
    title = dom.xpath('//*[@id="productTitle"]')[0].text
    logger.info("%s %s", price, title)
    return price, title


if __name__ == '__main__':
    price, title = scrap("https://www.amazon.com.br/Mentes-perigosas-psicopata-comemorativa-anivers%C3%A1rio/dp/8525067326")
    logger.error("%s %s", price, title)
