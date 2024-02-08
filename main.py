import os
import sys

from help_manager import ask_help
import plex_refresh
from config_loader import *

if __name__ == '__main__':
    venv_init()

ask_help("main")

if os.name == 'nt':
    import winreg

import json
import pathlib
import subprocess
import requests
import time
import threading
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import wget
from recup_lien_1fichier import *


version = "v1.1.1-beta"     # TODO Modifier le numéro de version

if os.name == 'nt':  # Windows
    os.system('cls')
else:  # Linux, Mac OS X
    os.system('clear')

config = load()

args = sys.argv
series, mode_auto = False, False

if "-f" in args:
    config["TITLE"] = args[args.index("-f") + 1]
    mode_auto = True
elif "-s" in args:
    config["TITLE"] = args[args.index("-f") + 1]
    series, mode_auto = True, True

# args = [arg.upper() for arg in args]


# if len(args) > 1 and not args[1] == "DEBUG":
#     config["TITLE"] = args[1]
#     mode_auto = True
# else:
#     mode_auto = False


if "-d" in args:
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
    rep = demande(f'{Fore.GREEN}Une nouvelle version est disponible: {latest_version}. Voulez vous la télécharger ?{Style.RESET_ALL}')

    if rep in ("OUI", "O"):
        package_url = None
        for asset in latest_realease['assets']:
            if asset["name"].startswith("wawacity_downloader"):
                if os.name == "nt" and "windows" in asset["name"]:
                    package_url = asset["browser_download_url"]
                    break
                if os.name != "nt" and "linux" in asset["name"]:
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


# TODO Verifier que chrome est installé


# ----------Initialisation du driver---------- #

driver = driver_init()

# ----------Initialisation du driver---------- #

prgm_dir = str(pathlib.Path(__file__).parent.absolute())

if "PATH" in config:
    dl_dir = config["PATH"]
else:
    dl_dir = prgm_dir

if not mode_auto:
    rep = demande(f"Par défaut, les films seront téléchargés dans le dossier \"{dl_dir}\". "
                  f"Ce chemin vous convient-t-il ?")

elif "PATH" in config:
    print(f"\nDossier de téléchargement récupéré dans config.txt : {dl_dir}\n")
    rep = None

else:
    print("\nLa valeur \"PATH\" est absente de config.txt\n\n")
    rep = "NON"

if rep in ("NON", "N"):

    choix_valide = False
    while not choix_valide:
        dl_dir = input(f"Entrez le chemin d'accès complet du dossier dans "
                       f"lequel vous souhaitez télécharger les films.\n")
        if os.path.exists(dl_dir.replace("\\", "/")):
            choix_valide = True
        else:
            print(f"{Fore.RED}Réponse invalide. Le chemin d'accès n'existe pas\n{Style.RESET_ALL}"
                  f"Le chemin doit être sous cette forme : \"C:\\Users\\Fabrice\\Downloads\" par exemple\n")

    rep = demande(f"Voulez vous faire de {dl_dir} la valeur par défaut ?")

    if rep in ("OUI", "O"):
        fill_config(path=dl_dir, manual=False)


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
    driver.get("https://www.astuces-aide-informatique.info/17934/nouvelle-adresse-wawacity")

    lien_wawacity = driver.find_element(By.XPATH, "//p/a[contains(@href,\'https://www.wawacity.\')]")
    lien_wawacity = lien_wawacity.text.removeprefix("https://")

    print(f"{Fore.GREEN}Lien trouvé : {lien_wawacity}{Style.RESET_ALL}\n")

    connect_to_wawacity(lien_wawacity)

    fill_config(address=lien_wawacity, manual=False)

print(f"{Fore.GREEN}Connected !{Fore.BLACK}\n")

search = driver.find_element(By.NAME, "search")
if not mode_auto:
    search.send_keys(input(f"{Style.RESET_ALL}\n\nQuel est le titre du film que vous recherchez ?\n"))
else:
    search.send_keys(config["TITLE"])

print(Fore.BLACK)
search.submit()


