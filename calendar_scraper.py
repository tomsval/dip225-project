from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


import config_parser

ORTUS_LOGIN_URL = "https://id2.rtu.lv/openam/UI/Login"
LOAD_TIMEOUT_SECS = 5


class CalendarScraper:
    def __init__(self):
        self.credentials: config_parser.ORTUSCredentials = config_parser.parse_config()

        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options, service=service)

        self.scrape()

    def scrape(self):
        self.login(self.credentials.username, self.credentials.password)
        self.navigate_schedule_page()
        self.download_schedule_file()

    def login(self, username: str, password: str):
        self.driver.get(ORTUS_LOGIN_URL)

        try:
            # "Lietotājvārds" lauks
            username_box_loaded = expected_conditions.presence_of_element_located(
                (By.XPATH, r'//*[@id="IDToken1"]')
            )

            # "Parole" lauks
            password_box_loaded = expected_conditions.presence_of_element_located(
                (By.XPATH, r'//*[@id="IDToken2"]')
            )

            # "Pieteikties" poga
            login_button_loaded = expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    r"/html/body/div[3]/div/div[1]/table/tbody/tr[3]/td[2]/input",
                )
            )

            # Gaida, kamēr nepieciešamie elementi ir pilnībā ielādējušies
            WebDriverWait(self.driver, LOAD_TIMEOUT_SECS).until(username_box_loaded)
            WebDriverWait(self.driver, LOAD_TIMEOUT_SECS).until(password_box_loaded)
            WebDriverWait(self.driver, LOAD_TIMEOUT_SECS).until(login_button_loaded)

            username_box = self.driver.find_element(By.XPATH, r'//*[@id="IDToken1"]')
            password_box = self.driver.find_element(By.XPATH, r'//*[@id="IDToken2"]')
            login_button = self.driver.find_element(
                By.XPATH, r"/html/body/div[3]/div/div[1]/table/tbody/tr[3]/td[2]/input"
            )

            username_box.clear()
            password_box.clear()

            username_box.send_keys(username)
            password_box.send_keys(password)

            login_button.click()
        except TimeoutError as err:
            self.driver.quit()
            print(
                f"Kļūda: ORTUS ielogošanās lapa '{ORTUS_LOGIN_URL}' lādējās pārāk ilgi: {err}"
            )

    def navigate_schedule_page(self):
        pass

    def download_schedule_file(self):
        pass
