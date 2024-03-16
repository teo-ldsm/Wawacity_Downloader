from config_loader import *

if __name__ == '__main__':
    venv_init()

import os, sys
import requests
import json
import pathlib
from colorama import Fore, Style

import wget

args = sys.argv


def check_download_extract(version):
    print("\n\n\nVérification des mises a jour ...\n\n")
    api_url = 'https://api.github.com/repos/teo-ldsm/Wawacity_Downloader/releases/latest'
    response = requests.get(api_url)
    latest_realease = json.loads(response.text)
    latest_version = latest_realease["tag_name"]

    if latest_version != version:
        rep = demande(f'{Fore.GREEN}Une nouvelle version est disponible: {latest_version}. Voulez vous la télécharger ?{Style.RESET_ALL}')

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

                print(f"\n\nVotre fichier a été téléchargé ici : {parent_dir}\\{package_name}\n\n"
                      f"Extraction du fichier zip\n\n")

                if os.name == "nt":
                    os.system(f"unzip \"{parent_dir}\\{package_name}\" -d \"{parent_dir}\\{package_name_no_suffix}\"")

                    # os.system(f"cp {parent_dir}\\{package_name_no_suffix}\\updater.py {parent_dir}")
                    # new_dir_name = f"{parent_dir}\\{package_name_no_suffix}"
                    # old_dir_name = str(pathlib.Path(__file__).parent.name)
                    # os.startfile(f"{parent_dir}\\update.py -rm_old --old_name {old_dir_name} --new_name {new_dir_name}")

                    input(f"\n\nLa nouvelle version a été extrait ici : {parent_dir}\\{package_name_no_suffix}\n"
                          f"Vous pouvez supprimer cette version et lancer la nouvelle a la place\n"
                          f"{Fore.LIGHTYELLOW_EX}Attention ! Pensez à sauvegarder le contenu de config.txt !\n"
                          f"{Style.RESET_ALL}\n"
                          f"Appuyez sur Entrer pour quitter ...\n")
                    exit(0)

            else:
                input("Une erreur est survenue durant la recherche de mise à jour\n"
                      "Vous pouvez télécharger manuellement la mise a jour ici : "
                      "\"https://github.com/teo-ldsm/Wawacity_Downloader/releases/\"\n"
                      "Appuyez sur Entrer pour quitter ...")
                exit(1)

    else:
        print(f"\n{Fore.GREEN}Le programme est a jour.{Style.RESET_ALL}\n\n")


def remove_old_version(old, new):
    print("\n\nCopie de config.txt\n")
    os.system(f"mv -f {old}\\config.txt {new}\\config.txt")

    print("Suppression de l'ancienne version...\n\n")
    os.system(f"rm -R {old}")

    print("Finalisation...")
    os.startfile(f"{new}\\updater.py -rm_updater")
    exit(0)


if __name__ == '__main__':
    if "-rm_old" in args:
        if "--old_name" in args and "--new_name" in args:
            old_name = args[args.index("--old_name") + 1]
            new_name = args[args.index("--new_name") + 1]
            remove_old_version(old_name, new_name)
        else:
            raise ValueError("Il manque des arguments dans l'appel de la commande")

    elif "-rm_updater" in args:
        os.system(f"rm -f {pathlib.Path(__file__).parent.parent.absolute()}\\updater.py")
        print(f"{Fore.GREEN}Mise a jour effectuée avec succès !{Style.RESET_ALL}")
        os.startfile("main.py")
        exit(0)


