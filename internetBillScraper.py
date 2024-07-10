import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#open json file
with open('props.json') as f:
    props = json.load(f)

#configure webdriver
driver = webdriver.Chrome()
driver.get("https://www.optimum.net/")

#get credentials from props file
optimumID = props['optimumID']
password = props['optimumPassword']

#initialize optimumid and password fields
idField = driver.find_element(By.ID,"homeLoginFormOptimumId")
passwordField = driver.find_element(By.ID, "homeLoginFormPassword")

#input credentials and press ENTER
idField.send_keys(optimumID)
passwordField.send_keys(password)
passwordField.send_keys(Keys.RETURN)

time.sleep(15)
driver.quit()