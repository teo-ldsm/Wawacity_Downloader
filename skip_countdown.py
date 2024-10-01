import subprocess
import tempfile
from threading import Thread

from driver_init import *
from recup_lien_1fichier import recup_lien
import time


def skip_countdown(mode_auto: bool, lien_dl_site) -> tuple[str, str]:

    print(f"{Fore.RED}Une erreur est survenue.\n\n{Style.RESET_ALL}"
          f"Le site 1fichier a un compte à rebours qui empêche de télécharger plusieurs "
          f"films d'affilé.\n"
          f"Ce compte à rebours peut être esquivé en désactivant et en réactivant la carte réseau (Expérimental, Windows uniquement)\n")

    if mode_auto and ("SKIP_COUNTDOWN" in config):

        rep = config["SKIP_COUNTDOWN"].upper()

    else:
        if os.name == "nt":
            rep = demande("Voulez vous utiliser cette technique ? Cela coupera internet sur votre machine pendant "
                          "quelques secondes.\n"
                          "Si vous répondez \"Non\" le programme va s'arrêter")
        else:
            input(f"{Fore.RED}Cette option est uniquement disponible sous Windows.{Style.RESET_ALL}\n"
                  "Désactivez et réactivez internet manuellement et essayez de relancez le programme")
            sys.exit(1)

    if rep in ("OUI", "O"):

        fd, path = tempfile.mkstemp(suffix='.ps1')
        with os.fdopen(fd, 'w') as f:
            f.write("""
                    # Vérifier si le script est exécuté en tant qu'administrateur
                    If (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
                    {
                        # Relancer le script avec les privilèges administrateur dans la même fenêtre
                        $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"" + $MyInvocation.MyCommand.Definition + "`""
                        Start-Process -FilePath "powershell" -ArgumentList $arguments -Verb runAs -Wait
                        Exit
                    }
                    
                    # Récupérer le nom de la carte réseau connectée à Internet
                    $networkAdapter = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' }
                    
                    # Désactiver la carte réseau
                    Disable-NetAdapter -Name $networkAdapter.Name -Confirm:$false
                    
                    Write-Output "Internet désactivé, reconnexion dans 5 secondes"
                    
                    # Attendre 5 secondes
                    Start-Sleep -Seconds 5
                    
                    # Réactiver la carte réseau
                    Enable-NetAdapter -Name $networkAdapter.Name -Confirm:$false


            """)

        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", path],
                       check=True)

        print("\nReconnexion ", end="")
        for _ in range(30):
            try:
                o = subprocess.run(["ping", "-n", "1", "8.8.8.8"], capture_output=True)
                if o.returncode == 0:
                    break
                else:
                    print(".", end="")
                    time.sleep(1)
            except:
                time.sleep(1)
        else:
            print(f"{Fore.RED}\n\nÉchec de la reconnexion ...{Style.RESET_ALL}\n"
                  f"Désactivez et réactivez internet manuellement et essayez de relancez le programme")
            sys.exit(1)

        print(f"\n{Fore.GREEN}Connecté ! \n{Style.RESET_ALL}"
              f"\nNouvel essai de connexion a 1fichier\n")

        try:
            driver = DriverInit.firefox()
            lien_film, file_name = recup_lien(lien_dl_site, driver)
            Thread(target=driver.quit).start()
        except Exception as e:
            if e.args[0] != "countdown error":
                input(f"{Fore.RED}\n\nLe compte à rebours est toujours présent.{Style.RESET_ALL}\n"
                      f"Voici la page concernée : {lien_dl_site}\n"
                      f"La technique de déconnexion ne fonctionne surement pas sur votre wifi actuel.\n\n"
                      f"Conseils pour retirer le compte a rebours :\n"
                      f"\t - Changez de wi-fi\n"
                      f"\t - Essayez de connecter votre PC à un partage de connexion\n"
                      f"\t - Utilisez un VPN\n"
                      f"\t - Payez Netflix :(\n\n"
                      f"Appuyez sur Enter pour quitter ...\n")
                sys.exit(1)
            else:
                input(f"\n\n{Fore.RED}Une erreur est survenue durant la reconnexion au site 1fichier{Style.RESET_ALL}\n"
                      f"Vous pouvez essayer de désactiver puis de réactiver internet sur votre PC.\n"
                      f"Relancez ensuite le programme.\n"
                      f"Appuyez sur Entrer pour quitter ...\n")
                sys.exit(1)

        else:
            return lien_film, file_name
