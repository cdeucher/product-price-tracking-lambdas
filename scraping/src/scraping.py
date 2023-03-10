import logging, requests
from bs4 import BeautifulSoup
from lxml import etree

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


def scrap(url):
    try:
        logger.info("url %s", url)
        page = get_html_page(url)
        logger.info("page %s", page)
        price, title = scrape_html(page.text, url)
        return price, title
    except Exception as e:
        logger.exception(f'{e}.')


def get_html_page(url):
    logger.info("get_html_page %s", url)
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'})
    return requests.get(url, headers=HEADERS)


def scrape_html(webpage, url):
    soup = BeautifulSoup(webpage, "html.parser")
    dom = etree.HTML(str(soup))
    logger.info("dom %s", dom)
    price, title = 0, "not supported yet"
    if "amazon" in url:
        price, title = amazon(dom)
    elif "kabum" in url:
        price, title = kabum(dom)

    return price, title


def kabum(dom):
    container = dom.xpath('//*[contains(@class, "container-purchase")]')
    title = container[0].xpath('//h1/text()')[0]
    logger.info("title %s", title)
    price = container[0].xpath('//*[contains(@class, "finalPrice")]')[0].text
    price = price.replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "")
    logger.info("price %s", price)
    return price, title


def amazon(dom):
    price = dom.xpath('//*[@class="a-price-whole"]')[0].text
    title = dom.xpath('//*[@id="productTitle"]')[0].text
    logger.info("%s %s", price, title)
    return price, title


if __name__ == '__main__':
    price, title = scrap(
        "https://www.kabum.com.br/produto/181088/processador-amd-ryzen-5-5600g-3-9ghz-4-4ghz-max-turbo-cache-19mb-6-nucleos-12-threads-video-integrado-am4-100-100000252box")
    logger.error("%s %s", price, title)
    logger.error("end")
