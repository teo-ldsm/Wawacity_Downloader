from driver_init import *
from config_loader import *
from wget import bar_thermometer, get_console_width

from colorama import Fore, Style
import sys

debug_mode_check(sys.argv)


def select_quality(driver, mode_auto, uploadDates, lien_page_film) -> str:
    """Renvoie le lien vers la page wawacity du film en fonction de la qualité choisie par l'utilisateur"""

    liste_qualites = driver.find_elements(By.XPATH, "//ul[@class=\'wa-post-list-ofLinks row readable-post-list\']/li/a")

    class MovieUpload:
        def __init__(self, name, links, size, uploadDate) -> None:
            self.name = name
            self.links = links
            self.size = size
            self.uploadDate = uploadDate
        def __repr__(self):
            return repr(vars(self))

    def parseMovieUploadPage(uploadName, uploadUrl):
        liste_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[2]")
        liste_liens_sites = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[1]/a")
        links = {liste_sites[i].text: liste_liens_sites[i].get_attribute("href") for i in range(len(liste_sites))
                if  "Partie" not in liste_liens_sites[i].text}
        liste_tailles = driver.find_elements(By.XPATH, "//*[@id=\"DDLLinks\"]/tbody/tr/td[3]")
        size = liste_tailles[0].text
        uploadDate = uploadDates.get(uploadUrl)
        return MovieUpload(name = uploadName, links = links, size = size, uploadDate=uploadDate)

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

        movieUpload = parseMovieUploadPage(
            uploadName = supp_spec_car(driver.find_element(By.XPATH, "//*[@id=\'detail-page\']/div[2]/div[1]/i[2]").text.replace("]", "")[1:]),
            uploadUrl = lien_page_film
        )
        movieUploads = {movieUpload.name: movieUpload}

        print("\n\nRécupération des infos pour chaque qualité...\n")
        cpt = 0

        for name, url in liens_qualites.items():
            if url:
                driver.get(url)
            else:
                driver.get(lien_page_film)
            movieUpload = parseMovieUploadPage(name, url)
            movieUploads[name] = movieUpload

            cpt += 1
            # Affichage d'une barre de chargement et d'un pourcentage qui affiche la progression dans la
            # recherche des qualités
            print(f"{bar_thermometer(cpt, len(liens_qualites), int(get_console_width()*3/4))}\t{int(cpt*100/len(liens_qualites))}%", end="\r")

        movieUploads = dict(sorted(movieUploads.items()))

        print(f"\n\nVoici les qualités disponibles pour votre film (Qualité | Taille | Date d'upload)\n")

        def justified_str(expr: str, lg: int) -> str:
            """Renvoie un str de longueur lg commençant par expr et complété avec des espaces pour arriver à la
            longueur lg. Lg doit être supérieur ou egal a len(expr)"""
            if len(expr) > lg:
                raise ValueError("L'expression a centrer ne peut pes être plus grande que la la taille totale")
            if len(expr) == lg:
                return expr
            espacement = (lg - len(expr))
            texte = expr + " " * espacement
            return texte

        long_max = len(max(movieUploads.keys(), key=len))

        index_qualites = sorted([i for i in liens_qualites])
        n = 1
        previous_quality_name = None
        for name, movieUpload in movieUploads.items():
            quality_name = name.rsplit(" ")[0]
            if quality_name != previous_quality_name:
                print()
            print(f"{n}:\t{justified_str(name, long_max)}   | {justified_str(movieUpload.size, 7)} | {movieUpload.uploadDate}")
            n += 1
            previous_quality_name = quality_name

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
                # TODO Ici le Ctrl+C n'arrete pas le programme ce except n'arrive pas a choper le keyboard interrupt

            except:
                print(
                    f"{Fore.RED}Réponse invalide, entrez un chiffre entre 1 et {len(movieUploads)}{Style.RESET_ALL}")
                choix_valide = False

            else:
                if 1 <= index_qualite <= len(movieUploads):
                    choix_valide = True
                    if ("QUALITY" in config and len(config["QUALITY"]) == 1 and
                            config["QUALITY"] != index_qualites[index_qualite - 1]):
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
