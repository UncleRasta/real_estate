import os
from selenium import webdriver
import pandas as pd
import requests
import datetime as dt
from datetime import date, timedelta
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import time
import pymysql
from time import sleep
import numpy as np

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized"); ## open Browser in maximized mode
chrome_options.add_argument("disable-infobars"); # disabling infobars
chrome_options.add_argument("--disable-extensions"); # disabling extensions//
chrome_options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
chrome_options.add_argument("--no-sandbox"); # Bypass OS security model

os.chmod('/Users/user/Downloads/chromedriver2', 755)

PATH = '/Users/user/Downloads/chromedriver2'
driver = webdriver.Chrome(PATH)#, options=chrome_options)

def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

for i in range(1, 3):
    try:
        os.remove("/Users/user/Downloads/offers.xlsx")
    except Exception as e:
        print("No such file!")

    #today = date.today()
    url = 'https://spb.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=offices&office_type%5B0%5D=3&office_type%5B1%5D=5&office_type%5B2%5D=6&office_type%5B3%5D=11&p=' + str(i) + '&region=2'
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div/div[5]/div/div/div/button[1]')))
            
    download_dir = r"/Users/user/Downloads/"

    enable_download_headless(driver, download_dir)
            
    sleep(2)
            
    driver.find_element_by_xpath('/html/body/div[5]/div/div[5]/div/div/div/button[1]')\
        .click()
            
    sleep(10)
    df_result = pd.read_excel('/Users/user/Downloads/offers.xlsx')
    print("Got new file!")
    if i == 1:
        df_result.to_csv('offers_cian.csv', header=True, index=False)
    else:
        df_result.to_csv('offers_cian.csv', mode='a', header=False)

driver.quit()
