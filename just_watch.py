from config_loader import *

if __name__ == '__main__':
    venv_init()

from colorama import Fore, Style
from simplejustwatchapi import *


class ResultatJustWatch:
    def __init__(self, titre, country="FR", language="fr", count=5, best_only=True):

        self.resultats: list[MediaEntry] = search(titre, country, language, count, best_only)

        if count == 1:
            self.resultat = self.resultats[0]
            self.titre = self.resultat.title

        else:
            # TODO implémenter ici le système de sélection des titres de main.py pour utiliser le moteur de recherche
            #  de Justwatch à la place de celui de Wawacity qui est moins bon
            pass


class InfosFilm:
    def __init__(self, resultat: MediaEntry):

        self.resultat = resultat

        self.titre = self.resultat.title
        self.free = dict()
        self.flatrate = dict()

        for offer in self.resultat.offers:

            if offer.monetization_type == "FLATRATE":
                self.flatrate[offer.name] = offer.url

            elif offer.monetization_type in ("ADS", "FREE"):
                self.free[offer.name] = offer.url


def where_to_watch(film, entree_media: MediaEntry = None):

    if entree_media is not None:
        result = InfosFilm(entree_media)

    else:
        recherche_justwatch = ResultatJustWatch(film, count=1)
        result = InfosFilm(recherche_justwatch.resultat)
    offre_disponible = False

    if len(result.flatrate) > 0 and "PLATFORMS" in config:

        plateformes = config["PLATFORMS"]
        msg = (f"\n\n{Fore.LIGHTCYAN_EX}Ce film est disponible en streaming sur les plateformes suivantes"
               f"\n\n{Style.RESET_ALL}")

        for i in plateformes:
            if i in result.flatrate:
                msg += f"{i} : {result.flatrate[i]}\n"
                offre_disponible = True

        if offre_disponible:
            print(msg)

    if len(result.free) > 0:
        msg = (f"\n\n{Fore.LIGHTCYAN_EX}Ce film est disponible gratuitement en streaming sur les plateformes suivantes"
               f"\n\n{Style.RESET_ALL}")

        for i in result.free:
            msg += f"{i} : {result.free[i]}\n"
            offre_disponible = True

        print(msg)

    if offre_disponible:
        rep = demande("\nVoulez vous continuer le téléchargement")
        if rep in ("NON", "N"):
            input("\n\nMerci d'avoir utilisé Wawacity Downloader\n\n"
                  "Appuyez sur Enter pour quiter\n\n")
            exit(0)


if __name__ == '__main__':
    # config = load()
    where_to_watch(input("Entrez le film dont vous souhaitez obtenir les infos\n"))
