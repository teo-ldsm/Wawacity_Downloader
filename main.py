from plex_refresh import refresh
from config_loader import load
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


user_os = platform.system()


print("Initialising...")
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
print("Init OK !\n")


print("Connecting...")
driver.get("https://www.justgeek.fr/wawacity-91967/")
print("Connected !\n")

link = driver.find_element(By.XPATH, "//strong/a[contains(@href, \'https://www.wawacity.\')]")
link = link.text
print(f"Link : {link}")

print(f"Connecting to {link}...")
driver.get(f"https://{link}")
print(f"Connected !\n")

search = driver.find_element(By.NAME, "search")
search.send_keys(input("Quel est le titre du film que vous recherchez ?\n"))
search.submit()

liste_films = driver.find_elements(By.XPATH, "//div[@class=\'wa-sub-block-title\']/a")
for i in liste_films:
    print(i.text)



driver.close()
driver.quit()
