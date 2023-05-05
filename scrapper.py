from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import time
import os
from dotenv import load_dotenv

load_dotenv()


def scrapper(username_text, password_text, hashtag, time_period_scrapping):

    browser_driver_path = os.getenv('CHROME_DRIVER_PATH')
    driver = webdriver.Chrome(executable_path=browser_driver_path)
    # This instance will be used to log into LinkedIn
    
    driver.get("https://linkedin.com/uas/login")
    
    time.sleep(5)
    username = driver.find_element(By.ID, "username")
    print(password_text)

    username.send_keys(username_text) 
    
    pword = driver.find_element(By.ID, "password")

    pword.send_keys(password_text)       

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    if time_period_scrapping == 'past 24 hrs':
        hashtag_url = f"https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=%23{hashtag}"        

    elif time_period_scrapping == 'past week':
        hashtag_url = f"https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=%23{hashtag}"

    elif time_period_scrapping == 'past month':
        hashtag_url = f"https://www.linkedin.com/search/results/content/?datePosted=%22past-month%22&keywords=%23{hashtag}"

    else:
        hashtag_url = f"https://www.linkedin.com/search/results/content/?keywords=%23{hashtag}&postedBy=%5B%22following%22%5D"


    driver.get(hashtag_url)

    start = time.time()
    
    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000
    
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000

        time.sleep(3)
    
        end = time.time()
    
        # We will scroll for 20 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > 20:
            break

    src = driver.page_source

    with open('file_new.html','w',encoding='utf-8') as f:
        f.write(src)
