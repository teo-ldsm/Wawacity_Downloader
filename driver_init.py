import threading
from collections.abc import Iterable
from functools import wraps
from itertools import count
from time import perf_counter, sleep
from typing import Mapping, Any, Callable

import requests
import signal
from threading import Thread, Lock

from click import launch

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


def exit(n: int):
    if "driver" in globals():
        global driver
        driver.quit()
    sys.exit(n)


args = sys.argv

debug = False


def signal_handler(sig, frame):
    """Fermeture du webdriver quand on fait Ctrl+C, pour éviter de ralentir le PC avec des processus Chrome fantômes"""

    def killDriver():
        print(Style.RESET_ALL)
        try:
            driver.close()
            driver.quit()
        except:
            pass


    print("Arrêt du programme en cours...")
    # kill_thread = threading.Thread(target=killDriver)
    # kill_thread.start()

    killDriver()
    print("Webdriver arrêté")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


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


class DriverInit:

    lien_wawacity = "wawacity.ing"
    chrome_profile_location = ""

    @staticmethod
    def get_chrome_path():
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        def detect_scoop_chrome_app():
            try:
                chrome_exe = shutil.which("chrome")
                chrome_exe_dir = os.path.dirname(chrome_exe)
                chrome_shim = os.path.join(chrome_exe_dir, "chrome.shim")
                if os.path.isfile(chrome_shim):
                    with open(chrome_shim, 'r', encoding='utf8') as file:
                        return file.readline().strip().split(" = ")[1].replace('"', '')
            except:
                pass
            return None

        portable_chrome_path = 'Chrome\\App\\Chrome-bin\\chrome.exe'
        if "CHROME_PATH" in config:
            chrome_path = config["CHROME_PATH"]

        elif is_exe(portable_chrome_path):
            chrome_path = portable_chrome_path

        elif getattr(sys, 'frozen', False):  # Si le script est compilé avec PyInstaller
            chrome_path = os.path.join(sys._MEIPASS, portable_chrome_path)  # PyInstaller extrait les fichiers ici

        elif scoop_chrome_app := detect_scoop_chrome_app():
            chrome_path = scoop_chrome_app

        else:
            chrome_path = None

        return chrome_path

    @staticmethod
    def get_firefox_path():
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        portable_firefox_path = r".\FirefoxPortable\App\Firefox64\firefox.exe"
        if "CHROME_PATH" in config:
            firefox_path = config["CHROME_PATH"]

        elif is_exe(portable_firefox_path):
            firefox_path = portable_firefox_path

        elif getattr(sys, 'frozen', False):  # Si le script est compilé avec PyInstaller
            firefox_path = os.path.join(sys._MEIPASS, portable_firefox_path)  # PyInstaller extrait les fichiers ici

        else:
            firefox_path = None

        return firefox_path

    @staticmethod
    def chrome(headless=True, show_images: bool = False, ip_wawacity: str = None, initialize: bool = True):

        print(f"\n\nInitialising...\n{Fore.BLACK}")

        chrome_path = DriverInit.get_chrome_path()

        options = Options()
        # service = Service()
        # options = webdriver.ChromeOptions()

        if chrome_path is not None:
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
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # if DriverInit.chrome_profile_location != "":
        #     options.add_argument(f"--user-data-dir={DriverInit.chrome_profile_location}")

        options.add_argument("--dns-over-https-mode=secure")
        options.add_argument("--dns-over-https-templates=https://chrome.cloudflare-dns.com/dns-query")

        local_state = {
            "dns_over_https.mode": "secure",
            # "dns_over_https.templates": "https://dns.google/dns-query{?dns}",
            "dns_over_https.templates": "https://chrome.cloudflare-dns.com/dns-query",
        }
        options.add_experimental_option('localState', local_state)

        if not headless and not show_images:
            options.add_argument("--blink-settings=imagesEnabled=false")
        
        if ip_wawacity is None:
            if "ADDRESS" in config:
                ip_wawacity = config["ADDRESS"]
            else:
                ip_wawacity = DriverInit.fetch_new_ip_adress()

        # options.add_argument(f"--host-resolver-rules=MAP {DriverInit.lien_wawacity} {ip_wawacity},EXCLUDE localhost")

        if not initialize:
            return options

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        print(f"{Fore.GREEN}Init OK !\n{Style.RESET_ALL}")

        return driver

    @staticmethod
    def firefox(headless=True, initialize: bool = True):

        if initialize:
            print(f"\n\nInitialising...\n{Fore.BLACK}")

        options = webdriver.FirefoxOptions()

        if headless and not debug:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--lang=fr')
        options.set_preference('network.trr.mode', 2)
        options.set_preference('network.trr.uri', 'https://mozilla.cloudflare-dns.com/dns-query')
        # options.add_argument('--proxy-server=http://127.0.0.1:8080')
        # options.add_argument('--disable-extensions')
        options.binary_location = DriverInit.get_firefox_path()

        if not initialize:
            return options

        driver = webdriver.Firefox(options=options)

        driver.implicitly_wait(10)
        print(f"{Fore.GREEN}Init OK !\n{Style.RESET_ALL}")

        return driver

    @staticmethod
    def fetch_new_ip_adress():
        """Demande au serveur dns de Google l'adresse ip de wawacity et la sauvegarde dans config.txt"""
        url = f'https://dns.google/resolve?name={DriverInit.lien_wawacity}'
        response = requests.get(url)
        data = response.json()
        ip_address = data['Answer'][0]['data']
        fill_config(manual=False, address=ip_address)
        return ip_address