def recup_results(num_page):
    liste_resultats = driver.find_elements(By.XPATH, "//div[@class=\'wa-sub-block-title\']/a")
    liste_dates = driver.find_elements(By.XPATH, "//a[contains(@href,\'?p=films&year=\')]")

    if len(liste_resultats) == 0:
        input(f"\n{Fore.RED}Aucun résultat trouvé.\n"
              f"{Style.RESET_ALL}Appuyez sur Entrer pour quitter...")
        exit(1)

    liens_resultats = dict()
    dates = dict()
    for i in liste_resultats:
        title = i.text[:i.text.index(" [")]
        liens_resultats[title] = i.get_attribute("href")
        dates[title] = liste_dates[liste_resultats.index(i)].text

    titre_correct = True

    if mode_auto and ("TITLE" in config):
        def find_closest_title(dictionary, title):
            closest_title = None
            min_distance = float('inf')

            for cle in dictionary.keys():
                distance = levenshtein_distance(cle.lower(), title.lower())

                if distance < min_distance:
                    min_distance = distance
                    closest_title = cle

            return closest_title

        def levenshtein_distance(s, t):
            if s == t:
                return 0

            if len(s) == 0:
                return len(t)

            if len(t) == 0:
                return len(s)

            previous_row = range(len(t) + 1)
            for i, c1 in enumerate(s):
                current_row = [i + 1]
                for j, c2 in enumerate(t):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        # Merci ChatGPT
        titre = find_closest_title(liens_resultats, config["TITLE"])
        lien = liens_resultats[titre]

        print(f"{Fore.GREEN}Titre récupéré : {titre} ({dates[titre]}){Style.RESET_ALL}\n")

        # def check_input():
        #     global is_incorrect
        #     input()  # Attend l'entrée de l'utilisateur
        #     is_incorrect = True
        #
        # def validation():
        #
        #     import multiprocessing
        #
        #     print("Appuyez sur Entrée si le titre récupéré est incorrect.")
        #
        #     global is_incorrect
        #     is_incorrect = False
        #
        #     # input_thread = threading.Thread(target=check_input)
        #     input_thread = multiprocessing.Process(target=check_input())
        #     # input_thread.daemon = True  # Définit le thread comme un thread démon
        #     input_thread.start()
        #
        #     debut_temporisation = time.time()
        #     while True:
        #         if is_incorrect:
        #             print(f"\n\n{Fore.LIGHTYELLOW_EX}Opération annulée, vous avez indiqué que le titre était incorrect\n"
        #                   f"Veuillez choisir un titre manuellement{Style.RESET_ALL}\n\n")
        #             return False
        #
        #         if time.time() - debut_temporisation > 7:
        #             print("Temps écoulé. La titre est considérée comme valide.")
        #             input_thread.terminate()
        #             return True
        #
        #         time.sleep(0.1)
        #
        # titre_correct = validation()
        #
        # print("bite")
        # input("Zgueg")

        # ^^^^ Fonctionne mais le thread reste actif pendant toute l'exécution du programme


        # def handle_timeout():
        #     raise TimeoutError
        #
        # def validation():
        #     valeur = 42  # La valeur à valider
        #     print("La valeur à valider est :", valeur)
        #
        #     print("Appuyez sur Entrée si la valeur est incorrecte.")
        #
        #     try:
        #         timer = threading.Timer(5, handle_timeout)
        #         timer.start()
        #         input()  # Attend l'entrée de l'utilisateur
        #         timer.cancel()
        #         print("La valeur est incorrecte.")
        #     except TimeoutError:
        #         print("Temps écoulé. La valeur est considérée comme valide.")
        #
        #
        #
        #     print("Suite du programme")
        #     # ...
        #     # ...
        #
        # validation()

        # ^^^^^^ Approche intéréssante mais le try ne capture pas la timeouterror

        # TODO Faire un compte a rebours de 5 secondes qui demande d'appuyer sur entrée si le titre est pas bon.
        # TODO Si c'est le cas, relancer la recherche en page suivante

    if not mode_auto or not ("TITLE" in config) or not titre_correct:
        print(f"{Fore.GREEN}\nVoici les résultats\n{Style.RESET_ALL}")
        index_liens = []
        n = 1
        for i in liens_resultats:
            print(f"{n} : {i} ({dates[i]})")
            index_liens.append(i)
            n += 1

        choix_valide = False
        rep = None
        while not choix_valide:
            try:
                rep = eval(input(f"\nEntrez le numéro correspondant a votre résultat. "
                                 f"Si il ne s'y trouve pas, entrez 0\n"))
                if not isinstance(rep, int):
                    raise TypeError("La variable rep doit être de type int")
                choix_valide = True

            except KeyboardInterrupt:
                exit(1)

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


def supp_spec_car(elt: str):
    elt = elt.replace("[", "", -1)
    elt = elt.replace("]", "", -1)
    elt = elt.replace("(", "", -1)
    elt = elt.replace(")", "", -1)
    elt = elt.replace("-", "", -1)
    return elt


liens_qualites = dict()
for i in liste_qualites:
    liens_qualites[supp_spec_car(i.text)] = i.get_attribute("href")


