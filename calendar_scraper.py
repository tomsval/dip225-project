from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import config_parser


class CalendarScraper:
    def __init__(self):
        self.credentials = config_parser.parse_config()
        self.scrape()

    def scrape(self):
        self.login(self.credentials.username, self.credentials.password)
        self.navigate_schedule_page()
        self.download_schedule_file()

    def login(self, username: str, password: str):
        pass

    def navigate_schedule_page(self):
        pass

    def download_schedule_file(self):
        pass
