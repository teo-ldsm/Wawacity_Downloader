from driver_init import *
from config_loader import *

from colorama import Fore, Style
import sys

args = sys.argv
debug_mode_check(args)


def recup_page_captcha(driver, lien_page_film, mode_auto) -> tuple:
    """Renvoie le lien de la page du captcha en fonction du site de téléchargement choisi par l'utilisateur

    Actuellement désactivé car seul 1fichier est utilisé"""

    if lien_page_film is not None:
        driver.get(lien_page_film)

    liste_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[2]")
    liste_liens_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[1]/a")

    liens_sites = {liste_sites[i].text: liste_liens_sites[i].get_attribute("href") for i in range(len(liste_sites))
                   if liste_sites[i].text == "1fichier" and "Partie " not in liste_liens_sites[i].text}

    # if not mode_auto or "SITE" not in config:
    #
    #     print(f"{Style.RESET_ALL}Voici les sites de téléchargements disponibles\n")
    #     n = 1
    #     index_sites = []
    #     for i in liens_sites:
    #         print(f"{n} : {i}")
    #         index_sites.append(i)
    #         n += 1
    #
    #     choix_valide = False
    #     rep = None
    #     while not choix_valide:
    #         try:
    #             rep = eval(input(f"\nEntrez le numéro correspondant au site que vous souhaitez utiliser.\n"))
    #             if not isinstance(rep, int):
    #                 raise TypeError("La variable rep doit être de type int")
    #             choix_valide = True
    #
    #         except KeyboardInterrupt:
    #             exit(1)
    #
    #         except:
    #             print(f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_sites)}{Style.RESET_ALL}")
    #             choix_valide = False
    #
    #         else:
    #             if 1 <= rep <= len(index_sites):
    #                 choix_valide = True
    #             else:
    #                 print(
    #                     f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_sites)}{Style.RESET_ALL}")
    #                 choix_valide = False
    #
    #     dl_site = index_sites[rep - 1]
    #
    # else:
    #
    #     dl_site = config["SITE"].capitalize()
    #     print("\nSite récupéré dans config.txt\n")

    dl_site = "1fichier"

    return liens_sites[dl_site], dl_site
