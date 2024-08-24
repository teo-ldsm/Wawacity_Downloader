from selenium.common import TimeoutException

from driver_init import *
from config_loader import *
import flask_app
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from dl_protect_resolver import LinkResolver
import os

args = sys.argv

debug_mode_check(args)

lien_dl_site = ""


class CaptchaSolver:

    @staticmethod
    def methode1(lien_page_captcha, dl_site):
        
        def findLocalIpAddress():
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        localIp = findLocalIpAddress()

        global lien_dl_site
        print(f"{Fore.LIGHTCYAN_EX}\n\nOuvrez l'application Captcha Skipper sur votre téléphone pour valider le captcha.\n"
              f"{Style.RESET_ALL}Vous pouvez trouver l'application ici : "
              f"\"https://github.com/teo-ldsm/CaptchaSkipper/releases/latset\"\n"
              f"Connecter l'application sur l'adresse IP {localIp} et le port 5000.\n"
              f"Attention, le smartphone doit être sur le même réseau Wifi que ce PC.\n\n\n")

        return flask_app.wait_for_link(lien_page_captcha, dl_site)

    @staticmethod
    def methode2(lien_page_captcha, dl_site):

        if os.name == "nt":

            firefox_driver = DriverInit.firefox()

            try:
                print(f"{Style.RESET_ALL}Tentative de résolution automatique du captcha{Fore.BLACK}")

                firefox_driver.get(lien_page_captcha)

                WebDriverWait(firefox_driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//button[text()=\"Continuer\"]")))

                form = firefox_driver.find_element(By.ID, "myForm")

                form.submit()

                lien_dl_site = WebDriverWait(firefox_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//a[contains(@href,\'https://{dl_site}\')]")))

                print(f"{Fore.GREEN}Captha résolu{Style.RESET_ALL}\n")

                firefox_driver.quit()

                return lien_dl_site.text

            except TimeoutException:

                print(f"{Fore.LIGHTYELLOW_EX}Impossible de résoudre le captcha automatiquement{Style.RESET_ALL}\n"
                      f"Une page de navigateur va s'ouvrir. Résolvez le captcha manuellement\n"
                      f"La page se fermera toute seule dès que le captcha est résolu\n"
                      f"Appuyez sur Enter pour continuer ...{Fore.BLACK}\n")

                driver_maximized = DriverInit.firefox(headless=False)

                driver_maximized.get(lien_page_captcha)
                driver_maximized.maximize_window()

                WebDriverWait(driver_maximized, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//button[text()=\"Continuer\"]")))

                form = driver_maximized.find_element(By.ID, "myForm")
                form.submit()

                lien_dl_site = WebDriverWait(driver_maximized, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href,\'https://1fichier.com\')]")))

                lien_dl_site = lien_dl_site.text

                driver_maximized.quit()

                print(f"{Fore.GREEN}Captha résolu{Style.RESET_ALL}\n")

                return lien_dl_site

        else:

            print(
                f"\n\n{Fore.LIGHTCYAN_EX}############################################################################\n"
                f"L\'accès au téléchargement nécessite la validation d'un captcha.\n"
                "Vous devez valider ce captcha manuellement.\n"
                f"############################################################################\n\n{Style.RESET_ALL}")

            input(
                f"{Style.RESET_ALL}\n\nUn navigateur va s'ouvrir. Elle contient le captcha qu'il faut résoudre.\n"
                f"Une fois que le captcha est résolu, vous devez copier-coller ci-dessous le lien du film qui "
                f"commence par \"https://{dl_site.lower()}...\n"
                f"Le site fait apparaitre de nombreuses popups inutiles. Tout ce passe sur la première page ouverte.\n"
                f"Une fois le lien copié, fermez l'onglet, puis revenez sur cette fenêtre\n"
                f"Appuyez sur Entrer pour ouvrir chrome ...\n")
            os.system(f"xdg-open {lien_page_captcha}")

            while True:
                new_url = input(f"Copiez-collez ici le lien qui commence par \"https://{dl_site.lower()}...\n")
                if new_url.startswith(f"https://{dl_site.lower()}"):
                    break
                else:
                    print(f"\n\n{Fore.RED}Le lien que vous avez entré n'est pas valide{Style.RESET_ALL}\n\n")

            return new_url

    @staticmethod
    def methode3(lien_page_captcha, dl_site):
        resolved_links = LinkResolver().resolveLinks([lien_page_captcha])
        return resolved_links[lien_page_captcha]
