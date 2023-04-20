from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

print("Initialising...")
options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
print("Init OK !\n")

driver.get("https://dl-protect.link/80722917?fn=VGhvciA6IExlIE1vbmRlIGRlcyB0w6luw6hicmVzIFtIRExJR0hUIDEwODBwXSAtIE1VTFRJIChUUlVFRlJFTkNIKQ%3D%3D&rl=a2")

