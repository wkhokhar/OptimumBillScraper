import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


with open('props.json') as f:
    props = json.load(f)
driver = webdriver.Chrome()
driver.get("https://www.optimum.net/")
optimumID = props['optimumID']
password = props['optimumPassword']
idField = driver.find_element(By.ID,"homeLoginFormOptimumId")
passwordField = driver.find_element(By.ID, "homeLoginFormPassword")
idField.send_keys(optimumID)
passwordField.send_keys(password)
passwordField.send_keys(Keys.RETURN)
time.sleep(15)
driver.quit()