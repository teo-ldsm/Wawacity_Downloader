import os
import sys


def venv_init():

    if os.name == 'nt':
        sys.path.insert(0, './venv/Scripts')
    else:
        sys.path.insert(0, './venv/bin')
    import activate_this


if __name__ == '__main__':
    venv_init()


def load() -> dict:
    print("Récupération des données de \'config.txt\'...\n")
    try:
        file = open("./config.txt", "r", encoding="UTF-8")

    except:

        rep = demande("Le fichier \'config.txt\' est absent. Voulez vous le reconstruire automatiquement ?")

        if rep in ("OUI", "O"):
            build_config()

        file = open("./config.txt", "r", encoding="UTF-8")

    finally:
        config_tmp = []

        for i in file.readlines():
            tmp = i.rstrip("\n")
            if tmp != "":
                config_tmp.append(tmp)

        a_supp = []
        for i in config_tmp:
            if i[0] == "#":
                a_supp.append(i)

        [config_tmp.remove(i) for i in a_supp]

        config = dict()
        try:
            for i in config_tmp:
                tmp = i.rsplit("=")
                config[tmp[0].strip()] = tmp[1]

        except:

            print("Le fichier \'config.txt\' est mal construit. Appuyez sur Entrer le reconstruire automatiquement.")
            input()

            file.close()
            build_config()
            load()

        else:
            config = verify_config(config)
            file.close()
            return config


def verify_config(config: dict) -> dict:
    from colorama import Fore, Style
    if "PATH" in config:
        if not os.path.exists(config["PATH"].replace("\\", "/")):
            print(f"{Fore.LIGHTYELLOW_EX}Le chemin spécifié dans config.txt à la valeur \'PATH\' "
                  f"n'existe pas{Style.RESET_ALL}\n")
            config.pop("PATH")

    if "SITE" in config:
        if config["SITE"].upper() not in ("1FICHIER", "UPTOBOX"):
            print(f"{Fore.LIGHTYELLOW_EX}La valeur spécifiée dans config.txt à la valeur \'SITE\' "
                  f"n'est pas valide{Style.RESET_ALL}\n")
            config.pop("SITE")

    if "METHOD" in config:
        if config["METHOD"] not in ("1", "2"):
            print(f"{Fore.LIGHTYELLOW_EX}La valeur spécifiée dans config.txt à la valeur \'METHOD\' "
                  f"n'est pas valide{Style.RESET_ALL}\n")
            config.pop("METHOD")

    if "SKIP_COUNTDOWN" in config:
        if config["SKIP_COUNTDOWN"].upper() not in ("OUI", "NON"):
            print(f"{Fore.LIGHTYELLOW_EX}La valeur spécifiée dans config.txt à la valeur \'SKIP_COUNTDOWN\' "
                  f"n'est pas valide{Style.RESET_ALL}\n")
            config.pop("SKIP_COUNTDOWN")

    return config
    # TODO Verifier que les arguments de config sont bons (quality existe)


