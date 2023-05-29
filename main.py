from config_loader import *

if __name__ == '__main__':
    venv_init()

if os.name == 'nt':
    import winreg

import json
import pathlib
import subprocess
import requests
import time
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import wget


version = "v1.0.0-beta"

if os.name == 'nt':  # Windows
    os.system('cls')
else:  # Linux, Mac OS X
    os.system('clear')

args = sys.argv
args = [arg.upper() for arg in args]

config = load()

if "DEBUG" in args:
    class Fore:
        BLACK = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""
        RESET = ""
        LIGHTBLACK_EX = ""
        LIGHTRED_EX = ""
        LIGHTGREEN_EX = ""
        LIGHTYELLOW_EX = ""
        LIGHTBLUE_EX = ""
        LIGHTMAGENTA_EX = ""
        LIGHTCYAN_EX = ""
        LIGHTWHITE_EX = ""


    class Style:
        RESET_ALL = ""

else:
    from colorama import Fore, Style


print("\n\n\nVérification des mises a jour ...\n\n")
api_url = 'https://api.github.com/repos/teo-ldsm/Wawacity_Downloader/releases/latest'
response = requests.get(api_url)
latest_realease = json.loads(response.text)
latest_version = latest_realease["tag_name"]

if latest_version != version:
    rep = demande(f'Une nouvelle version est disponible: {latest_version}. Voulez vous la télécharger ?\n')

    if rep in ("OUI", "O"):
        package_url = None
        for asset in latest_realease['assets']:
            if asset["name"].startswith("WawacityDownloader"):
                package_url = asset["browser_download_url"]
                break

        if package_url is not None:
            parent_dir = str(pathlib.Path(__file__).parent.parent.absolute())
            package_name = wget.detect_filename(package_url)
            print(f"\nDébut du téléchargement depuis {package_url}\n")

            wget.download(package_url, out=f"{parent_dir}\\{package_name}")

            input(f"\n\nVotre fichier a été téléchargé ici : {parent_dir}\\{package_name}\n"
                  f"Vous pouvez supprimer cette version et extraire la nouvelle a la place\n"
                  f"{Fore.LIGHTYELLOW_EX}Attention ! Pensez à sauvegarder le contenu de config.txt !{Style.RESET_ALL}\n"
                  f"Appuyez sur Entrer pour quitter ...")
            exit(0)

        else:
            input("Une erreur est survenue durant la recherche de mise à jour\n"
                  "Vous pouvez télécharger manuellement la mise a jour ici : "
                  "\"https://github.com/teo-ldsm/Wawacity_Downloader/releases/\"\n"
                  "Appuyez sur Entrer pour quitter ...")
            exit(1)

else:
    print(f"\n{Fore.GREEN}Le programme est a jour.{Style.RESET_ALL}\n\n")

# TODO Faire un try pour vérifier si tt les bibliothèques sont la

# TODO Faire un système pour skipper la config manuelle


# TODO Verifier que chrome est installé
print(f"Initialising...\n{Fore.BLACK}")
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--lang=fr')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,
                          service_log_path="./venv/Lib/site-packages/webdriver_manager/log.txt",
                          )
driver.implicitly_wait(10)
print(f"{Fore.GREEN}Init OK !\n{Style.RESET_ALL}")

prgm_dir = str(pathlib.Path(__file__).parent.absolute())
dl_dir = prgm_dir

rep = demande(f"Par défaut, les films seront téléchargés dans le dossier \"{dl_dir}\". "
              f"Voulez vous changer ?")

if rep in ("OUI", "O"):

    choix_valide = False
    while not choix_valide:
        dl_dir = input(f"Entrez le chemin d'accès complet du dossier dans "
                       f"lequel vous souhaitez télécharger les films.\n")
        if os.path.exists(dl_dir.replace("\\", "/")):
            choix_valide = True
        else:
            print(f"{Fore.RED}Réponse invalide. Le chemin d'accès n'existe pas\n{Style.RESET_ALL}"
                  f"Le chemin doit être sous cette forme : \"C:\\Users\\Fabrice\\Downloads\" par exemple\n")

