

from abc import ABC, abstractmethod
from selenium import webdriver
from urllib import request
from services.logger import logger_geneartor

logger = logger_geneartor(__name__)

class Browser(ABC):
    @abstractmethod
    def get(self, url) -> str:
        """GET request to url and return the response data"""

class SeleniumBrowser(Browser):
    def __init__(self):
        self.driver = webdriver.Firefox()

    def get(self, url):
        self.driver.get(url)
        return self.driver.page_source

class RequestBrowser(Browser):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}
    
    def get(self, url):
        req = request.Request(url, headers=self.headers)
        logger.info(f"GET {url}")
        response = request.urlopen(req)
        data = response.read().decode()
        return data