import logging, requests
from bs4 import BeautifulSoup
from lxml import etree

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


def scrap(url):
    logger.info("url %s", url)
    page = get_html_page(url)
    logger.info("page %s", len(page))
    price, title, image = scrape_html(page, url)
    return price, title, image


def get_html_page(url):
    logger.info("get_html_page %s", url)
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'})
    return requests.get(url, headers=HEADERS, timeout=(3.05, 27)).text

def debug_html_page(url):
    logger.info("get_html_page %s", url)
    '''
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.binary_location='E:/dev/product-tracking/product-tracking-lambdas/scraping/src/geckodriver.exe'
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    wait = WebDriverWait(browser, 10)  # Wait for 10 seconds
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    page = browser.page_source
    browser.quit()
    return page
    '''


def scrape_html(webpage, url):
    logger.info("page %s", len(webpage))
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
    title = container.xpath('//h1/text()')
    logger.info("title - %s", len(title))

    price = container.xpath('//*[contains(@class, "finalPrice")]')
    logger.info("price - %s", len(price))

    carousel = dom.xpath('//*[@id="carouselDetails"]')[0]
    image = carousel.xpath('//div[@data-index="1"]//img/@src')
    logger.info("image - %s", len(image))

    if len(price) == 0 or len(title) == 0: # or len(image) == 0:
        raise Exception(f"scrapping error: price, title, image:{len(price)},{len(title)},{len(image)}")

    if len(image) == 0:
        image = ""
    else:
        image = image[0]

    price = price[0].text.replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "")

    return price, title, image


def amazon(dom):
    title = dom.xpath('//*[@id="productTitle"]')
    logger.info("title - %s", len(title))

    price = dom.xpath('//*[@class="a-price-whole"]')
    if len(price) == 0:
        price = dom.xpath('//*[@class="a-offscreen"]')
    logger.info("price - %s", len(price))

    image = dom.xpath('//*[@id="imageBlockThumbs"]//img/@src')
    if len(image) == 0:
        image = dom.xpath('//*[@id="imageBlock"]//img/@src')
    logger.info("image - %s", len(image))

    if len(price) == 0 or len(title) == 0 or len(image) == 0:
        raise Exception(f"scrapping error: price, title, image:{len(price)},{len(title)},{len(image)}")

    return price[0].text, title[0].text, image[0]


def store_page(url):
    html = get_html_page(url)
    with open('example.txt', 'w') as f:
        f.write(html)


if __name__ == '__main__':
    try:
        url = "https://www.kabum.com.br/produto/181088/processador-amd-ryzen-5-5600g-3-9ghz-4-4ghz-max-turbo-cache-19mb-6-nucleos-12-threads-video-integrado-am4-100-100000252box"
        # store_page(url)
        price, title, image = scrap(url)
        logger.error("%s %s %s", price, title, image)
    except Exception as e:
        logger.error("starts error")
        logger.exception(f'{e}.')
    logger.error("end")
