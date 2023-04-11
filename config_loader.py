def load():

    try:
        file = open("config.txt", "r", encoding="UTF-8")

    except:
        return "Le fichier \'config.txt\' est absent"

    else:
        config_tmp = []

        for i in file.readlines():
            tmp = i.rstrip("\n")
            if tmp != "":
                config_tmp.append(tmp)

        for i in config_tmp:
            if i[0] == "#":
                config_tmp.remove(i)

        config = dict()

        for i in config_tmp:
            tmp = i.rsplit("=")
            config[tmp[0]] = tmp[1]

        return config
