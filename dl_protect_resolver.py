import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import os
import tempfile
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config_loader import *

class LinkResolver:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--disable-images")
        chrome_path = 'Chrome\\App\\Chrome-bin\\chrome.exe'
        if "CHROME_PATH" in config:
            chrome_path = config["CHROME_PATH"]
        self.driver = uc.Chrome(headless=False, browser_executable_path=chrome_path, options = options)
    
    def resolveLinks(self, urls):
        links = dict()
        for url in urls:
            fd, path = tempfile.mkstemp(suffix='.html')
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(f'<a href="{url}" target="_blank">link</a>')
            self.driver.get(f"file://{path}")
            link = self.driver.find_element(By.TAG_NAME, "a")
            link.click()
            sleep(4)
            self.driver.switch_to.window(self.driver.window_handles[1])
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "subButton"))
            )
            self.driver.execute_script("document.getElementById('subButton').click()")
            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//li/a"))
            )
            links[url] = link.text
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        return links        

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    urls = [
        "https://dl-protect.link/bb80536c?fn=RXF1YWxpemVyIDMgW0hEUklQXSAtIFRSVUVGUkVOQ0g%253D", #Equilizer 3
        "https://dl-protect.link/c2599b48?fn=RHVjb2J1IHBhc3NlIGF1IHZlcnQgW1dFQlJJUF0gLSBGUkVOQ0g%3D&rl=a2" # Ducobu
    ]
    linkResolver = LinkResolver()
    links = linkResolver.resolveLinks(urls)
    print(links)
    urls = ["https://dl-protect.link/8b97b80d?fn=TGUgUGFyaXNpZW4gKyBMJ0VxdWlwZSBkdSAwNC4wOC4yMDI0IFtKb3VybmF1eF0%3D&rl=e2"]
    links = linkResolver.resolveLinks(urls)
    print(links)
