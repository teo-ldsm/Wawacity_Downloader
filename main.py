from plex_refresh import refresh
import config_loader
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


user_os = platform.system()

# TODO Faire un système pour skipper la config manuelle

print("Initialising...")
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
print("Init OK !\n")


print("Getting wawacity link...")
driver.get("https://www.justgeek.fr/wawacity-91967/")

link = driver.find_element(By.XPATH, "//strong/a[contains(@href, \'https://www.wawacity.\')]")
link = link.text
print(f"Link found : {link}\n")

print(f"Connecting to {link}...")
driver.get(f"https://{link}")
print(f"Connected !\n")

search = driver.find_element(By.NAME, "search")
search.send_keys(input("Quel est le titre du film que vous recherchez ?\n"))
search.submit()

liste_resultats = driver.find_elements(By.XPATH, "//div[@class=\'wa-sub-block-title\']/a")
index_resultat = dict()
for i in liste_resultats:
    title = i.text[:i.text.index(" [")]
    print(title)
    index_resultat[title] = i

driver.close()
driver.quit()
