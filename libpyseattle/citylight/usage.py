"""Utility module to retrieve data from Seattle City Light."""

import csv
import datetime
from datetime import date
import glob
import logging
import os

from dateutil.parser import parse

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from libpyseattle.sso import api
from libpyseattle.citylight import config


class SeattleCityLight:
    """A helper class to download usage data from Seattle City Light."""

    def __init__(self, seattle_api: api.API):
        """Set up the necessary selenium components for accessing SCL."""
        self._api = seattle_api

    def get_recent_usage(self, window: int = 30):
        """Get the energy usage of the specified user over the past n days.

        Args:
            window (int): The number of days to look back. Defaults to 30.

        Returns:
            dict[date, float]: A dictionary with usage records.
        """
        if not self._api.get_authenticated(config.COS_UTILITY_USAGE_SITE):
            raise Exception("Could not authenticate.")

        WebDriverWait(self._api.driver, timeout=10).until(
            lambda driver: driver.find_element(
                by=By.XPATH, value=config.COS_UTILITY_USAGE_DAILY
            )
        )
        self._api.driver.find_element(
            by=By.XPATH, value=config.COS_UTILITY_USAGE_DAILY
        ).click()

        WebDriverWait(self._api.driver, timeout=10).until(
            lambda driver: driver.find_element(
                by=By.CLASS_NAME, value=config.COS_UTILITY_USAGE_GRAPH
            )
        )
        end_date = self._api.driver.find_element(
            by=By.XPATH, value=config.COS_UTILITY_USAGE_END_DATE
        )
        start_date = self._api.driver.find_element(
            by=By.XPATH, value=config.COS_UTILITY_USAGE_START_DATE
        )
        logging.info("Getting energy usage from the last 30 days")

        # The city only provides data on a daily basis except today.
        old_value = end_date.get_attribute("value")
        end_date.clear()
        end_date.send_keys(
            (date.today() - datetime.timedelta(days=1)).strftime("%m-%d-%Y")
        )
        start_date.clear()
        start_date.send_keys(
            (date.today() - datetime.timedelta(days=window)).strftime("%m-%d-%Y")
        )
        WebDriverWait(self._api.driver, timeout=10).until(
            lambda driver: end_date.get_attribute("value") != old_value
        )
        self._api.driver.find_element(
            by=By.XPATH, value="//button[text() = 'Update']"
        ).click()
        WebDriverWait(self._api.driver, timeout=10).until(
            lambda driver: driver.find_element(
                by=By.CLASS_NAME, value="fusioncharts-container"
            )
        )

        logging.info("Downloading data")
        expected_file_glob = self._api.downloads.name + os.path.sep + "*.csv"
        self._api.driver.find_element(by=By.LINK_TEXT, value="Download").click()
        WebDriverWait(self._api.driver, timeout=10).until(
            lambda driver: glob.glob(expected_file_glob)
        )

        logging.info("Data downloaded\n")
        usage: dict[date, float] = {}
        with open(glob.glob(expected_file_glob)[0], "r", encoding="ascii") as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=",", fieldnames=config.COS_CSV_SCHEMA
            )

            # Skip two lines because there are special headers.
            next(reader)
            next(reader)

            for row in reader:
                day = parse(row[config.COS_CSV_DATE_HEADER]).date()
                usage[day] = float(row[config.COS_CSV_CONSUMPTION_HEADER])
        os.remove(glob.glob(expected_file_glob)[0])

        return usage
