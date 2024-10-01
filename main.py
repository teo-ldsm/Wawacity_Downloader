from colorama import Fore, Style
import re
from threading import Thread
from selenium.common import WebDriverException

from captcha_solver import *
from find_closest_title import find_closest_title
from justwatch_browser import Browser
from plex_page_parser import parse_plex_page
from recup_page_captcha import recup_page_captcha
from select_quality import select_quality
from driver_init import *
from skip_countdown import skip_countdown

# from obf_authenticator import verify_access

args = sys.argv

# exit = sys.exit

if __name__ == '__main__' and "-d" not in args:
    # venv_init()

    ask_help("main")

from just_watch import where_to_watch
import time

import wget
from recup_lien_1fichier import *
from updater import check_for_update


version = "v1.2.0-beta"     # TODO Modifier le numéro de version
check_for_update(version)
debug_mode_check(args)
Fore.BLACK = ""

driver = None

series, mode_auto = False, False

if len(args) <= 1:
    if "ARGUMENTS" in config:
        for arg in config["ARGUMENTS"].split():
            args.append(arg)
    else:
        args.append("-m")

if "-f" in args:
    config["TITLE"] = args[args.index("-f") + 1]
    mode_auto = True

elif "-s" in args:
    config["TITLE"] = args[args.index("-f") + 1]
    series, mode_auto = True, True

elif "-p" in args:
    config["TITLE"] = parse_plex_page(args[args.index("-p") + 1])
    mode_auto = True

elif "-m" in args:
    mode_auto = False

elif "-i" in args:
    try:
        print("\n\nChoisissez votre film dans le navigateur ...\n")

        # Initialisation du driver suivant en arrière-plan pour gagner du temps
        def initer():
            global driver
            driver = DriverInit.firefox()

        tr = Thread(target=initer)
        tr.start()

        br = Browser()
        config["TITLE"] = br.run()
    except:
        print(f"{Fore.LIGHTYELLOW_EX}Échec de la recherche du titre, utilisation du mode manuel{Style.RESET_ALL}")
        mode_auto = False
    else:
        mode_auto = True

no_download = True if "--no-download" in args else False


# ----------Initialisation du driver---------- #

if not driver:
    driver = DriverInit.firefox()
    # driver = DriverInit.chrome()

# ----------Initialisation du driver---------- #

# prgm_dir = str(pathlib.Path(__file__).parent.absolute())

if no_download:
    rep = "OUI"

elif "DOWNLOAD_PATH" in config:
    dl_dir = config["DOWNLOAD_PATH"]
    print(f"\nDossier de téléchargement récupéré dans config.txt : {dl_dir}\n")
    rep = "OUI"

else:
    if os.name == "nt":
        dl_dir = os.path.join(pathlib.Path().home(), "Downloads")
    else:
        dl_dir = "~/Downloads"

    if not os.path.exists(dl_dir.replace("\\", "/")):
        rep = "NON"
        dl_dir = None

    else:
        rep = demande(f"Par défaut, les films seront téléchargés dans le dossier \"{dl_dir}\". "
                      f"Ce chemin vous convient-t-il ?")


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

if "DOWNLOAD_PATH" not in config and not mode_auto and not no_download:
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
    print(Style.RESET_ALL)

    if not driver.title.startswith("Wawacity"):
        raise WebDriverException

except WebDriverException as e:
    if "ERR_CONNECTION_TIMED_OUT" in e.msg or "ERR_CONNECTION_REFUSED" in e.msg:
        print(f"Adresse invalide ! Recherche de la nouvelle adresse... {Fore.BLACK}")
        driver.quit()
        del driver
        driver = DriverInit.chrome(ip_wawacity=DriverInit.fetch_new_ip_adress())
        driver.get(f"https://{DriverInit.lien_wawacity}")
        print(Style.RESET_ALL)

    else:
        print(Style.RESET_ALL)
        raise e

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
    config["TITLE"] = input(f"{Style.RESET_ALL}\n\nQuel est le titre du film que vous recherchez ?\n")

