import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display

import requests
import base64
import os

def update():
    #open json file
   
    curpath = os.path.dirname(os.path.realpath(__file__))
    propfile = os.path.join(curpath, 'props.json' ) 

    with open(propfile) as f:
        props = json.load(f)
 

    display = Display(visible=0, size=(800, 600))
    display.start()

    #configure webdriver
    driver = webdriver.Chrome()


    driver.get("https://www.optimum.net/pay-bill/account-activity")
    
    #get credentials from props file
    optimumID = props['optimumId']
    password = base64.b64decode(props['optimumPassword'].encode("ascii")).decode("ascii")

    #initialize optimumid and password fields

    idField = driver.find_element(By.ID,"loginPageUsername")
    passwordField = driver.find_element(By.ID, "loginPagePassword")
    
    #input credentials and press ENTER
    idField.send_keys(optimumID)
    passwordField.send_keys(password)
    passwordField.send_keys(Keys.RETURN)
    
    time.sleep(10)

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
    if 'XSRF-TOKEN' in cookies_dict:
        headers['X-XSRF-TOKEN'] = cookies_dict['XSRF-TOKEN']

       
    #get url response
    url = 'https://www.optimum.net/api/billpay/services/v1/billpay/summary?system=Portal'
    response = requests.get(url, headers=headers, cookies=cookies_dict)

    # Check if the request was successful
    if response.status_code == 200:
        billing_data = response.json()
        
        # Save the billing data to a JSON file
        #dump raw data
        with open(os.path.join(curpath, 'billing_data.json'), 'w') as json_file:
            json.dump(billing_data, json_file, indent=4)
        
        print("Billing data saved successfully.")
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)

    driver.quit()

    #convert to d3 format
        
    bills = []
    for bill in billing_data["getBillSummaryReturn"]["billStatements"]:
        d = datetime.strptime(bill['billCloseDate'], '%m/%d/%Y').strftime("%b '%y")
        bills.append({"month": d, "cost": bill["billAmount"]})

    if len(bills) > 12:
        bills = bills[len(bills)-12:]
        
    costs = {"costs":bills}

    with open(os.path.join(curpath, 'optimum_bills.json'), 'w') as json_file:
        json.dump(costs, json_file, indent=4)

   #print(json.dumps(costs, indent=4))