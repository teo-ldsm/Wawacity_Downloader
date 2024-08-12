import os

from help_manager import ask_help
from config_loader import *
from driver_init import *

if __name__ == '__main__':
    # venv_init()
    pass
    # ask_help("recup_lien_1fichier")


from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import sys

args = sys.argv

debug_mode_check(args)


def recup_lien(lien, driver) -> tuple[str, str]:

    # driver = DriverInit.chrome()


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

        print(f"\n{Fore.GREEN}Lien obtenu : {lien_film}\n\n{Fore.BLACK}")

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
        print(f"{Fore.GREEN}Lien trouvé : {recup_lien(args[1], DriverInit.firefox())[0]}")

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
