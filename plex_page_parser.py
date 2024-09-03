from driver_init import *
from just_watch import ResultatJustWatch
from threading import Thread


def parse_plex_page(url: str) -> str:
    """Prends en argument l'url de la page d'un film plex et renvoie le titre du film sous la forme Titre (année)"""

    driver = DriverInit.chrome()

    driver.get(url)

    title = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/h1").text
    date = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div[2]/div[1]/div/span/span[1]").text

    def driver_shutdown():
        driver.quit()

    shutdown = Thread(target=driver_shutdown)
    shutdown.start()

    title = ResultatJustWatch(title, count=1).titre

    return f"{title} ({date})"


if __name__ == '__main__':
    # assert parse_plex_page("https://l.plex.tv/BdDrFHT") == "Kingsman : Le Cercle d'or (2017)"
    # assert parse_plex_page("https://l.plex.tv/6hwCH6P") == "The King's Man : Première Mission (2021)"
    pass

print(parse_plex_page("https://l.plex.tv/BdDrFHT"))