class FirefoxDriverThread(webdriver.Firefox):
    def __init__(self, headless: bool = True, name: str = None):
        self.lock = Lock()
        self.lock.acquire()
        self.is_alive = True
        self.__name__ = name

        options = DriverInit.firefox(headless=headless, initialize=False)
        super().__init__(options=options)

        self.lock.release()

    def launch_thread_w_lock(self, target: Callable, args: Iterable = tuple(), kwargs: Mapping[str, Any] = None):
        def thread_wrapper(*args, **kwargs):
            self.lock.acquire()
            target(*args, **kwargs)
            self.lock.release()

        thread = Thread(target=thread_wrapper, args=args, kwargs=kwargs, name=f"FDT({self.__name__}) -> {target.__name__}({args},{kwargs})")
        thread.start()

    def get(self, url: str):
        self.launch_thread_w_lock(target=super().get, args=(url,))

    def quit(self):
        if self.is_alive:
            # super().quit()
            self.launch_thread_w_lock(target=super().quit)
            self.is_alive = False

    def __del__(self):
        self.quit()

    def is_busy(self):
        return self.lock.locked()

    def join(self, timeout: int = 15):
        t = perf_counter()
        while self.lock.locked():
            if perf_counter() - t > timeout:
                raise TimeoutError("Le thread a mis trop de temps à répondre")


class ThreadDrivers:

    def __init__(self):
        self.__init_lock = Lock()
        self.drivers: list[FirefoxDriverThread] = []

    def is_busy(self):
        self.__init_lock.locked()

    def join(self, timeout: int = 15):
        t = perf_counter()
        while self.__init_lock.locked():
            if perf_counter() - t > timeout:
                raise TimeoutError("Le thread a mis trop de temps à répondre")

    def join_all(self):
        for i in self.drivers:
            if i.is_alive and i.is_busy():
                i.join()

    def quit_all(self):
        self.join_all()
        for i in self.drivers:
            i.quit()
        self.drivers = filter(lambda x: x.is_alive, self.drivers)

    def __getitem__(self, item):
        return self.drivers[item]

    def __del__(self):
        self.quit_all()

    ########################

    def init_multi_firefox(self,  count: int, headless=True) -> None:
        """Initialise une liste de diver thread firefox de longueur count. Initialise tous les drivers en meme temps"""
        self.__init_lock.acquire()
        append_lock = Lock()
        threads = []

        print(f"\n\nInitialising...\n")

        def individual_driver_initializer(headless: bool, name: str):
            d = FirefoxDriverThread(headless=headless, name=name)
            with append_lock:
                self.drivers.append(d)

        for i in range(count):
            driver_init_thread = Thread(target=individual_driver_initializer, args=(headless, f"drivers[{i}]"), name=f"Driver init {i}")
            threads.append(driver_init_thread)
            driver_init_thread.start()

        for thread in threads:
            thread.join()

        self.__init_lock.release()

        print(f"{Fore.GREEN}Init OK !\n{Style.RESET_ALL}")


if __name__ == '__main__':
    # pass
    # driver = DriverInit.firefox(False)
    drivers = ThreadDrivers()
    drivers.init_multi_firefox(2)
    drivers[0].get("https://www.google.com")
    drivers[1].get("https://www.youtube.com")

    drivers.join_all()

    print("Joined")

    drivers.quit_all()
    drivers.join_all()

    # input()



