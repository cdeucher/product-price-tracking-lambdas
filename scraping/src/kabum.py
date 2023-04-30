import logging
from selenium.webdriver.common.by import By
from scraper import Scraper

logger = logging.getLogger("lambda")
logger.setLevel(logging.INFO)  # INFO


class Kabum(Scraper):

    def __init__(self, url):
        super().__init__(url)
        self.price = None
        self.title = None
        self.image = None

    def scrap(self):
        self.find_image()
        self.find_price()
        self.find_title()
        self.browser.quit()

        if not all((self.price, self.title, self.image)):
            raise Exception(f"scrapping error: price, title, image:{len(self.price)},{len(self.title)},{len(self.image)}")
    # endDef

    def find_price(self):
        price = self.browser.find_element(By.CLASS_NAME, "finalPrice")
        logger.info("price - %s", price.text)

        self.price = price.text.replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "")

    def find_title(self):
        container = self.browser.find_element(By.CLASS_NAME, "container-purchase")
        title = container.find_element(By.XPATH, '//h1')
        logger.info("title - %s", title.text)
        self.title = title.text

    def find_image(self):
        img = self.browser.find_element(By.CSS_SELECTOR, "img.iiz__img")
        self.image = img.get_attribute("src")
    # endDef

    def get_price(self):
        return self.price

    def get_title(self):
        return self.title

    def get_image(self):
        return self.image
