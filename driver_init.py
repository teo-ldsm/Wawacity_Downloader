import requests

from config_loader import *
import colorama
from colorama import Fore, Style

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
import sys
import shutil

exit = sys.exit
args = sys.argv

debug = False


def debug_mode_check(arguments):
    global Fore, Style, debug
    if "-d" in arguments:
        debug = True

        class Fore:
            BLACK = ""
            RED = ""
            GREEN = ""
            YELLOW = ""
            BLUE = ""
            MAGENTA = ""
            CYAN = ""
            WHITE = ""
            RESET = ""
            LIGHTBLACK_EX = ""
            LIGHTRED_EX = ""
            LIGHTGREEN_EX = ""
            LIGHTYELLOW_EX = ""
            LIGHTBLUE_EX = ""
            LIGHTMAGENTA_EX = ""
            LIGHTCYAN_EX = ""
            LIGHTWHITE_EX = ""

        class Style:
            RESET_ALL = ""


debug_mode_check(args)

def get_chrome_path():
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    def detect_scoop_chrome_app():
        chrome_exe = shutil.which("chrome")
        chrome_exe_dir = os.path.dirname(chrome_exe)
        chrome_shim = os.path.join(chrome_exe_dir, "chrome.shim")
        if os.path.isfile(chrome_shim):
            with open(chrome_shim, 'r', encoding='utf8') as file:
                return file.readline().strip().split(" = ")[1].replace('"', '')
        return None

    portable_chrome_path = 'Chrome\\App\\Chrome-bin\\chrome.exe'
    if "CHROME_PATH" in config:
        chrome_path = config["CHROME_PATH"]
    elif is_exe(portable_chrome_path):
        chrome_path = portable_chrome_path
    elif (scoop_chrome_app := detect_scoop_chrome_app()):
        chrome_path = scoop_chrome_app
    else:
        chrome_path = None
    return chrome_path

class DriverInit:

    lien_wawacity = "wawacity.ing"
    # TODO remplacer par une liste. A ce jour (17/08/2024), wawacity.ing et wawacity.al fonctionnent sans DNS, 
    # et wawacity.tokyo avec DNS. 
    # Faire aussi un testeur d'URL qui essaie toute la liste, et si aucune URL ne répond, récupère la nouvelle URL sur 
    # https://www.astuces-aide-informatique.info/17934/nouvelle-adresse-wawacity ou sur https://t.me/s/Wawacity_officiel?before=60

    @staticmethod
    def chrome(headless=True, ip_wawacity=config["ADDRESS"]):

        print(f"\n\nInitialising...\n{Fore.BLACK}")

        chrome_path = get_chrome_path()
        profile_path = fr"{sys.path[0]}\Chrome\Data\profile\Profile 1"

        options = Options()
        # service = Service()
        # options = webdriver.ChromeOptions()

        options.binary_location = chrome_path

        # options.add_argument(chrome_path)
        if headless and not debug:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--lang=fr')
        options.add_argument('--disable-extensions')
        options.add_argument("--disable-search-engine-choice-screen")
        if not headless:
            options.add_argument("--blink-settings=imagesEnabled=false")
        # options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument(f"--host-resolver-rules=MAP {DriverInit.lien_wawacity} {ip_wawacity},EXCLUDE localhost")

        # service = ChromeService(executable_path=chromedriver_path)

        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # driver = webdriver.Chrome(service=service, options=options)
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome("venv311/Lib/site-packages/chromedriver-win64")
        driver.implicitly_wait(10)
        print(f"{Fore.GREEN}Init OK !\n{Style.RESET_ALL}")

        return driver

    @staticmethod
    def firefox(headless=True):

        print(f"\n\nInitialising...\n{Fore.BLACK}")

        firefox_path = r".\FirefoxPortable\App\Firefox64\firefox.exe"

        options = webdriver.FirefoxOptions()

        if headless and not debug:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--lang=fr')
        # options.add_argument('--proxy-server=http://127.0.0.1:8080')
        # options.add_argument('--disable-extensions')
        options.binary_location = firefox_path

        driver = webdriver.Firefox(options)

        driver.implicitly_wait(10)
        print(f"{Fore.GREEN}Init OK !\n{Style.RESET_ALL}")

        return driver

    @staticmethod
    def fetch_new_ip_adress():
        url = f'https://dns.google/resolve?name={DriverInit.lien_wawacity}'
        response = requests.get(url)
        data = response.json()
        ip_address = data['Answer'][0]['data']
        fill_config(manual=False, address=ip_address)
        return ip_address


if __name__ == '__main__':
    pass
    # driver = DriverInit.chrome(False)
