from getpass import getpass
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import config
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Setting up web driver and opening COS page")
driver = webdriver.Chrome()
driver.get(config.COS_UTILITY_USAGE_SITE)

WebDriverWait(driver, timeout=10).until(lambda driver : driver.execute_script("return document.title"))
logging.info("Loaded page - %s" % driver.title)

print("Please log in to your City of Seattle Account")
username = str(input("Username: "))
password = str(getpass("Password: "))

user_textbox = driver.find_element(by=By.NAME, value="userName")
pass_textbox = driver.find_element(by=By.NAME, value="password")
user_textbox.send_keys(username)
pass_textbox.send_keys(password)
print("Logging in...")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
submit_button.click()

# We need to do a bit of a pause because the form submit is asynchronous.
title = driver.title
WebDriverWait(driver, timeout=10).until(lambda driver : title != driver.title)
WebDriverWait(driver, timeout=10).until(lambda driver : driver.find_element(by=By.XPATH, value="//button[text() = 'Daily']"))
driver.find_element(by=By.XPATH, value="//button[text() = 'Daily']").click()
logging.info("Loaded page - %s" % driver.title)

WebDriverWait(driver, timeout=10).until(lambda driver : driver.find_element(by=By.XPATH, value="//input[@placeholder = 'End Date']"))
end_date = driver.find_element(by=By.XPATH, value="//input[@placeholder = 'End Date']")
logging.info("Loaded page - %s" % driver.title)
print(end_date.get_attribute("value"))

"""text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
value = message.text
print(value)"""

logging.info("Cleaning up webdriver")
driver.quit()