def build_config() -> None:
    from colorama import Fore, Style
    print(f"\n\n{Fore.LIGHTYELLOW_EX}!! ATTENTION !! \n"
          f"Toutes les données de \'config.txt\' vont être effacées. Veuillez les sauvegarder et appuyer sur Entrer{Style.RESET_ALL}")
    input()
    file = open("config.txt", "w", encoding="UTF-8")
    file.write("# Les lignes qui commencent par \"#\" ne sont pas prises en compte \n"
               "# Veuillez ne pas laisser de champs vide sans un \"#\" en début de ligne \n"
               "# Les champs seront remplis automatiquement si non précisé ici \n"
               "# - ADDRESS : Adresse actuelle du site wawacity. Cette valeur est remplie automatiquement\n"
               "# - PATH : Les medias seront téléchargés dans ce dossier \n"
               "# - QUALITY : Qualité par défaut pour télécharger les médias. Lancez une première fois le programme "
               "normalement pour que la valeur soit remplie automatiquement\n"
               "# - SITE : Site par défaut ou télécharger les médias. Doit être défini par \'1fichier\' "
               "ou \'Uptobox\'. Les autres sites ne sont pas encore pris en charges\n"
               "# - METHOD : Methode à utiliser pour valider le captcha. Doit être défini par \'1\' ou \'2\'\n"
               "#       + Methode 1 : Avec l'application mobile CaptchaSkipper (Android uniquement)\n"
               "#       + Methode 2 : Depuis une fenêtre Chrome (Windows uniquement, beaucoup de popups et de pubs)\n"
               "# - SKIP_COUNTDOWN : Est-ce que le programme doit déconnecter le PC d'internet pour contourner le "
               "compte a rebours du site 1fichier. Doit être défini par \'OUI\' ou \'NON\'\n"
               "#ADDRESS=\n"
               "#PATH=\n"
               "#QUALITY=\n"
               "#SITE=\n"
               "#METHOD=\n"
               "#SKIP_COUNTDOWN=\n\n"
               "# Retirez les # si vous utilisez un serveur plex et que vous souhaitez l'actualiser "
               "après chaque téléchargement \n"
               "#SERVER_IP=\n"
               "PORT=32400\n"
               "#TOKEN=")

    file.close()

    print("config.txt à été reconstruit avec succès !\n")

    rep = demande("Voulez vous remplir les valeurs du fichier maintenant ?")

    if rep in ("OUI", "O"):
        fill_config(tous=True)


def fill_config(tous: bool = False, address: str = False, path: str = False, quality: str = False, site: str = False,
                method: str = False, skip_countdown: str = False, plex: bool = False, manual: bool = True) -> None:
    
    if not isinstance(tous, bool):
        raise TypeError("L'argument tous doit être de type bool")
    if not isinstance(plex, bool):
        raise TypeError("L'argument plex doit être de type bool")
    if not isinstance(manual, bool):
        raise TypeError("L'argument manual doit être de type bool")
    if plex and not manual:
        raise ValueError("Les modifications des valeurs du serveur plex doivent être faites avec "
                         "manual=True en argument")

    if manual:
        config = load()
    if tous:
        address, path, quality, site, skip_countdown, method, plex = True, True, True, True, True, True, True
    args = {"ADDRESS": address, "PATH": path, "QUALITY": quality, "SITE": site, "METHOD": method,
            "SKIP_COUNTDOWN": skip_countdown, "SERVER_IP": plex, "PORT": plex, "TOKEN": plex}

    for i in args:
        if args[i]:
            if manual:
                if i in config:
                    rep = demande(f"La valeur {i} est par défaut a {config[i]}. Voulez vous la modifier ?")
                else:
                    rep = demande(f"La valeur {i} n'a pas été renseigné. Voulez vous la renseigner ?")
            else:
                rep = "OUI"

            if rep in ("OUI", "O"):
                if manual:
                    rep = input(f"Entrez la nouvelle valeur de {i}\n")
                else:
                    rep = args[i]

                with open("./config.txt", "r", encoding="UTF-8") as file:
                    lignes = file.readlines()

                for nb_ligne in range(len(lignes)):
                    if i + "=" in lignes[nb_ligne]:
                        lignes[nb_ligne] = f"{i}={rep}\n"

                with open("./config.txt", "w", encoding="UTF-8") as file:
                    file.writelines(lignes)


def demande(msg: str = ""):
    from colorama import Fore, Style
    choix_valide = False
    rep = None
    while not choix_valide:
        rep = input(f"{msg} (Oui/Non)\n").upper()
        if rep in ("OUI", "NON", "N", "O"):
            choix_valide = True
        else:
            print(f"{Fore.RED}Réponse invalide. Répondez par oui ou non{Style.RESET_ALL}")

    return rep


