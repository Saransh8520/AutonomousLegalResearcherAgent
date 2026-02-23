from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_web(query):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(f"https://www.google.com/search?q={query}")
    time.sleep(3)

    elements = driver.find_elements(By.TAG_NAME, "h3")
    text = "\n".join([e.text for e in elements[:5]])

    driver.quit()
    return text