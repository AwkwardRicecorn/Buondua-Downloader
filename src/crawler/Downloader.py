from io import BytesIO

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


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
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located((By.CLASS_NAME, 'challenge-running')))
        except:
            self.driver.reload()
        try:
            image_page = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'shrinkToFit')))
            image_url = image_page.get_attribute('src')
            if image_url:
                try:
                    # Download the image using requests%
                    response = requests.get(image_url)
                    response.raise_for_status()

                    image = Image.open(BytesIO(response.content))
                    image.save(savingPath_with_file)
                except Exception as e:
                    screenshot = self.driver.find_element(By.CLASS_NAME, 'shrinkToFit')
                    screenshot.screenshot(savingPath_with_file)
            else:
                return False
            return
        except:
            try:
                image_page = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
                image_url = image_page.get_attribute('src')
                if image_url:
                    screenshot = self.driver.find_element(By.TAG_NAME, 'img')
                    screenshot.screenshot(savingPath_with_file)
                else:
                    return False
                return
            except:
                return False
        finally:
            return True

    def Quit(self):
        self.driver.close()