liens_qualites[supp_spec_car(driver.find_element(By.XPATH, "//*[@id=\'detail-page\']/div[2]/div[1]/i[2]").text.replace("]", "")[1:])] = None


def selection_manuelle_qualite():

    print(f"\nVoici les qualités disponible pour votre film\n")

    index_qualites = sorted([i for i in liens_qualites])
    n = 1
    for i in index_qualites:
        if i.rsplit(" ")[0] != index_qualites[n-2].rsplit(" ")[0]:
            print()
        print(f"{n}:{i}")
        n += 1

    print("\n\nSi la qualité que vous souhaitez ne se trouve pas dans la liste, fermez le programme \n"
          "et relancez le en cherchant le titre de votre films dans une autre langue\n"
          "Exemple: Cherchez \"Avengers - l'Ère d'Ultron\" au lieu de \"Avengers - Age of Ultron\"")

    choix_valide = False
    index_qualite = None
    while not choix_valide:
        try:
            index_qualite = eval(input(f"\nEntrez le numéro correspondant a votre résultat.\n"))
            if not isinstance(index_qualite, int):
                raise TypeError("La variable rep doit être de type int")

        except KeyboardInterrupt:
            exit()

        except:
            print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_qualites)}{Style.RESET_ALL}")
            choix_valide = False

        else:
            if 1 <= index_qualite <= len(index_qualites):
                choix_valide = True
                if "QUALITY" in config and len(config["QUALITY"]) == 1 and config["QUALITY"] != index_qualites[index_qualite - 1]:
                    rep = demande(f"Voulez vous faire de {index_qualites[index_qualite - 1]} la valeur par défaut")
                    if rep in ("OUI", "O"):
                        fill_config(quality=str(index_qualites[index_qualite - 1]), manual=False)
            else:
                print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_qualites)}{Style.RESET_ALL}")
                choix_valide = False

    return liens_qualites[index_qualites[index_qualite - 1]]


if mode_auto and ("QUALITY" in config):

    if len(config["QUALITY"]) == 2:
        if config["QUALITY"][0] in liens_qualites:
            lien_page_film = liens_qualites[config["QUALITY"][0]]
            print(f"{Style.RESET_ALL}\nQualité récupérée dans config.txt : {config['QUALITY']}\n")

        elif config["QUALITY"][1] in liens_qualites:
            lien_page_film = liens_qualites[config["QUALITY"][1]]
            print(f"{Style.RESET_ALL}\nQualité récupérée dans config.txt\n"
                  f"\"{config['QUALITY'][0]}\" n'était pas disponible, "
                  f"\"{config['QUALITY'][1]}\" a été utilisé à la place")
        else:
            print(f"{Fore.LIGHTYELLOW_EX}Les qualités renseignées dans config.txt (\"{config['QUALITY'][0]}\" et "
                  f"\"{config['QUALITY'][1]}\")\n"
                  f"ne sont pas disponibles pour ce film{Style.RESET_ALL}\n"
                  f"Veuillez en choisir une manuellement")
            lien_page_film = selection_manuelle_qualite()

    elif config["QUALITY"] in liens_qualites:
        lien_page_film = liens_qualites[config["QUALITY"]]
        print(f"{Style.RESET_ALL}\nQualité récupérée dans config.txt\n")

    else:
        print(f"{Fore.LIGHTYELLOW_EX}La qualité renseignée dans config.txt (\"{config['QUALITY'][0]}\")"
              f"ne sont pas disponibles pour ce film{Style.RESET_ALL}\n"
              f"Veuillez en choisir une manuellement")
        lien_page_film = selection_manuelle_qualite()

else:
    lien_page_film = selection_manuelle_qualite()


print(Fore.BLACK)

if lien_page_film is not None:
    driver.get(lien_page_film)


liste_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[2]")
liste_liens_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[1]/a")

liens_sites = {liste_sites[i].text: liste_liens_sites[i].get_attribute("href") for i in range(len(liste_sites))
               if liste_sites[i].text in ("1fichier", "Uptobox DESACTIVE") and "Partie" not in liste_liens_sites[i].text}

# TODO Régler le problème de Uptobox

if not mode_auto or "SITE" not in config:

    print(f"{Style.RESET_ALL}Voici les sites de téléchargements disponibles\n")
    n = 1
    index_sites = []
    for i in liens_sites:
        print(f"{n} : {i}")
        index_sites.append(i)
        n += 1

    print(f"\n{Fore.LIGHTYELLOW_EX}Le site Uptobox est désactivé à cause d'un bug{Style.RESET_ALL}\n")  # TODO Enlever ça
    # TODO Enlever aussi le blocage de Uptobox dans le config_loader.verify_config()

    choix_valide = False
    rep = None
    while not choix_valide:
        try:
            rep = eval(input(f"\nEntrez le numéro correspondant au site que vous souhaitez utiliser.\n"))
            if not isinstance(rep, int):
                raise TypeError("La variable rep doit être de type int")
            choix_valide = True

        except KeyboardInterrupt:
            exit(1)

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

