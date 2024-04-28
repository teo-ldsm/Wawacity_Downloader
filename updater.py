from config_loader import *

# if __name__ == '__main__':
#     venv_init()

import os, sys
import requests
import json
import pathlib
from colorama import Fore, Style

import wget

args = sys.argv


def check_for_update(version):
    print("\n\n\nVérification des mises a jour ...\n\n")
    api_url = 'https://api.github.com/repos/teo-ldsm/Wawacity_Downloader/releases/latest'
    response = requests.get(api_url)
    latest_realease = json.loads(response.text)
    latest_version = latest_realease["tag_name"]

    if latest_version != version:
        rep = demande(f'{Fore.GREEN}Une nouvelle version est disponible: {latest_version}. Voulez-vous mettre a jour ?{Style.RESET_ALL}')

        if rep in ("OUI", "O"):
            package_url = None
            for asset in latest_realease['assets']:
                if asset["name"].startswith("wawacity_downloader"):
                    if os.name == "nt" and "windows" in asset["name"]:
                        package_url = asset["browser_download_url"]
                        break
                    if os.name != "nt" and "linux" in asset["name"]:
                        package_url = asset["browser_download_url"]
                        break

            if package_url is not None:
                parent_dir = str(pathlib.Path(__file__).parent.parent.absolute())
                package_name = wget.detect_filename(package_url)
                package_name_no_suffix = package_name.removesuffix(".zip")
                print(f"\nDébut du téléchargement depuis {package_url}\n")

                wget.download(package_url, out=f"{parent_dir}\\{package_name}")

                print(f"\n\nVotre fichier a été téléchargé ici : {parent_dir}\\{package_name}\n\n")

                if os.name == "nt":
                    input(f"{Fore.LIGHTYELLOW_EX}Attention ! Pensez à sauvegarder le contenu de config.txt !\n"
                          f"{Style.RESET_ALL}\n"
                          f"Appuyez sur Entrer pour quitter et lancer l'installateur...\n")

                    os.startfile(f"{parent_dir}\\{package_name}")

                exit(0)

            else:
                input("Une erreur est survenue durant la recherche de mise à jour\n"
                      "Vous pouvez télécharger manuellement la mise a jour ici : "
                      "\"https://github.com/teo-ldsm/Wawacity_Downloader/releases/\"\n"
                      "Appuyez sur Entrer pour quitter ...")
                exit(1)

    else:
        print(f"\n{Fore.GREEN}Le programme est a jour.{Style.RESET_ALL}\n\n")