# TODO Faire un try qui utilise l'adresse wawacity stockée dans config. Si ça marche pas il va la chercher sur le site


def connect_to_wawacity(link):
    try:
        print(f"\n\nConnecting to {lien_wawacity} ...{Fore.BLACK}")
        driver.get(f"https://{link}")
    except:
        print(f"\n\n{Fore.RED}Une erreur est survenue durant la connexion au site{Style.RESET_ALL}\n"
              f"Wawacity est contraint de changer d'adresse régulièrement. Il est possible que le site ai changé "
              f"d'adresse dans les dernières heures.\n"
              f"L'adresse {link} n'est donc plus valide.\n"
              f"Vous pouvez essayer de chercher manuellement la nouvelle adresse du site sur internet\n")

        rep = input(f"Entrez la nouvelle adresse du site ici ou entrez \"exit\" pour quitter ...\n")

        if rep.upper() == "EXIT":
            exit(0)
        else:
            connect_to_wawacity(rep)


try:
    lien_wawacity = config['ADDRESS']
    print(f"\n\nConnecting to {lien_wawacity} ...\n{Fore.BLACK}")
    driver.get(f"https://{lien_wawacity}")

except:
    print(f"{Style.RESET_ALL}\n\nLien invalide\n"
          f"Récupération du nouveau lien ...{Fore.BLACK}")
    driver.get("https://fulldeals.fr/wawacity-adresse-officielle-site-films-series-gratuits/.html")

    lien_wawacity = driver.find_element(By.XPATH, "//strong/a[contains(@href,\'https://www.wawacity.\')]")
    lien_wawacity = lien_wawacity.text

    print(f"{Fore.GREEN}Lien trouvé : {lien_wawacity}{Style.RESET_ALL}\n")

    connect_to_wawacity(lien_wawacity)

    fill_config(address=lien_wawacity, manual=False)

print(f"{Fore.GREEN}Connected !{Fore.BLACK}\n")

search = driver.find_element(By.NAME, "search")
search.send_keys(input(f"{Style.RESET_ALL}\n\nQuel est le titre du film que vous recherchez ?\n"))
print(Fore.BLACK)
search.submit()


def recup_results(num_page):
    liste_resultats = driver.find_elements(By.XPATH, "//div[@class=\'wa-sub-block-title\']/a")
    liens_resultats = dict()
    for i in liste_resultats:
        title = i.text[:i.text.index(" [")]
        liens_resultats[title] = i.get_attribute("href")

    print(f"{Fore.GREEN}\nVoici les résultats\n{Style.RESET_ALL}")
    index_liens = []
    n = 1
    for i in liens_resultats:
        print(f"{n} : {i}")
        index_liens.append(i)
        n += 1

    if len(liste_resultats) == 0:
        input(f"\n{Fore.RED}Aucun résultat trouvé.\n"
              f"{Style.RESET_ALL}Appuyez sur Entrer pour quitter...")
        exit(1)

    choix_valide = False
    rep = None
    while not choix_valide:
        try:
            rep = eval(input(f"\nEntrez le numéro correspondant a votre résultat. "
                             f"Si il ne s'y trouve pas, entrez 0\n"))
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
    lien = ""
    if rep == 0:
        try:
            print(Fore.BLACK)
            if num_page == 1:
                next_page = driver.current_url + f"&page={num_page+1}"
            else:
                next_page = driver.current_url.replace(f"page={num_page}", f"page={num_page+1}")
            driver.get(next_page)
        except:
            input(f"{Fore.RED}Vous avez atteint la dernière page.{Style.RESET_ALL}\n"
                  f"Essayez de relancer la recherche avec une orthographe différente.\n"
                  f"Appuyez sur Entrer pour quitter ...")
        else:
            print(f"{Style.RESET_ALL}\n\nRecherche des résultats sur la page {num_page+1} : \n")
            lien = recup_results(num_page+1)

    else:
        lien = liens_resultats[index_liens[rep - 1]]

    return lien


