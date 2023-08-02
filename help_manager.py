import os
import sys


def general_help():
    print("\n\n\nAide générale pour Wawacity Downloader:\n\n"
          "Wawacity Downloader est un utilitaire pour télécharger des films depuis le site Wawacity.\n\n"
          "Pour obtenir de l'aide sur un fichier, ouvrez \"invite de commande\" puis entrez :\n"
          "python help_manager.py <nom_de_fichier>\n\n"
          "Exemple:\n"
          "python help_manager.py main\n"
          "python help_manager.py recup_lien_1fichier\n\n\n"
          "Pour une utilisation normale du programme vous devez lancer le fichier main.py\n"
          "Entrez \"python help_manager.py main\" pour obtenir de l'aide.\n\n")


def main_help():
    print("\n\n\nAide pour main:\n\n\n"
          "Utilisation mode manuel:\n\n"
          "python main.py\n\n\n"
          "Dans le mode manuel, vous devez sélectionner toutes les infos manuellement (Titre du film, qualité, ...\n\n"
          "Utilisation mode automatique:\n\n"
          "python main.py -f \"<titre_du_film>\n\n\n"
          "Dans le mode automatique, le programme va utiliser les valeurs par défaut remplies dans config.txt\n"
          "Vous devez donc remplir ce fichier au préalable (Le fichier contiens une aide pour remplir chaque valeur)\n"
          "Si config.txt est mal rempli, le programme basculera en mode manuel à pour chaque valeur mal remplie.\n"
          "Attention : Essayez de mettre le titre de la manière la plus précise possible.\n"
          "Exemple : Pour le film \"Creed III\", il faut éviter de mettre \"Creed 3\". Essayez de \n"
          "respecter l'orthographe au maximum.\n\n\n"
          "\nListe des commandes:\n\n"
          "-h, --help \t\t|\tAffiche cette page d'aide\n"
          "-f <\"titre_du_film\">\t|\tLance le programme en mode auto\n\n"
          "Exemples:\n\n"
          "python main.py \t\t\t\t (Mode normal)\n"
          "python main.py -f \"Titanic\" \t\t (Mode automatique, le programme va télécharger le film Titanic)\n\n\n")


def recup_lien_1fichier_help():
    print("\n\n\nAide pour recup_lien_1fichier:\n\n\n"
          "recup_lien_1fichier est un utilitaire qui permet de sauter le compte à rebours d'une minute \n"
          "systématiquement présent sur le site 1fichier.\n"
          "Attention : Il ne permet pas de sauter le compte a rebours de plusieurs heures présent\n"
          "après un téléchargement ! Cette fonctionnalité est implémenté dans main.py.\n\n\n"
          "Liste des commandes :\n\n"
          "-h, --help \t\t|\tAffiche cette page d'aide\n"
          "<\"lien_1fichier\"> \t|\tRenvoie le lien de téléchargement direct associé à <lien_1fichier>\n\n\n"
          "Exemple :\n\n"
          "python recup_lien_1fichier.py \"https://1fichier.com/?qchkik7c7zfojzg4aai1&af=2891723\"\n\n"
          "Cette commande renvoie un lien sous cette forme \"https://o-7.1fichier.com/c602497668\"\n\n"
          "Vous pouvez utilisez ce lien pour télécharger directement le fichier : \n"
          " - Soit avec wget.py (\"python help_manager.py wget\" pour obtenir de l'aide)\n"
          " - Soit en copiant le lien dans votre navigateur.\n\n\n")


def config_loader_help():
    print("\n\n\nAide pour config_loader:\n\n\n"
          "config_loader est un utilitaire pour récupérer le contenu de config.txt sous la forme d'un dictionnaire\n"
          "Il suffit de lancer \"python config_loader.py\" pour récupérer le contenu de config.txt\n\n\n")


def plex_refresh_help():
    print("\n\n\nAide pour plex_refresh:\n\n\n"
          "plex_refresh est un utilitaire pour réactualiser toutes les bibliothèques d'un serveur plex\n"
          "Pour l'utiliser, il faut avoir complété les champs SERVER_IP, PORT et TOKEN dans config.txt")


def wget_help():
    print("\n\n\nAide pour wget:\n\n\n"
          "")


def help_manager_help():
    general_help()


def display_help(file: str):
    file.removesuffix(".py")
    function_name = file + "_help"
    if function_name in globals():
        help_func = globals()[function_name]
        help_func()
    else:
        print(f"Aide non disponible pour le fichier '{file}'.")
        general_help()


def ask_help(file: str):
    args = sys.argv
    no_args_allowed = ("main", "plex_refresh", "help_manager")
    if "-h" in args or "--help" in args:
        display_help(file)
        input("Appuyez sur Entrer pour quitter ...")
        exit()
    elif args[0] != file + ".py" or (len(args) < 2 and file not in no_args_allowed):
        print("\n\nSyntaxe incorrecte !\n\n")
        display_help(file)
        input("Appuyez sur Entrer pour quitter ...")
        exit()


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        general_help()
        input("Appuyez sur Entrer pour quitter ...")
    else:
        display_help(args[1])
        input("Appuyez sur Entrer pour quitter ...")