config["TITLE"] = config["TITLE"].strip()

# print(Fore.BLACK)
# search.submit()

# match = re.search(r"\(\d{4}\)$", config["TITLE"])
#
# if match:
#     date = config["TITLE"][match.start()+1:match.end()-1]
#     title = config["TITLE"][:match.start()].replace(" ", "%20")
#     search_querry = "?p=films&search=" + title + "&year=" + date
#
# else:
#     title = config["TITLE"].replace(" ", "%20")
#     search_querry = "?p=films&search=" + title

search_querry = "?p=films&search=" + config["TITLE"].replace(" ", "%20")

driver.get(driver.current_url + "/" + search_querry)


class Movie:
    def __init__(self, title, year, link) -> None:
        self.title = title
        self.year = year
        self.link = link


uploadDates = dict()


def parse_search_result_page():
    liste_resultats = driver.find_elements(By.XPATH, "//div[@class=\'wa-sub-block-title\']/a")
    liste_dates = driver.find_elements(By.XPATH, "//li[span[contains(text(),'Année')]]/b/a")
    liste_dates_upload = driver.find_elements(By.XPATH, "//span[@class=\'date-text text-muted\']")
    liens_titres = dict()
    dates_titres = dict()
    for index, htmlElement in enumerate(liste_resultats):
        uploadTitle = htmlElement.text
        movieTitle = uploadTitle[:uploadTitle.index(" [")]
        uploadLink = htmlElement.get_attribute("href")
        uploadDate = liste_dates_upload[index].text
        uploadDates[uploadLink] = uploadDate
        liens_titres[movieTitle] = htmlElement.get_attribute("href")
        dates_titres[movieTitle] = liste_dates[index].text
    movies = dict()
    for title in liens_titres:
        year = dates_titres[title]
        fullTitle = f"{title} ({year})"
        movies[fullTitle] = Movie(title = title, year = year, link = liens_titres[title])
    return movies


def recup_results(num_page):
    movies = dict()
    movies.update(parse_search_result_page())
    driver.get(driver.current_url + f"&page=2")
    movies.update(parse_search_result_page())

    if len(movies) == 0:
        input(f"\n{Fore.RED}Aucun résultat trouvé.\n"
              f"{Style.RESET_ALL}Appuyez sur Entrer pour quitter...")
        exit(1)

    titre_correct = True

    if mode_auto and ("TITLE" in config):
        titre = find_closest_title(movies.keys(), config["TITLE"])
        lien = movies[titre].link

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
        titles = []
        movies = {m: movies[m] for m in sorted(movies.keys())}
        n = 1
        for i in movies:
            print(f"{n} : {i}")
            titles.append(i)
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
                print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(titles)}{Style.RESET_ALL}")
                choix_valide = False

            else:
                if 0 <= rep <= len(titles):
                    choix_valide = True
                else:
                    print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 0 et {len(titles)}{Style.RESET_ALL}")
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
            titre = titles[rep - 1]
            lien = movies[titre].link

    return lien, titre


print()
lien_page_film, titre = recup_results(2)
if "PLATFORMS" in config and not mode_auto:
    if not where_to_watch(titre):
        driver.quit()
        sys.exit(0)

driver.get(lien_page_film)

# v v v v v v v v v v SÉLECTION QUALITÉ v v v v v v v v v v #

lien_page_film = select_quality(driver, mode_auto, uploadDates, lien_page_film)

# ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ SÉLECTION QUALITÉ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ #


# v v v v v v v v v v SÉLECTION DU SITE DE DL v v v v v v v v v v #

lien_page_captcha, dl_site = recup_page_captcha(driver, lien_page_film, mode_auto)

# ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ SÉLECTION DU SITE DE DL ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ #


# v v v v v v v v v v RÉSOLUTION DU CAPTCHA v v v v v v v v v v #

methode = CaptchaSolver.select_methode(mode_auto)

lien_dl_site = ""

