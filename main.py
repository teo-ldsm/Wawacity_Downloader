from colorama import Fore, Style
from selenium.common import WebDriverException

from captcha_solver import *
from recup_page_captcha import recup_page_captcha
from select_quality import select_quality
from driver_init import *

# from obf_authenticator import verify_access

args = sys.argv

exit = sys.exit

if __name__ == '__main__':
    # venv_init()

    ask_help("main")

from just_watch import where_to_watch
import time

import wget
from recup_lien_1fichier import *
from updater import check_for_update
import signal
import threading


version = "v1.1.3-beta"     # TODO Modifier le numéro de version
# TODO MODIFIER AUSSI LE NUM DE VERSION DANS LE NOM DE L'INSTALLATEUR

if os.name == 'nt':  # Windows
    os.system('cls')
else:  # Linux, Mac OS X
    os.system('clear')

# import obf_authenticator

# config = load()

series, mode_auto = False, False

if "-f" in args:
    config["TITLE"] = args[args.index("-f") + 1]
    mode_auto = True
elif "-s" in args:
    config["TITLE"] = args[args.index("-f") + 1]
    series, mode_auto = True, True

no_download = True if "--no_download" in args else False

debug_mode_check(args)


# args = [arg.upper() for arg in args]


# if len(args) > 1 and not args[1] == "DEBUG":
#     config["TITLE"] = args[1]
#     mode_auto = True
# else:
#     mode_auto = False

check_for_update(version)

# ----------Initialisation du driver---------- #

# driver = DriverInit.firefox()
driver = DriverInit.chrome()

# Fermeture du webdriver quand on fait Ctrl+C, pour éviter de ralentir le PC avec des processus Chrome fantômes
def signal_handler(sig, frame):
    def killDriver():
        driver.quit()
    print("Arrêt du programme en cours...")
    kill_thread = threading.Thread(target=killDriver)
    kill_thread.start()
    print("Webdriver arrêté")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# ----------Initialisation du driver---------- #

prgm_dir = str(pathlib.Path(__file__).parent.absolute())

if "DOWNLOAD_PATH" in config:
    dl_dir = config["DOWNLOAD_PATH"]
else:
    if os.name == "nt":
        dl_dir = pathlib.Path().home() / "Downloads"
    else:
        dl_dir = "~/Downloads"

if no_download:
    rep = "OUI"

else:
    if not mode_auto:
        rep = demande(f"Par défaut, les films seront téléchargés dans le dossier \"{dl_dir}\". "
                      f"Ce chemin vous convient-t-il ?")

    elif "DOWNLOAD_PATH" in config:
        print(f"\nDossier de téléchargement récupéré dans config.txt : {dl_dir}\n")
        rep = None

    else:
        print("\nLa valeur \"DOWNLOAD_PATH\" est absente de config.txt\n\n")
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
        fill_config(download_path=dl_dir, manual=False)


def connect_to_wawacity(link):
    try:
        print(f"\n\nConnecting to {DriverInit.lien_wawacity} ...{Fore.BLACK}")
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
    # lien_wawacity = config['ADDRESS']
    print(f"\n\nConnecting to {DriverInit.lien_wawacity} ...\n{Fore.BLACK}")
    driver.get(f"https://{DriverInit.lien_wawacity}")

    if not driver.title.startswith("Wawacity"):
        raise WebDriverException

except WebDriverException as e:
    if "ERR_CONNECTION_TIMED_OUT" in e.msg:
        print("Adresse invalide ! Recherche de la nouvelle adresse...")
        driver.quit()
        driver = DriverInit.chrome(ip_wawacity=DriverInit.fetch_new_ip_adress())

    else:
        raise e
    # TODO Faire un match avec une eventuelle erreur si l'erreur elle contient NETWORK_ERROR ou jsp quoi
    #  (En gros la page elle est introuvable) Il faut aller faire une requette au dns resolver de google et lui
    #  demander la nouvelle IP du site au cas ou elle ait changé (peu probable). Remplacer le nom de domaine dans
    #  config["ADRESS"] par l'IP actuel du site. Pour connecter avec un nouvel ip ajouter un argument dans
    #  DriverInit.chrome() avec l'adresse ip. Sa valeur par défaut c'est la valeur dans config["ADRESS"]
    #  Voila bg buena suerte