lien_page_film = recup_results(1)

driver.get(lien_page_film)

liste_qualites = driver.find_elements(By.XPATH, "//ul[@class=\'wa-post-list-ofLinks row readable-post-list\']/li/a")


liens_qualites = dict()
for i in liste_qualites:
    liens_qualites[i.text] = i.get_attribute("href")

liens_qualites[driver.find_element(By.XPATH, "//*[@id=\'detail-page\']/div[2]/div[1]/i[2]").text] = None

# TODO créer un truc qui skip ce bloc si la qualité est définie dans config.txt

print(f"\nVoici les qualités disponible pour votre film\n")

index_qualites = []
n = 1
for i in liens_qualites:
    print(f"{n} : {i}")
    index_qualites.append(i)
    n += 1


print("\n\nSi la qualité que vous souhaitez ne se trouve pas dans la liste, fermez le programme \n"
      "et relancez le en cherchant le titre de votre films dans une autre langue\n"
      "Exemple: Cherchez \"Avengers - l'Ère d'Ultron\" au lieu de \"Avengers - Age of Ultron\"")

choix_valide = False
rep = None
while not choix_valide:
    try:
        rep = eval(input(f"\nEntrez le numéro correspondant a votre résultat.\n"))
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


print(Fore.BLACK)

if lien_page_film is not None:
    driver.get(lien_page_film)


liste_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[2]")
liste_liens_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[1]/a")

liens_sites = {liste_sites[i].text: liste_liens_sites[i].get_attribute("href") for i in range(len(liste_sites))
               if liste_sites[i].text in ("1fichier", "Uptobox") and "Partie" not in liste_liens_sites[i].text}

# TODO Régler le problème de Uptobox


print(f"{Style.RESET_ALL}Voici les sites de téléchargements disponibles\n")
n = 1
index_sites = []
for i in liens_sites:
    print(f"{n} : {i}")
    index_sites.append(i)
    n += 1

print(f"\n{Fore.LIGHTYELLOW_EX}Le site Uptobox est désactivé à cause d'un bug{Style.RESET_ALL}\n")  # TODO Enlever ça

choix_valide = False
rep = None
while not choix_valide:
    try:
        rep = eval(input(f"\nEntrez le numéro correspondant au site que vous souhaitez utiliser.\n"))
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

print(f"\n\n{Fore.LIGHTCYAN_EX}############################################################################\n"
      f"L\'accès au téléchargement nécessite la validation d'un captcha.\n"
      "Vous devez valider ce captcha manuellement.\n"
      f"############################################################################\n\n{Style.RESET_ALL}")

choix_valide = False
methode = None
while not choix_valide:
    methode = input(f"Entrez 1 pour résoudre le captcha avec l'application android Captcha skipper\n"
                    f"Entrez 2 pour résoudre le captcha depuis une fenêtre chrome\n\n"
                    f"{Fore.LIGHTYELLOW_EX}Attention ! La methode 2 ne fonctionne que sur Windows depuis "
                    f"l'interface graphique (ne fonctionne donc pas en ssh)\n{Style.RESET_ALL}").upper()
    if methode in ("1", "2"):
        if methode == "2" and os.name != 'nt':
            print(f"{Fore.RED}Réponse invalide. Vous ne pouvez pas choisir la methode 2 si vous "
                  f"n'êtes pas sur Windows\n{Style.RESET_ALL}")
        else:
            choix_valide = True
    else:
        print(f"{Fore.RED}Réponse invalide. Veuillez entrer 1 ou 2\n{Style.RESET_ALL}")

new_url = ""

