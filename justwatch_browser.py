from threading import Thread
from selenium.webdriver.support.wait import WebDriverWait
import time

from driver_init import *


class Browser:
    def __init__(self):
        self.driver = DriverInit.chrome(headless=False, show_images=True)

        self.driver.maximize_window()
        self.driver.get('https://www.justwatch.com/fr')

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "usercentrics-root"))
        )
        time.sleep(1)

        self.driver.execute_script("""
                div = document.getElementById("usercentrics-root");
                shd = div && div.shadowRoot;
                shd.querySelector(".sc-dcJsrY.dQaUXI").click()
        """)
        self.context = "searching"

        self.btn_clicked = False
        self.movie_title = ""

    def generate_searching_panel(self):
        searching_script = """document.body.appendChild(Object.assign(document.createElement('div'), {
                              innerHTML: "Rendez vous sur la page d'un film pour le télécharger",
                              id: 'panneau_perso',
                              style: 'position: fixed; font-size: 30px; right: 10px; top: 50%; background-color: #131a55; color: white; padding: 30px; border-radius: 10px; z-index: 1000; font-weight: bold; width: 25%; text-align: center;',}))"""

        self.driver.execute_script("""old = document.getElementById('panneau_perso');
                                      if (old != null) {old.parentElement.removeChild(old)};
        """)
        self.driver.execute_script(searching_script)

    def generate_film_panel(self) -> str:
        title = self.driver.find_element(By.CLASS_NAME, "title-detail-hero__details__title").text

        self.driver.execute_script("""old = document.getElementById('panneau_perso');
                                              old.parentElement.removeChild(old);
                """)

        self.driver.execute_script("""document.body.appendChild(Object.assign(document.createElement('div'), {
                                      innerHTML: `<p style='color: white; font-size: 30px; margin: 0px'>Cliquez ici pour télécharger</br>${arguments[0]}</p>`,
                                      id: 'panneau_perso',
                                      style: 'position: fixed; font-size: 30px; right: 10px; top: 50%; background-color: #07b033; color: white; padding: 30px; border-radius: 10px; z-index: 1000; font-weight: bold; width: 25%; text-align: center;',}))
        """, title[:-6])

        self.driver.execute_script("""document.getElementById('panneau_perso').appendChild(
                                                      Object.assign(document.createElement('button'), {
                                                      innerHTML: 'Télécharger', 
                                                      id: 'dl_button',
                                                      style: 'border: none; border-radius: 5px; background-color: #111924; color: white; cursor: pointer; font-size: 20px;'}))""")

        self.driver.execute_script("""document.getElementById('dl_button').addEventListener('click', function() {
                                      window.location.href = 'about:blank';
                                      })""")

        return title

    def generate_serie_panel(self) -> None:

        self.driver.execute_script("""old = document.getElementById('panneau_perso');
                                      old.parentElement.removeChild(old);
        """)

        self.driver.execute_script("""document.body.appendChild(Object.assign(document.createElement('div'), {
                                      innerHTML: "Le programme ne peut pas télécharger les séries",
                                      id: 'panneau_perso',
                                      style: 'position: fixed; font-size: 30px; right: 10px; top: 50%; background-color: #b00707; color: white; padding: 30px; border-radius: 10px; z-index: 1000; font-weight: bold; width: 25%; text-align: center;',}))
        """)

    def wait_for_btn_clicked(self) -> None:

        while not self.btn_clicked:
            if (self.context != "film" and
                    self.driver.current_url.startswith('https://www.justwatch.com/fr/film')):

                self.movie_title = self.generate_film_panel()
                self.context = "film"

            elif (self.context != "serie" and
                  self.driver.current_url.startswith('https://www.justwatch.com/fr/serie')):

                self.generate_serie_panel()
                self.context = "serie"

            elif (self.context != "searching" and
                  not self.driver.current_url.startswith('https://www.justwatch.com/fr/serie') and
                  not self.driver.current_url.startswith('https://www.justwatch.com/fr/film')):

                self.generate_searching_panel()
                self.context = "searching"

            if self.driver.current_url == "about:blank":
                self.btn_clicked = True

            time.sleep(1)

    def run(self):

        try:
            self.generate_searching_panel()
            self.wait_for_btn_clicked()

        except Exception as e:
            driver_quit_thread = Thread(target=self.driver.quit)
            driver_quit_thread.start()

            raise e

        finally:
            self.driver.quit()

        return self.movie_title


if __name__ == '__main__':
    br = Browser()
    print(br.run())
