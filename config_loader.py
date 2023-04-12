def load() -> dict:
    print("Récupération des données de \'config.txt\'...\n")
    try:
        file = open("config.txt", "r", encoding="UTF-8")

    except:
        print("Le fichier \'config.txt\' est absent. Voulez vous le reconstruire automatiquement ?(Oui/Non)")

        choix_valide = False
        while not choix_valide:
            rep = input().upper()
            if rep in ("OUI", "NON", "N", "O"):
                choix_valide = True
            else:
                print("Réponse invalide. Répondez par oui ou non")
        build_config()
        file = open("config.txt", "r", encoding="UTF-8")

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
                config[tmp[0]] = tmp[1]

        except:

            print("Le fichier \'config.txt\' est mal construit. Appuyez sur Entrer le reconstruire automatiquement.")
            input()

            file.close()
            build_config()
            load()

        else:
            verify_config()
            file.close()
            return config


def verify_config():
    pass
    # TODO Verifier que les arguments de config sont bons (path existe, site existe, quality existe)


def build_config() -> None:
    print("\n\n!! ATTENTION !! \n"
          "Toutes les données de \'config.txt\' vont être effacées. Veuillez les sauvegarder et appuyer sur Entrer")
    input()
    file = open("config.txt", "w", encoding="UTF-8")
    file.write("# Les lignes qui commencent par \"#\" ne sont pas prises en compte \n\
                            # Veuillez ne pas laisser de champs vide sans un \"#\" en début de ligne \n\
                            # Les champs seront remplis automatiquement si non précisé ici \n\
                            # - PATH : Les medias seront téléchargés dans ce dossier \n\
                            # - QUALITY : Qualité par défaut pour télécharger les médias \n\
                            # - SITE : Site par défaut ou télécharger les médias \n\
                            # PATH= \n\
                            # QUALITY= \n\
                            # SITE= \n\n\
                            # Si vous utilisez un serveur plex et que vous souhaitez l'actualiser après chaque téléchargement \n\
                            # SERVER_IP= \n\
                            # PORT=32400 \n\
                            # TOKEN= ")

    print("config.txt à été reconstruit avec succès !\n")
    file.close()


def fill_config(path=False, quality=False, site=False, plex=False) -> None:
    config = load()
    file = open("config.txt", "r", encoding="UTF-8")
    args = {"PATH": path, "QUALITY": quality, "SITE": site}
    for i in args:
        if args[i]:
            if i in config:
                print(f"La valeur {i} est par défaut a {config[i]}. Voulez vous la modifier ?(OUI/NON)")
            else:
                print(f"La valeur {i} n'a pas été renseigné. Voulez vous la renseigner ?(OUI/NON")

            choix_valide = False
            rep = None
            while not choix_valide:
                rep = input().upper()
                if rep in ("OUI", "NON", "N", "O"):
                    choix_valide = True
                else:
                    print("Réponse invalide. Répondez par oui ou non")

            if rep in ("OUI", "O"):
                print(f"Entrez la nouvelle valeur de {i}")
                rep = input()

                with open("config.txt", "r", encoding="UTF-8") as file:
                    lignes = file.readlines()

                for nb_ligne in range(len(lignes)):
                    if i+"=" in lignes[nb_ligne]:
                        lignes[nb_ligne] = f"{i}={rep}"

                with open("config.txt", "w", encoding="UTF-8") as file:
                    file.writelines(lignes)
