from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import config
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Setting up web driver and opening COS page")
driver = webdriver.Chrome()
driver.get(config.COS_UTILITY_WEBSITE)

WebDriverWait(driver, timeout=10).until(lambda driver : driver.execute_script("return document.title"))
logging.info("Loaded page - %s" % driver.title)

logging.info("Finding login button")
app_buttons = driver.find_elements(by=By.CLASS_NAME, value="btn-app")
log_in_button = None
for button in app_buttons:
    if str.find(button.text, config.COS_UTILITY_LOGIN_TEXT) != -1:
        log_in_button = button
        break
assert log_in_button

logging.info("Clicking login button")
log_in_button.click()
WebDriverWait(driver, timeout=10).until(lambda driver : driver.execute_script("return document.title"))
logging.info("Loaded page - %s" % driver.title)

"""text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
value = message.text
print(value)"""

logging.info("Cleaning up webdriver")
driver.quit()