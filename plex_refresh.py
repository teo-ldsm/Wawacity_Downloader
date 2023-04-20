import http.client
from config_loader import *


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
        print("Un problème est survenu lors de la connexion au serveur plex. Vérifiez que les valeurs dans "
              "\'config.txt\' sont correctes et que le serveur et connecté au réseau")
        return None

    else:
        print(rep_srv.reason)
        return rep_srv.status


if __name__ == '__main__':
    config = load()
    refresh(config)