except:
    print(f"{Style.RESET_ALL}\n\nLien invalide\n"
          f"Récupération du nouveau lien ...{Fore.BLACK}")
    driver.get("https://www.astuces-aide-informatique.info/17934/nouvelle-adresse-wawacity")

    DriverInit.lien_wawacity = driver.find_element(By.XPATH, "//a[contains(@href,\'https://www.wawacity.\')]")
    DriverInit.lien_wawacity = DriverInit.lien_wawacity.text.removeprefix("https://")

    print(f"{Fore.GREEN}Lien trouvé : {DriverInit.lien_wawacity}{Style.RESET_ALL}\n")

    connect_to_wawacity(DriverInit.lien_wawacity)

    fill_config(address=DriverInit.lien_wawacity, manual=False)

print(f"{Fore.GREEN}Connected !{Fore.BLACK}\n")

# -------------------- Recherche du Titre -------------------- #

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
    # dates = dict()
    for i in liste_resultats:
        title = i.text[:i.text.index(" [")]
        date = liste_dates[liste_resultats.index(i)]
        title += f" ({date.text})"
        # if title in dates and dates[title] != date:
        liens_resultats[title] = i.get_attribute("href")
        # dates[title] = date.text

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

        print(f"{Fore.GREEN}Titre récupéré : {titre}{Style.RESET_ALL}\n")

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
            print(f"{n} : {i}")
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
                exit(0)
            else:
                print(f"{Style.RESET_ALL}\n\nRecherche des résultats sur la page {num_page+1} : \n")
                lien, titre = recup_results(num_page+1)

        else:
            titre = index_liens[rep - 1]
            lien = liens_resultats[titre]

    return lien, titre

# TODO Transférer ce système dans just_watch.py pour utiliser le moteur de recherche de justwatch
#  au lieu de celui de wawacity
#  TODO Utiliser la distance de levenstein pour déterminer quel est le titre le plus proche renvoyé par
#   wawacity en lui donnant le résultat de justwatch


print()
lien_page_film, titre = recup_results(1)
if "PLATFORMS" in config:
    where_to_watch(titre)

driver.get(lien_page_film)

# ----------SELECTION QUALITE---------- #


lien_page_film = select_quality(driver, mode_auto)


# ----------SELECTION QUALITE---------- #

print(Fore.BLACK)

# ----------SELECTION DL SITE---------- #

lien_page_captcha, dl_site = recup_page_captcha(driver, lien_page_film, mode_auto)


# ----------SELECTION DL SITE---------- #


choix_valide = False
methode = None
while not choix_valide:             # TODO Vérifier si tu ne peut pat être bloqué ici indéfiniment avec le mode auto
    if not mode_auto or "METHOD" not in config:
        methode = input(f"{Style.RESET_ALL}Entrez 1 pour résoudre le captcha avec l'application android Captcha skipper\n"
                        f"Entrez 2 pour résoudre le captcha depuis une fenêtre Firefox\n\n"
                        f"{Fore.LIGHTYELLOW_EX}Attention ! La methode 2 ne fonctionne que sur Windows\n{Style.RESET_ALL}").upper()
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
    new_url = CaptchaSolver.methode1(lien_page_captcha, dl_site)

else:
    new_url = CaptchaSolver.methode2(lien_page_captcha, dl_site)

if new_url == "":
    exit()

# driver.quit()

print(f"{Fore.GREEN}Le captcha a été passé avec succès !{Style.RESET_ALL}\n\n")

if no_download:
    input(f"Voici le lien vers votre film : {new_url}\n"
          "Merci d'avoir utilisé Wawacity Downloader\n\n"
          "Appuyez sur Enter pour quiter\n\n")
    exit(0)

# driver = DriverInit.firefox(headless=False)

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

        lien_film, file_name = recup_lien(new_url, driver)

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
                    driver_test = DriverInit.firefox()

                    driver_test.get("https://google.com")

                    break
                except:
                    time.sleep(1)

            print(f"\n{Fore.GREEN}Connecté ! \n{Style.RESET_ALL}"
                  f"\nNouvel essai de connexion a 1fichier\n")

            try:
                lien_film, file_name = recup_lien(new_url, driver)
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


# driver.quit()


if dl_site == "Uptobox":
    file_name = wget.detect_filename(lien_film)


print(f"\n\n{Style.RESET_ALL}Début du téléchargement\n")
wget.download(lien_film, out=f"{dl_dir}/{file_name}")

print(f"{Fore.GREEN}\n\nVotre fichier a été téléchargé ici : {dl_dir}/{file_name}\n\n{Style.RESET_ALL}")

input("\n\nMerci d'avoir utilisé Wawacity Downloader !\n"
      "Appuyez sur Entrer pour quitter...")