else:

    dl_site = config["SITE"].capitalize()
    print("\nSite récupéré dans config.txt\n")


lien_page_captcha = liens_sites[dl_site]

print(f"\n\n{Fore.LIGHTCYAN_EX}############################################################################\n"
      f"L\'accès au téléchargement nécessite la validation d'un captcha.\n"
      "Vous devez valider ce captcha manuellement.\n"
      f"############################################################################\n\n{Style.RESET_ALL}")

choix_valide = False
methode = None
while not choix_valide:             # TODO Vérifier si tu ne peut pat etre bloqué ici indéfiniment avec le mode auto
    if not mode_auto or "METHOD" not in config:
        methode = input(f"Entrez 1 pour résoudre le captcha avec l'application android Captcha skipper\n"
                        f"Entrez 2 pour résoudre le captcha depuis une fenêtre chrome\n\n"
                        f"{Fore.LIGHTYELLOW_EX}Attention ! La methode 2 ne fonctionne que sur Windows depuis "
                        f"l'interface graphique (ne fonctionne donc pas en ssh)\n{Style.RESET_ALL}").upper()
    else:
        methode = config["METHOD"]

    if methode in ("1", "2"):
        if methode == "2" and os.name != 'nt':
            print(f"{Fore.RED}Réponse invalide. Vous ne pouvez pas choisir la methode 2 si vous "
                  f"n'êtes pas sur Windows\n{Style.RESET_ALL}")
            mode_auto = False
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

        if new_url.startswith(f"https://{dl_site.lower()}"):
            # Arrête le serveur Flask
            shutdown_server()
        else:
            print(f"\n\n{Fore.RED}Le lien reçu n'est pas valide{Style.RESET_ALL}\n"
                  f"Sur votre téléphone, vous devez cliquer sur \"Continuer\" dès que le bouton apparait\n"
                  f"Ensuite, cliquez sur le lien qui commence par https://{dl_site}/...\n"
                  f"Pour finir, cliquez sur \"Valider\" en haut a droite de l'écran")

        return 'OK'


    def shutdown_server():
        print(Fore.BLACK)
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            print(Style.RESET_ALL)
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        print(Style.RESET_ALL)


    app.run(host="0.0.0.0", port=5000)

elif methode == "2":

    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe')
    chrome_path = winreg.QueryValue(key, None)

    input(f"{Style.RESET_ALL}\n\nUne fenêtre chrome va s'ouvrir. Elle contient le captcha qu'il faut résoudre.\n"
          f"Une fois que le captcha est résolu, vous devez copier-coller dans cette fenêtre le lien du film qui "
          f"commence par \"https://{dl_site.lower()}...\n"
          f"Le site fait apparaitre de nombreuses popups inutiles. Tout ce passe sur la première page ouverte.\n"
          f"Une fois le lien copié, fermez l'onglet, puis revenez sur cette fenêtre\n"
          f"Appuyez sur Entrer pour ouvrir chrome ...\n")

    subprocess.run([chrome_path, lien_page_captcha])

    # TODO Demander a ChatGPT pk le programme attends que chrome se ferme pour passer a la suite

    while True:
        new_url = input(f"Copiez-collez ici le lien qui commence par \"https://{dl_site.lower()}...\n")
        if new_url.startswith(f"https://{dl_site.lower()}"):
            break
        else:
            print(f"\n\n{Fore.RED}Le lien que vous avez entré n'est pas valide{Style.RESET_ALL}\n\n")

if new_url == "":
    exit()

print(f"{Fore.GREEN}Le captcha a été passé avec succès !{Style.RESET_ALL}\n\n")

