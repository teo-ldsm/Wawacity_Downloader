from driver_init import *
from config_loader import *

from colorama import Fore, Style
import sys

debug_mode_check(sys.argv)


def select_quality(driver, mode_auto) -> str:
    """Renvoie le lien vers la page wawacity du film en fonction de la qualité choisie par l'utilisateur"""

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

    liens_qualites[supp_spec_car(
        driver.find_element(By.XPATH, "//*[@id=\'detail-page\']/div[2]/div[1]/i[2]").text.replace("]", "")[1:])] = None

    def selection_manuelle_qualite():

        print(f"\nVoici les qualités disponible pour votre film\n")

        index_qualites = sorted([i for i in liens_qualites])
        n = 1
        for i in index_qualites:
            if i.rsplit(" ")[0] != index_qualites[n - 2].rsplit(" ")[0]:
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
                print(
                    f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_qualites)}{Style.RESET_ALL}")
                choix_valide = False

            else:
                if 1 <= index_qualite <= len(index_qualites):
                    choix_valide = True
                    if "QUALITY" in config and len(config["QUALITY"]) == 1 and config["QUALITY"] != index_qualites[
                        index_qualite - 1]:
                        rep = demande(f"Voulez vous faire de {index_qualites[index_qualite - 1]} la valeur par défaut")
                        if rep in ("OUI", "O"):
                            fill_config(quality=str(index_qualites[index_qualite - 1]), manual=False)
                else:
                    print(
                        f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(index_qualites)}{Style.RESET_ALL}")
                    choix_valide = False

        return liens_qualites[index_qualites[index_qualite - 1]]

    if mode_auto and ("QUALITY" in config):

        liens_qualites_bis = liens_qualites
        liens_qualites = {i.replace("  ", " "): liens_qualites_bis[i] for i in liens_qualites_bis}

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

    return lien_page_film
