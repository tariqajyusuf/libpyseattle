"""Main API object used for executing any calls to city systems."""

import logging
import tempfile

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from libpyseattle.sso import config


class API:
    def __init__(self, username: str = "", password: str = ""):
        logging.info("Setting up web driver")
        self.username = username
        self.password = password
        self.downloads = tempfile.TemporaryDirectory()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.experimental_options["prefs"] = {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": self.downloads.name,
        }

        # Classic headless mode uses a different code implementation which
        # limits some features. We need to use the new implementation which has
        # a more standardized implementation.
        #
        # See: https://developer.chrome.com/articles/new-headless/
        chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        """Clean up driver and temporary files."""
        logging.info("Cleaning up")
        self.driver.quit()
        self.downloads.cleanup()

    def get_authenticated(self, dest_url: str = config.COS_LOGIN_URL) -> bool:
        """Get destination URL and handle authentication.

        Args:
            dest_url (str): The URL to authenticate and navigate towards.
                Defaults to the City of Seattle login page.

        Returns:
            bool: Whether we could navigate and authenticate the given URL.
        """
        logging.info("Loading %s", dest_url)
        # TODO make sure we deal with the already authenticated case.
        self.driver.get(dest_url)
        try:
            WebDriverWait(self.driver, timeout=10).until(
                lambda driver: driver.find_element(
                    by=By.NAME, value=config.COS_LOGIN_USERNAME
                )
            )
        except (NoSuchElementException, TimeoutException):
            return True

        user_textbox = self.driver.find_element(
            by=By.NAME, value=config.COS_LOGIN_USERNAME
        )
        pass_textbox = self.driver.find_element(
            by=By.NAME, value=config.COS_LOGIN_PASSWORD
        )
        user_textbox.send_keys(self.username)
        pass_textbox.send_keys(self.password)
        submit_button = self.driver.find_element(by=By.CSS_SELECTOR, value="button")
        current_url = self.driver.current_url
        submit_button.click()
        print(current_url)

        # Form submits asynchronously so we need to wait.
        try:
            WebDriverWait(self.driver, timeout=10).until(
                lambda _: current_url != self.driver.current_url
            )
            return True
        except NoSuchElementException:
            print(self.driver.current_url)
            print(
                self.driver.find_element(
                    by=By.CLASS_NAME, value=config.COS_LOGIN_ALERT
                ).text
            )
            return False
