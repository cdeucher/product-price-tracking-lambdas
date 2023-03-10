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
        price, title, image = scrape_html(page.text, url)
        return price, title, image
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
    price, title, image = 0, "not supported yet", ""
    if "amazon" in url:
        price, title, image = amazon(dom)
    elif "kabum" in url:
        price, title, image = kabum(dom)

    return price, title, image


def kabum(dom):
    container = dom.xpath('//*[contains(@class, "container-purchase")]')[0]
    title = container.xpath('//h1/text()')[0]
    logger.info("title %s", title)
    price = container.xpath('//*[contains(@class, "finalPrice")]')[0].text
    price = price.replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "")
    logger.info("price %s", price)

    carousel = dom.xpath('//*[@id="carouselDetails"]')[0]
    image = carousel.xpath('//div[@data-index="1"]//img/@src')[0]
    logger.info("image %s", image)
    return price, title, image


def amazon(dom):
    price = dom.xpath('//*[@class="a-price-whole"]')[0].text
    title = dom.xpath('//*[@id="productTitle"]')[0].text
    logger.info("%s %s", price, title)

    image = dom.xpath('//*[@id="imageBlockThumbs"]//img/@src')[0]
    logger.info("image %s", image)

    return price, title, image


if __name__ == '__main__':
    price, title, image = scrap(
        "https://www.kabum.com.br/produto/129653/placa-mae-asus-prime-a520m-e-amd-am4-matx-ddr4")
    logger.error("%s %s %s", price, title, image)
    logger.error("end")
