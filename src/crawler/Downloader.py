from io import BytesIO

import requests
from PIL import Image
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

class presence_of_element_with_img_alt:
    def __init__(self, locator, alt_value):
        self.locator = locator
        self.alt_value = alt_value

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            if element.get_attribute('alt') == self.alt_value:
                return element
            else:
                print(element.get_attribute('alt')," == ", self.alt_value )
                return False
        except NoSuchElementException:
            print("No alt tag")
            return False

class ImageDownloader:

    def __init__(self, headless: bool = False):
        self.options = webdriver.FirefoxOptions()
        if (headless):
            self.options.add_argument('--headless')  # Run in headless mode
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=self.options)

    def __CreateDriver(self):
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=self.options)

    def download_image_buondua(self, url: str, savingPath_with_file: str):
        self.driver.get(url)

        try:
            image_page = WebDriverWait(self.driver,10).until(presence_of_element_with_img_alt((By.TAG_NAME, 'img'),url))
            image_page.screenshot(savingPath_with_file)
            return True
        except TimeoutException:
            print("image to url not found ", url)
            return False

    def Quit(self):
        self.driver.close()
