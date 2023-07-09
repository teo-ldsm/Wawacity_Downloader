from config_loader import *
if __name__ == '__main__':
    venv_init()

from colorama import Fore, Style

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import sys


def recup_lien(lien) -> tuple[str, str]:

    print(f"\n\n{Style.RESET_ALL}Initialising...\n{Fore.BLACK}")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--lang=fr')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    print(f"{Fore.GREEN}Init OK !\n{Fore.BLACK}")

    driver.get(lien)

    try:
        file_name = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[1]/td[3]").text
        btn = driver.find_element(By.ID, "dlb")
        btn.submit()
    except:
        input(f"{Fore.RED}Le fichier à été supprimé du site 1fichier !{Style.RESET_ALL}\n"
              f"Vous pouvez essayer sur un autre site de téléchargement ou avec une autre qualité.\n"
              f"Appuyez sur Entrer pour quitter ...")
        exit(1)

    try:
        btn2 = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Cliquer ici pour télécharger le fichier")))

    except:

        print(Style.RESET_ALL)
        raise Exception("countdown error")

    else:

        lien_film = btn2.get_attribute("href")

        driver.quit()

        print(Style.RESET_ALL)

        return lien_film, file_name


if __name__ == '__main__':

    args = sys.argv
    print(Style.RESET_ALL, recup_lien(args[1])[0])


