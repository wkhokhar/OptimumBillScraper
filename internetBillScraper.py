import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import requests

#open json file
with open('props.json') as f:
    props = json.load(f)

#configure webdriver
driver = webdriver.Chrome()

#configure webdriver for RASBERRY_PI os only:
#sudo apt install chromium-browser chromium-chromedriver python3-venv
#need to run venv and install selenium
'''
service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service)
'''

driver.get("https://www.optimum.net/pay-bill/account-activity")

#get credentials from props file
optimumID = props['optimumID']
password = props['optimumPassword']

#initialize optimumid and password fields

idField = driver.find_element(By.ID,"loginPageUsername")
passwordField = driver.find_element(By.ID, "loginPagePassword")
#input credentials and press ENTER
idField.send_keys(optimumID)
passwordField.send_keys(password)
passwordField.send_keys(Keys.RETURN)

time.sleep(5)

#get browser info and cookies
cookies = driver.get_cookies()
cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
user_agent = driver.execute_script("return navigator.userAgent;")


# Prepare headers
headers = {
    'User-Agent': user_agent,
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://www.optimum.net/pay-bill/account-activity/',
    'X-Requested-With': 'XMLHttpRequest'
}

# Include the XSRF token in headers if present in cookies
for cookie in cookies:
    if cookie['name'] == 'XSRF-TOKEN':
        headers['X-XSRF-TOKEN'] = cookie['value']
        break

#get url response
url = 'https://www.optimum.net/api/billpay/services/v1/billpay/summary?system=Portal'
response = requests.get(url, headers=headers, cookies=cookies_dict)

# Check if the request was successful
if response.status_code == 200:
    billing_data = response.json()
    
    # Save the billing data to a JSON file
    with open('billing_data.json', 'w') as json_file:
        json.dump(billing_data, json_file, indent=4)
    
    print("Billing data saved successfully.")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)

driver.quit()

#print bill amounts in order of oldest to most recent.
with open("billing_data.json") as bd:
    billingData = json.load(bd)
    
bills = []
for bill in billingData["getBillSummaryReturn"]["billStatements"]:
    bills.append(bill["billAmount"])
print(bills)