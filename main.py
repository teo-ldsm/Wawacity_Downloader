from plex_refresh import refresh
import config_loader
import threading
from flask import Flask, request
import time
import platform
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# TODO Faire un try pour vérifier si tt les bibliothèques ont la


user_os = platform.system()

# TODO Faire un système pour skipper la config manuelle

print("Initialising...")
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
print(f"{Fore.GREEN}Init OK !{Style.RESET_ALL}\n")


print("Getting wawacity link...")
driver.get("https://www.justgeek.fr/wawacity-91967/")

lien_wawacity = driver.find_element(By.XPATH, "//strong/a[contains(@href, \'https://www.wawacity.\')]")
lien_wawacity = lien_wawacity.text
print(f"{Fore.GREEN}Link found : {lien_wawacity}{Style.RESET_ALL}\n")

print(f"Connecting to {lien_wawacity}...")
driver.get(f"https://{lien_wawacity}")
print(f"{Fore.GREEN}Connected !{Style.RESET_ALL}\n")

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

    if len(liste_resultats) == 0:
        print(f"\n{Fore.RED}Aucun résultat trouvé. {Style.RESET_ALL}\n")
        time.sleep(5)
        exit()

    choix_valide = False
    rep = None
    while not choix_valide:
        try:
            rep = eval(input("\nEntrez le numéro correspondant a votre résultat. "
                             "Si il ne s'y trouve pas, entrez 0\n"))
            if not isinstance(rep, int):
                raise TypeError("La variable rep doit être de type int")
            choix_valide = True

        except:
            print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_liens)}{Style.RESET_ALL}")
            choix_valide = False

        else:
            if 0 <= rep <= len(index_liens):
                choix_valide = True
            else:
                print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 0 et {len(index_liens)}{Style.RESET_ALL}")
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


lien_page_film = recup_results()

driver.get(lien_page_film)

liste_qualites = driver.find_elements(By.XPATH, "//ul[@class=\'wa-post-list-ofLinks row readable-post-list\']/li/a")


liens_qualites = dict()
for i in liste_qualites:
    liens_qualites[i.text] = i.get_attribute("href")

liens_qualites[driver.find_element(By.XPATH, "//*[@id=\'detail-page\']/div[2]/div[1]/i[2]").text] = None

# TODO créer un truc qui skip ce bloc si la qualité est définie dans config.txt

print("\nVoici les qualités disponible pour votre film\n")

index_qualites = []
n = 1
for i in liens_qualites:
    print(f"{n} : {i}")
    index_qualites.append(i)
    n += 1


choix_valide = False
rep = None
while not choix_valide:
    try:
        rep = eval(input("\nEntrez le numéro correspondant a votre résultat.\n"))
        if not isinstance(rep, int):
            raise TypeError("La variable rep doit être de type int")
        choix_valide = True

    except:
        print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_qualites)}{Style.RESET_ALL}")
        choix_valide = False

    else:
        if 1 <= rep <= len(index_qualites):
            choix_valide = True
        else:
            print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_qualites)}{Style.RESET_ALL}")
            choix_valide = False

lien_page_film = liens_qualites[index_qualites[rep - 1]]


if lien_page_film is not None:
    driver.get(lien_page_film)


liste_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[2]")
liste_liens_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[1]/a")

liens_sites = {liste_sites[i].text: liste_liens_sites[i].get_attribute("href") for i in range(len(liste_sites)) \
               if liste_sites[i].text in ("1fichier", "Uptobox")}


print("Voici les sites de téléchargements disponibles")
n = 1
index_sites = []
for i in liens_sites:
    print(f"{n} : {i}")
    index_sites.append(i)
    n += 1

choix_valide = False
rep = None
while not choix_valide:
    try:
        rep = eval(input("\nEntrez le numéro correspondant au site que vous souhaitez utiliser.\n"))
        if not isinstance(rep, int):
            raise TypeError("La variable rep doit être de type int")
        choix_valide = True

    except:
        print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_sites)}{Style.RESET_ALL}")
        choix_valide = False

    else:
        if 1 <= rep <= len(index_sites):
            choix_valide = True
        else:
            print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_sites)}{Style.RESET_ALL}")
            choix_valide = False


dl_site = index_sites[rep - 1]
lien_page_captcha = liens_sites[dl_site]


print(f"\n\n{Fore.LIGHTBLUE_EX}##################\n"
      f"L\'accès au téléchargement nécessite la validation d'un captcha.\n"
      f"Ouvrez l'application Captcha Skipper sur votre téléphone pour continuer.{Style.RESET_ALL}\n"
      f"##################\n")

new_url = ""

app = Flask(__name__)


@app.route('/get_url')
def get_url():
    print(f"{Fore.GREEN}Le lien a été transmis à l'application mobile{Style.RESET_ALL}")
    return lien_page_captcha


@app.route('/upload_url', methods=['POST'])
def upload_url():
    global new_url
    new_url = request.form.get('url')

    print(f"{Fore.GREEN}New URL received: {new_url}{Style.RESET_ALL}")
    # Arrête le serveur Flask
    shutdown_server()

    return 'OK'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


app.run(host="0.0.0.0", port=5000)


print(f"{Fore.GREEN}Le captcha a été passé avec succès !{Style.RESET_ALL}\n\n"
      f"Connecting to {new_url}")

driver.get(new_url)

if dl_site == "1fichier":

    btn = driver.find_element(By.ID, "dlb")
    btn.submit()

    btn = driver.find_element(By.CLASS_NAME, "ok btn-general btn-orange") # TODO Il trouve pas ici et il renvoie une erreur
    lien_film = btn.get_attribute("href")


print(lien_film)


driver.close()
driver.quit()
