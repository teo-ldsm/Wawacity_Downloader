from config_loader import *
from help_manager import ask_help
if __name__ == '__main__':
    venv_init()

import http.client


def refresh(config):

    try:
        conn = http.client.HTTPConnection(config["SERVER_IP"], int(config["PORT"]))
        conn.request("GET", f"/library/sections/all/refresh?X-Plex-Token={config['TOKEN']}")
        rep_srv = conn.getresponse()

    except KeyError:
        rep = demande("Vous devez renseigner des valeurs dans le fichier \'config.txt\'. Voulez-vous le faire "
                      "maintenant ?")

        if rep in ("OUI", "O"):
            fill_config(tous=True)

    except:
        print(f"{Fore.RED}Un problème est survenu lors de la connexion au serveur plex.\n{Style.RESET_ALL}"
              f"Vérifiez que les valeurs dans \'config.txt\' sont correctes et que le serveur et connecté au réseau")
        return None

    else:
        print(rep_srv.reason)
        return rep_srv.status


if __name__ == '__main__':
    from colorama import Fore, Style
    ask_help("plex_refresh")
    config = load()
    refresh(config)
