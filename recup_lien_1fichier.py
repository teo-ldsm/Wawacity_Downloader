import os

from help_manager import ask_help
from config_loader import *
if __name__ == '__main__':
    venv_init()
    # ask_help("recup_lien_1fichier")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import sys

args = sys.argv


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


def driver_init():
    print(f"\n\nInitialising...\n{Fore.BLACK}")

    chrome_path = 'Chrome\\App\\Chrome-bin\\chrome.exe'
    if "CHROME_PATH" in config:
        chrome_path = config["CHROME_PATH"]

    # options = Options()
    service = Service()
    options = webdriver.ChromeOptions()

    options.add_argument(chrome_path)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--lang=fr')
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-search-engine-choice-screen")
    options.binary_location = chrome_path

    # service = ChromeService(executable_path=chromedriver_path)

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options)
    # driver = webdriver.Chrome("venv311/Lib/site-packages/chromedriver-win64")
    driver.implicitly_wait(10)
    print(f"{Fore.GREEN}Init OK !\n{Style.RESET_ALL}")

    return driver


def recup_lien(lien) -> tuple[str, str]:

    driver = driver_init()

    print(Fore.BLACK)

    driver.get(lien)

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
        print(f"{Style.RESET_ALL}Vérification de la présence du compte a rebours{Fore.BLACK}")
        btn2 = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Cliquer ici pour télécharger le fichier")))
        print(f"{Fore.GREEN}Aucun compte a rebours{Fore.BLACK}")

    except KeyboardInterrupt:
        exit()

    except:

        print(Style.RESET_ALL)
        raise Exception("countdown error")

    else:

        lien_film = btn2.get_attribute("href")

        driver.quit()

        print(Style.RESET_ALL)

        return lien_film, file_name


if __name__ == '__main__':

    args = sys.argv

    help_msg = f"{Style.RESET_ALL}Utilisation : \n" \
               f"python recup_lien_1fichier.py <lien>\n\n" \
               f"Exemple :\n" \
               f"python recup_lien_1fichier.py \"https://1fichier.com/?26kivkh2pkkkdijgrbxj&af=3797078\"\n\n"

    if os.name != "nt":
        help_msg.replace("python", "python3")

    if "-h" in args or "--help" in args:
        print("\n\n\n" + help_msg)
        exit()

    try:
        print(f"{Fore.GREEN}Lien trouvé : {recup_lien(args[1])[0]}")

    except IndexError:
        print(f"\n\n\n{Fore.RED}Syntaxe incorrecte\n\n{Style.RESET_ALL}"
              f"{help_msg}")

    except Exception as e:
        if e.args[0] == "countdown error":
            print(f"{Fore.RED}Impossible de trouver le lien{Fore.LIGHTYELLOW_EX}\n"
                  f"Le site 1fichier contiens un compte a rebours qui empêche de télécharger plusieurs films d'affilé\n"
                  f"{Style.RESET_ALL}Désactivez puis réactivez internet sur votre PC puis relancez le programme")

        else:
            print(e)


    # TODO Changer tout ceci
