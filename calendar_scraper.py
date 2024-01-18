from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

import requests

import config_parser

ORTUS_LOGIN_URL = "https://id2.rtu.lv/openam/UI/Login"
LOAD_TIMEOUT_SECS = 20


class CalendarScraper:
    def __init__(self):
        self.credentials: config_parser.ORTUSCredentials = config_parser.parse_config()

        service = Service(ChromeDriverManager().install())
        options = Options()
        # options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options, service=service)

        self.scrape()
        self.driver.quit()

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

            if self.driver.title == "ORTUS (Neveiksmīga autentifikācija)":
                raise ValueError(
                    "Kļūda ORTUS autentifikācijā. Lūdzu pārbaudiet, vai lietotājvārds un/vai parole ir pareiza."
                )

        except TimeoutError as err:
            self.driver.quit()
            print(
                f"Kļūda: ORTUS ielogošanās lapa '{ORTUS_LOGIN_URL}' lādējās pārāk ilgi: {err}"
            )

    def navigate_schedule_page(self):
        try:
            studentiem_span_xpath = (
                r"/html/body/div[1]/div/div[2]/div[1]/ul/li[2]/a/span"
            )

            grafiki_span_xpath = (
                r"/html/body/div[1]/div/div[2]/div[2]/ul/li[3]/a[1]/span"
            )

            studentiem_span_loaded = expected_conditions.presence_of_element_located(
                (By.XPATH, studentiem_span_xpath)
            )

            WebDriverWait(self.driver, LOAD_TIMEOUT_SECS).until(studentiem_span_loaded)

            studentiem_span = self.driver.find_element(By.XPATH, studentiem_span_xpath)
            studentiem_span.click()

            grafiki_span_loaded = expected_conditions.presence_of_element_located(
                (By.XPATH, grafiki_span_xpath)
            )
            WebDriverWait(self.driver, LOAD_TIMEOUT_SECS).until(grafiki_span_loaded)

            grafiki_span = self.driver.find_element(By.XPATH, grafiki_span_xpath)

            grafiki_span.click()
        except TimeoutError as err:
            self.driver.quit()
            print(
                f"Kļūda: ORTUS ielogošanās lapa '{ORTUS_LOGIN_URL}' lādējās pārāk ilgi: {err}"
            )

    def download_schedule_file(self):
        try:
            ical_download_a_xpath = r"/html/body/div[1]/div/div[4]/div[1]/div/div[4]/div/div[1]/div[2]/div/div[3]/div[1]/div/div[2]/p[4]/a"

            ical_download_a_loaded = expected_conditions.presence_of_element_located(
                (By.XPATH, ical_download_a_xpath)
            )

            WebDriverWait(self.driver, LOAD_TIMEOUT_SECS).until(ical_download_a_loaded)

            ical_download_a = self.driver.find_element(By.XPATH, ical_download_a_xpath)

            ical_url = ical_download_a.get_attribute("href")

            # Lai saglabātu sesiju starp Selenium un lejupielādēšanas veikšanu vajag saglabāt Selenium cookies
            selenium_session_cookies = self.driver.get_cookies()

            # Nepieciešams pārveidot Selenium sniegtos cookies requests bibliotēkas lasāmā formātā
            session_cookies = {}
            for cookie in selenium_session_cookies:
                session_cookies[cookie["name"]] = cookie["value"]

            try:
                ical_url_response = requests.get(
                    ical_url,
                    cookies=session_cookies,
                    timeout=LOAD_TIMEOUT_SECS,
                )
                ical_url_response.raise_for_status()

                with open("grafiks.ics", mode="wb") as f:
                    f.write(ical_url_response.content)

            except requests.exceptions.RequestException as err:
                self.driver.quit()
                print(f"Kļūda HTTP pieprasījuma veikšanā: {err}")

        except TimeoutError as err:
            self.driver.quit()
            print(
                f"Kļūda: ORTUS ielogošanās lapa '{ORTUS_LOGIN_URL}' lādējās pārāk ilgi: {err}"
            )