if methode == "1":
    lien_dl_site = CaptchaSolver.methode1(lien_page_captcha, dl_site)

elif methode == "2":
    lien_dl_site = CaptchaSolver.methode2(lien_page_captcha, dl_site)

elif methode == "3":
    lien_dl_site = CaptchaSolver.methode3(lien_page_captcha, dl_site)

else:
    print(f"{Fore.RED}La méthode '{methode}' n'est pas disponible.\n{Style.RESET_ALL}")
    exit(1)

if lien_dl_site == "":
    exit()

# driver.quit()

print(f"{Fore.GREEN}Le captcha a été passé avec succès !{Style.RESET_ALL}\n\n")

# ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ RÉSOLUTION DU CAPTCHA ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ ˄ #


if no_download:
    driver.quit()
    input(f"Voici le lien vers votre film : {lien_dl_site}\n"
          "Merci d'avoir utilisé Wawacity Downloader\n\n"
          "Appuyez sur Enter pour quiter\n\n")
    exit(0)


print(f"Connecting to {lien_dl_site} ...{Fore.BLACK}\n")
driver.get(lien_dl_site)
print(f"{Fore.GREEN}Connected !{Fore.BLACK}\n")

lien_film = ""

file_name = ""

if dl_site == "1fichier":

    try:

        lien_film, file_name = recup_lien(lien_dl_site, driver)

    except Exception as e:
        if e.args[0] != "countdown error":
            print(Style.RESET_ALL, e)
            exit(1)

        else:
            Thread(target=driver.quit).start()
            lien_film, file_name = skip_countdown(mode_auto, lien_dl_site)


# elif dl_site == "Uptobox":
#
#     btn = driver.find_element(By.XPATH, "//*[@id=\"dl\"]/form")
#     btn.submit()
#
#     print(f"{Fore.GREEN}Timer skipped !\n{Style.RESET_ALL}"
#           f"En attente du chargement de la page{Fore.BLACK}\n")
#
#     try:
#         # btn2 = WebDriverWait(driver, 10).until(
#         #     EC.presence_of_element_located((By.XPATH, "//thead/tr/td/a[contains(@href,\'.uptobox.com/dl/\')]")))
#
#         btn2 = driver.find_element(By.XPATH, "//thead/tr/td/a[contains(@href,\'.uptobox.com/dl/\')]")
#
#         print(f"{Style.RESET_ALL}C'est OUI !!!!")
#         lien_film = btn2.get_attribute("href")
#     except:
#         try:
#             btn2 = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.LINK_TEXT, "Click here to start your download")))
#             lien_film = btn2.get_attribute("href")
#         except:
#
#             input(f"{Fore.RED}Une erreur est survenue.\n\n"
#                   f"{Fore.LIGHTYELLOW_EX}Pour fonctionner, chrome doit être en français ou en anglais\n"
#                   f"Le site Uptobox a un compte à rebours qui empêche de télécharger plusieurs "
#                   f"films d'affilé. \n"
#                   f"Essayez de relancer le programme en allant sur un autre site de "
#                   f"téléchargement ou en changeant votre localisation avec un VPN.\n{Style.RESET_ALL}"
#                   f"Vous pouvez aller vérifier manuellement sur cette page : {lien_dl_site}\n"
#                   f"Appuyez sur Entrer pour quitter...\n\n")
#             exit(1)
#
#     print(f"{Fore.GREEN}Page chargée !\n{Style.RESET_ALL}\n\n")


# driver.quit()


if dl_site == "Uptobox":
    file_name = wget.detect_filename(lien_film)


print(f"\n\n{Style.RESET_ALL}Début du téléchargement\n")
wget.download(lien_film, out=f"{dl_dir}/{file_name}")

print(f"{Fore.GREEN}\n\nVotre fichier a été téléchargé ici : {dl_dir}/{file_name}\n\n{Style.RESET_ALL}")

input("\n\nMerci d'avoir utilisé Wawacity Downloader !\n"
      "Appuyez sur Entrer pour quitter...")


