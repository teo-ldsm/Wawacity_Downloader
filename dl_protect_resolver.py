import subprocess

import undetected_chromedriver as uc
from undetected_chromedriver import Patcher
# from selenium.webdriver.common.by import By
# import threading
import tempfile
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from config_loader import *
from driver_init import *


class LinkResolver:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--disable-images")
        # chrome_path = get_chrome_path()
        if os.name == 'nt':
            version = subprocess.run(f"powershell -command \"&{{(Get-Item '{uc.find_chrome_executable()}').VersionInfo.ProductVersion}}\"", capture_output=True)
            version = eval(version.stdout.decode("utf-8").split(".")[0])
            self.driver = uc.Chrome(headless=False, options=options, version_main=version)
        else:
            p = Patcher()
            self.driver = uc.Chrome(headless=False, options=options, version_main=p.fetch_release_number().version[0])

    def resolveLinks(self, urls):

        def anti_ad_cowboy(driver, stop_event: threading.Event):
            """Le Lucky Luke de la pub, il les fait disparaitre plus vite que son ombre pour que l'utilisateur ne fasse
            qu'une bouchée de ce vilain captcha qui terrorise les populations"""

            while not stop_event.is_set():
                try:
                    ad = driver.find_element(By.ID, "dontfoid")
                    driver.execute_script("""
                            var element = arguments[0];
                            element.parentNode.removeChild(element);
                            """, ad)
                    # print("Pub dégagée")
                    sleep(1)
                except:
                    # print("Pub non détectée")
                    sleep(0.2)

        links = dict()
        for url in urls:
            fd, path = tempfile.mkstemp(suffix='.html')
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(f'<a href="{url}" target="_blank">link</a>')
            self.driver.get(f"file://{path}")
            link = self.driver.find_element(By.TAG_NAME, "a")
            link.click()
            sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[1])

            # stop_event = threading.Event()
            #
            # ad_removal_thread = threading.Thread(target=anti_ad_cowboy, args=(self.driver, stop_event))
            # ad_removal_thread.start()

            self.driver.execute_script("document.body.appendChild(Object.assign(document.createElement('div'), {"
                                       "innerHTML: 'Si une case a cocher apparait, cochez la', "
                                       "style: 'position:fixed;"
                                       "font-size: 30px;"
                                       "top:10px;"
                                       "left:50%;"
                                       "transform:translateX(-50%);"
                                       "background-color:black;"
                                       "color:white;"
                                       "padding:30px;"
                                       "border-radius:5px;"
                                       "z-index:1000;'})) "
                                       "&& setTimeout(e => e.remove(), 3000);")

            # WebDriverWait(self.driver, 30).until(
            #     EC.presence_of_element_located((By.XPATH, "//button[@id='btn1' and text()='Continuer']"))
            # )
            # WebDriverWait(self.driver, 15).until(
            #     EC.presence_of_element_located((By.ID, "subButton"))
            # )
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//button[@id='subButton' and text()='Continuer']"))
            )
            self.driver.execute_script("document.getElementById('subButton').click()")
            link = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//li/a"))
            )
            links[url] = link.text

            # stop_event.set()
            # ad_removal_thread.join()

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        return links        

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    # urls = [
    #     "https://dl-protect.link/bb80536c?fn=RXF1YWxpemVyIDMgW0hEUklQXSAtIFRSVUVGUkVOQ0g%253D",  # Equilizer 3
    #     "https://dl-protect.link/c2599b48?fn=RHVjb2J1IHBhc3NlIGF1IHZlcnQgW1dFQlJJUF0gLSBGUkVOQ0g%3D&rl=a2"  # Ducobu
    # ]
    linkResolver = LinkResolver()
    # linkResolver.driver.get(urls[0])
    # links = linkResolver.resolveLinks(urls)
    # print(links)
    urls = ["https://dl-protect.link/8b97b80d?fn=TGUgUGFyaXNpZW4gKyBMJ0VxdWlwZSBkdSAwNC4wOC4yMDI0IFtKb3VybmF1eF0%3D&rl=e2"]
    links = linkResolver.resolveLinks(urls)
    print(links)
    input("...")