lien_valide = False
while not lien_valide:
    try:
        print(f"Connecting to {new_url} ...{Fore.BLACK}\n")
        driver.get(new_url)
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

            input("\n\nLe programme va changer automatiquement les paramètres DNS en mettant le DNS gratuit de "
                  "Google\n"
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

    try:

        lien_film, file_name = recup_lien(new_url)

    except Exception as e:

        if e.args[0] != "countdown error":
            print(Style.RESET_ALL, e)
            exit(1)

        print(f"{Fore.RED}Une erreur est survenue.\n\n{Style.RESET_ALL}"
              f"Le site 1fichier a un compte à rebours qui empêche de télécharger plusieurs "
              f"films d'affilé.\n"
              f"Ce compte à rebours peut être esquivé en désactivant et en réactivant la carte réseau\n")

        if mode_auto and ("SKIP_COUNTDOWN" in config):

            rep = config["SKIP_COUNTDOWN"].upper()

        else:
            rep = demande("Voulez vous utiliser cette technique ? Cela coupera internet sur votre machine pendant "
                          "quelques secondes.\n"
                          "Si vous répondez \"Non\" le programme va s'arrêter")

        if rep in ("OUI", "O"):

            driver.quit()

            if mode_auto and "CARTE_RES" in config:

                carte_res = config["CARTE_RES"]

            else:

                if os.name == 'nt':  # Windows
                    os.system("netsh interface ipv4 show interfaces")
                else:  # Linux, Mac OS X
                    os.system('ifconfig')

                carte_res = input(f"Copier-Collez ici le nom de votre carte réseau connectée a internet\n")

                if "CARTE_RES" in config and config["CARTE_RES"] != carte_res:
                    rep = demande(f"Voulez vous faire de {carte_res} la valeur par défaut ?")

                    if rep in ("OUI", "O"):
                        fill_config(carte_res=carte_res, manual=False)

                input("\n\nLe programme va vous demander 2 fois un accès administrateur\n"
                      "Appuyez sur Entrer pour continuer...\n")

            if os.name == 'nt':
                os.system("powershell -Command \"Start-Process powershell -Verb runAs -ArgumentList \'-Command\', "
                          f"\'Disable-NetAdapter -Name \"{carte_res}\" -Confirm:$false\'\"")
            else:
                os.system(f"sudo ifconfig {carte_res} down")

            time.sleep(7)

            if os.name == 'nt':
                os.system("powershell -Command \"Start-Process powershell -Verb runAs -ArgumentList \'-Command\', "
                          f"\'Enable-NetAdapter -Name \"{carte_res}\" -Confirm:$false\'\"")
            else:
                os.system(f"sudo ifconfig {carte_res} up")

            time.sleep(7)

            print("\nReconnexion ...\n")
            while True:
                try:
                    options_test = Options()
                    options_test.add_argument('--headless')
                    options_test.add_argument('--no-sandbox')
                    options_test.add_argument('--disable-dev-shm-usage')
                    options_test.add_argument('--lang=fr')

                    driver_test = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options_test)
                    driver_test.implicitly_wait(10)

                    driver_test.get("https://google.com")

                    break
                except:
                    time.sleep(1)

            print(f"\n{Fore.GREEN}Connecté ! \n{Style.RESET_ALL}"
                  f"\nNouvel essai de connexion a 1fichier\n")

            try:
                lien_film, file_name = recup_lien(new_url)
            except:
                input(f"\n\n{Fore.RED}Une erreur est survenue durant la reconnexion au site 1fichier{Style.RESET_ALL}\n"
                      f"Vous pouvez essayer de désactiver puis de réactiver internet sur votre PC.\n"
                      f"Relancez ensuite le programme.\n"
                      f"Appuyez sur Entrer pour quitter...\n")
                exit(1)


elif dl_site == "Uptobox":

    btn = driver.find_element(By.XPATH, "//*[@id=\"dl\"]/form")
    btn.submit()

    print(f"{Fore.GREEN}Timer skipped !\n{Style.RESET_ALL}"
          f"En attente du chargement de la page{Fore.BLACK}\n")

    try:
        # btn2 = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//thead/tr/td/a[contains(@href,\'.uptobox.com/dl/\')]")))  # TODO Tester ceci

        btn2 = driver.find_element(By.XPATH, "//thead/tr/td/a[contains(@href,\'.uptobox.com/dl/\')]")

        print(f"{Style.RESET_ALL}C'est OUI !!!!")
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


driver.quit()


if dl_site == "Uptobox":
    file_name = wget.detect_filename(lien_film)


print(f"\n\n{Style.RESET_ALL}Début du téléchargement\n")
wget.download(lien_film, out=f"{dl_dir}/{file_name}")

print(f"{Fore.GREEN}\n\nVotre fichier a été téléchargé ici : {dl_dir}/{file_name}\n\n{Style.RESET_ALL}")

if "SERVER_IP" in config and "PORT" in config and "TOKEN" in config:
    print("Actualisation de votre serveur plex ...\n")

    if plex_refresh.refresh(config) == "200":
        print(f"\n{Fore.GREEN}Serveur actualisé avec succès{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}\nEchec de l'actualisation du serveur{Style.RESET_ALL}\n")

input("\n\nMerci d'avoir utilisé Wawacity Downloader !\n"
      "Appuyez sur Entrer pour quitter...")