if methode == "1":

    print(f"{Fore.LIGHTCYAN_EX}\n\nOuvrez l'application Captcha Skipper sur votre téléphone pour valider le captcha.\n"
          f"{Style.RESET_ALL}Vous pouvez trouver l'application ici : "
          f"\"https://github.com/teo-ldsm/CaptchaSkipper/releases/latset\"\n\n\n")

    app = Flask(__name__)


    @app.route('/get_url')
    def get_url():
        print(f"\n{Fore.GREEN}Le lien a été transmis à l'application mobile{Style.RESET_ALL}\n")
        return lien_page_captcha


    @app.route('/upload_url', methods=['POST'])
    def upload_url():
        global new_url
        new_url = request.form.get('url')

        print(f"\n{Fore.GREEN}New URL received: {new_url}{Style.RESET_ALL}\n")
        # Arrête le serveur Flask
        shutdown_server()

        return 'OK'


    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


    app.run(host="0.0.0.0", port=5000)

elif methode == "2":

    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe')
    chrome_path = winreg.QueryValue(key, None)

    input(f"\n\nUne fenêtre chrome va s'ouvrir. Elle contient le captcha qu'il faut résoudre.\n"
          f"Une fois que le captcha est résolu, vous devez copier-coller dans cette fenêtre le lien du film qui "
          f"commence par \"https://{dl_site}...\n"
          f"Le site fait apparaitre de nombreuses popups inutiles. Tout ce passe sur la première page ouverte.\n"
          f"Appuyez sur Entrer pour ouvrir chrome ...\n")

    subprocess.run([chrome_path, lien_page_captcha])

    new_url = input(f"Copiez-collez ici le lien qui commence par\"https://{dl_site}...\n")


print(f"{Fore.GREEN}Le captcha a été passé avec succès !{Style.RESET_ALL}\n\n")

lien_valide = False
while not lien_valide:
    try:
        print(f"Connecting to {new_url} ...{Fore.BLACK}\n")
        driver.get(new_url)                 # TODO PB de connection avec uptobox
        lien_valide = True
    except:
        rep = demande(f"{Fore.RED}Connexion impossible.{Style.RESET_ALL}\n"
                      f"Certains sites de téléchargements sont bloqués par certains opérateurs\n"
                      f"Cette restriction peut être contournée en modifiant les paramètres DNS du PC\n"
                      f"Voulez vous changer ces paramètres automatiquement ?")

        if rep in ("OUI", "O"):

            if os.name == 'nt':  # Windows
                os.system("netsh interface ipv4 show interfaces")
            else:  # Linux, Mac OS X
                os.system('ifconfig')

            carte_res = input(f"Copier-Collez ici le nom de votre carte réseau connectée a internet\n")

            input("\n\nLe programme va changer automatiquement les paramètres DNS en mettant le DNS gratuit de Google\n"
                  "à la place de celui par défaut. Cela ne changera en rien votre navigation sur internet.\n"
                  "Le programme va vous demander un accès administrateur\n"
                  "Appuyez sur Entrer pour continuer...\n")

            if os.name == 'nt':
                os.system(f"powershell -Command \"Start-Process \'{prgm_dir}/change_dns.bat\' -Verb runAs "
                          f"-ArgumentList \'{carte_res}\'\"")
            else:
                os.system(f"sudo nmcli dev modify {carte_res} ipv4.dns \"8.8.8.8 8.8.4.4\"")

            time.sleep(3)

        else:
            input("Appuyez sur Entrer pour quitter...")
            exit(0)
            

print(f"{Fore.GREEN}Connected !{Fore.BLACK}\n")

lien_film = ""

file_name = ""

