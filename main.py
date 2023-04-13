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


def recup_results():
    liste_resultats = driver.find_elements(By.XPATH, "//div[@class=\'wa-sub-block-title\']/a")
    liens_resultats = dict()
    for i in liste_resultats:
        title = i.text[:i.text.index(" [")]
        liens_resultats[title] = i.get_attribute("href")

    print("\nVoici les résultats\n")
    index_liens = []
    n = 1
    for i in liens_resultats:
        print(f"{n} : {i}")
        index_liens.append(i)
        n += 1

    choix_valide = False
    rep = None
    while not choix_valide:
        try:
            rep = eval(input("\nEntrez le numéro correspondant a votre résultat. Si il ne s'y trouve pas, entrez 0\n"))
            if not isinstance(rep, int):
                raise TypeError("La variable rep doit être de type int")
            choix_valide = True

        except:
            print(f"Réponse invalide, entrez un chiffre entre 1 et {len(index_liens)}")
            choix_valide = False

        else:
            if 0 <= rep <= len(index_liens):
                choix_valide = True
            else:
                print(f"Réponse invalide, entrez un chiffre entre 0 et {len(index_liens)}")
                choix_valide = False

    if rep == 0:
        bnt_next = driver.find_element(By.XPATH, "//div[@class=\'text-center\']/ul[@class=\'pagination\']/li[15]/a")
        next_page = bnt_next.get_attribute("href")
        driver.get(next_page)
        print("\n\nRecherche des résultats sur la page suivante : \n")
        lien = recup_results()

    else:
        lien = liens_resultats[index_liens[rep - 1]]

    return lien


lien = recup_results()

print(lien)





driver.close()
driver.quit()
