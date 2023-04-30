import logging, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


class Scraper:
    def __init__(self, url):
        self.url = url
        self.wait = None
        self.browser = None
        self.options = Options()

        self.bootsrap()
        self.load_page()

    def bootsrap(self):
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument('--disable-dev-tools')
        self.options.add_argument('--user-data-dir=/tmp/chrome-user-data')
        self.options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        self.options.add_argument('--single-process')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--debug')
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
        # self.options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        self.options.binary_location = r"/usr/bin/firefox"
        self.browser = webdriver.Firefox(executable_path=self.get_firefox_executable_path()
                                         , options=self.options
                                         , service_log_path='/tmp/geckodriver.log')
        self.wait = WebDriverWait(self.browser, 10)

    # endDef

    def load_page(self):
        self.browser.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # endDef

    def get_firefox_executable_path(self) -> str:
        try:
            if 'FIREFOX_DRIVER' in os.environ:
                logger.info("FIREFOX_DRIVER %s", os.environ.get("FIREFOX_DRIVER"))
                return os.environ.get("FIREFOX_DRIVER")
            elif os.path.exists("/usr/bin/geckodriver"):
                return "/usr/bin/geckodriver"
        except Exception as e:
            logger.error("error %s", e)

"""
    def scrap(url):
        logger.info("url %s", url)
        page = get_html_page(url)
        logger.info("page %s", len(page))
        price, title, image = scrape_html(page, url)
        return price, title, image


    def scrape_html(webpage, url):
        logger.info("page %s", len(webpage))
        soup = BeautifulSoup(webpage, "html.parser")
        dom = etree.HTML(str(soup))
        logger.info("dom %s", dom)
        price, title, image = 0, "not supported yet", ""
        #if "kabum" in url:
        #    price, title, image = kabum(dom)

        return price, title, image


if __name__ == '__main__':
    try:
        url = "https://www.kabum.com.br/produto/181088/processador-amd-ryzen-5-5600g-3-9ghz-4-4ghz-max-turbo-cache-19mb-6-nucleos-12-threads-video-integrado-am4-100-100000252box"
        # debug_chrome_html_page(url)

        # store_page(url)
        # price, title, image = scrap(url)
        # logger.error("%s %s %s", price, title, image)
    except Exception as e:
        logger.error("starts error")
        logger.exception(f'{e}.')
    logger.error("end")
"""