if dl_site == "1fichier":

    def recup_link_1fichier():

        try:
            file_name = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[1]/td[3]").text
            btn = driver.find_element(By.ID, "dlb")
            btn.submit()
        except:
            input(f"{Fore.RED}Le fichier à été supprimé du site 1fichier !{Style.RESET_ALL}\n"
                  f"Vous pouvez essayer sur un autre site de téléchargement ou avec une autre qualité.\n"
                  f"Appuyez sur Entrer pour quitter ...")
            exit(1)

        try:
            btn2 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Cliquer ici pour télécharger le fichier")))
        except:

            print(f"{Fore.RED}Une erreur est survenue.\n\n{Style.RESET_ALL}"
                  f"Le site 1fichier a un compte à rebours qui empêche de télécharger plusieurs "
                  f"films d'affilé.\n"
                  f"Ce compte à rebours peut être esquivé en désactivant et en réactivant la carte réseau\n")
            driver.close()
            driver.quit()

            rep = demande("Voulez vous utiliser cette technique ? Cela coupera internet sur votre machine pendant "
                          "quelques secondes.\n"
                          "Si vous répondez \"Non\" le programme va s'arrêter")

            if rep in ("OUI", "O"):

                if os.name == 'nt':  # Windows
                    os.system("netsh interface ipv4 show interfaces")
                else:  # Linux, Mac OS X
                    os.system('ifconfig')

                carte_res = input(f"Copier-Collez ici le nom de votre carte réseau connectée a internet\n")

                input("\n\nLe programme va vous demander 2 fois un accès administrateur\n"
                      "Appuyez sur Entrer pour continuer...\n")

                if os.name == 'nt':
                    os.system("powershell -Command \"Start-Process powershell -Verb runAs -ArgumentList \'-Command\', "
                              f"\'Disable-NetAdapter -Name \"{carte_res}\" -Confirm:$false\'\"")
                else:
                    os.system(f"sudo ifconfig {carte_res} down")

                time.sleep(5)

                if os.name == 'nt':
                    os.system("powershell -Command \"Start-Process powershell -Verb runAs -ArgumentList \'-Command\', "
                              f"\'Enable-NetAdapter -Name \"{carte_res}\" -Confirm:$false\'\"")
                else:
                    os.system(f"sudo ifconfig {carte_res} up")

                input("Relancez maintenant le programme. Si l'erreur persiste essayez de relancer en allant sur un "
                      "autre site de téléchargement\n"
                      "Appuyez sur Entrer pour quitter...")
            exit(0)

        else:
            lien_film = btn2.get_attribute("href")

        return lien_film, file_name

    lien_film, file_name = recup_link_1fichier()


elif dl_site == "Uptobox":

    btn = driver.find_element(By.XPATH, "//*[@id=\"dl\"]/form")
    btn.submit()

    print(f"{Fore.GREEN}Timer skipped !\n{Style.RESET_ALL}"
          f"En attente du chargement de la page{Fore.BLACK}\n")

    try:
        btn2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Cliquez-ici pour lancer votre téléchargement")))
        lien_film = btn2.get_attribute("href")
    except:
        try:
            btn2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Click here to start your download")))
            lien_film = btn2.get_attribute("href")
        except:

            input(f"{Fore.RED}Une erreur est survenue.\n\n"
                  f"{Fore.LIGHTYELLOW_EX}Pour fonctionner, chrome doit être en français ou en anglais\n"
                  f"Le site Uptobox a un compte à rebours qui empêche de télécharger plusieurs "
                  f"films d'affilé. \n"
                  f"Essayez de relancer le programme en allant sur un autre site de "
                  f"téléchargement ou en changeant votre localisation avec un VPN.\n{Style.RESET_ALL}"
                  f"Vous pouvez aller vérifier manuellement sur cette page : {new_url}\n"
                  f"Appuyez sur Entrer pour quitter...\n\n")
            exit(1)

    print(f"{Fore.GREEN}Page chargée !\n{Style.RESET_ALL}\n\n")


driver.close()
driver.quit()


if dl_site == "Uptobox":
    file_name = wget.detect_filename(lien_film)


print(f"\n\n{Style.RESET_ALL}Début du téléchargement\n")
wget.download(lien_film, out=f"{dl_dir}\\{file_name}")

print(f"{Fore.GREEN}\n\nVotre fichier a été téléchargé ici : {dl_dir}\\{file_name}\n\n{Style.RESET_ALL}")

# rep = demande(f"Si vos films sont sur un serveur plex, voulez vous actualiser le serveur ?")
# TODO Implémenter plex

input("Merci d'avoir utilisé Wawacity Downloader !\n"
      "Appuyez sur Entrer pour quitter...")


