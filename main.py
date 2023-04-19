import datetime
from datetime import date
from getpass import getpass
import glob
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import tempfile
import config
import logging

print("Please log in to your City of Seattle Account")
username = str(input("Username: "))
password = str(getpass("Password: "))

logging.info("Setting up web driver")
download_directory = tempfile.TemporaryDirectory()
chrome_options = webdriver.ChromeOptions()
chrome_options.experimental_options["prefs"] = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory': download_directory.name
}
driver = webdriver.Chrome(options=chrome_options)

print("Logging in...")
driver.get(config.COS_UTILITY_USAGE_SITE)
WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.execute_script("return document.title"))

user_textbox = driver.find_element(by=By.NAME, value="userName")
pass_textbox = driver.find_element(by=By.NAME, value="password")
user_textbox.send_keys(username)
pass_textbox.send_keys(password)
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
submit_button.click()

# We need to do a bit of a pause because the form submit is asynchronous.
title = driver.title
WebDriverWait(driver, timeout=10).until(lambda driver: title != driver.title)
WebDriverWait(driver, timeout=10).until(lambda driver: driver.find_element(
    by=By.XPATH, value="//button[text() = 'Daily']"))
driver.find_element(by=By.XPATH, value="//button[text() = 'Daily']").click()

WebDriverWait(driver, timeout=10).until(lambda driver: driver.find_element(
    by=By.CLASS_NAME, value="fusioncharts-container"))
end_date = driver.find_element(
    by=By.XPATH, value="//input[@placeholder = 'End Date']")
start_date = driver.find_element(
    by=By.XPATH, value="//input[@placeholder = 'Start Date']")
print("Getting energy usage from the last 30 days")

# The city only provides data on a daily basis except today.
old_value = end_date.get_attribute("value")
end_date.clear()
end_date.send_keys((date.today() - datetime.timedelta(days=1)
                    ).strftime("%m-%d-%Y"))
start_date.clear()
start_date.send_keys((date.today() - datetime.timedelta(days=30)
                      ).strftime("%m-%d-%Y"))
WebDriverWait(driver, timeout=10).until(
    lambda driver: end_date.get_attribute("value") != old_value)
driver.find_element(by=By.XPATH, value="//button[text() = 'Update']").click()
WebDriverWait(driver, timeout=10).until(
    lambda driver: driver.find_element(by=By.CLASS_NAME,
                                       value="fusioncharts-container"))

print("Downloading data")
driver.find_element(by=By.LINK_TEXT, value="Download").click()
print(download_directory.name + os.path.sep + "*.xls")
WebDriverWait(driver, timeout=10).until(
    lambda driver: glob.glob(download_directory.name + os.path.sep + "*.csv"))

print("Data downloaded\n")
print(open
      (glob.glob(download_directory.name + os.path.sep + "*.csv")[0], "r"
       ).read())

logging.info("Cleaning up")
driver.quit()
