from threading import Thread
from wsgiref.simple_server import make_server

from driver_init import *
from config_loader import *
from flask import Flask, request
import time
import socket

lien_dl_site = ""

class ServerThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server("0.0.0.0", 5000, app)
        self.context = app.app_context()
        self.context.push()
        self.isAlive = True

    def run(self):
            localIp = socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET)[0][4][0]
            print(f"Serveur en écoute sur http://{localIp}:5000")
            self.server.serve_forever()

    def shutdown(self):
        print("Arrêt du serveur...")
        self.server.shutdown()


def wait_for_link(lien_page_captcha, dl_site):
        
        app = Flask(__name__)

        @app.route('/get_url')
        def get_url():
            print(f"\n{Fore.GREEN}Le lien a été transmis à l'application mobile{Style.RESET_ALL}\n")
            return lien_page_captcha

        @app.route('/upload_url', methods=['POST'])
        def upload_url():
            global lien_dl_site
            lien_dl_site = request.form.get('url')

            print(f"\n{Fore.GREEN}New URL received: {lien_dl_site}{Style.RESET_ALL}\n")

            if lien_dl_site.startswith(f"https://{dl_site.lower()}"):
                server_thread.isAlive = False
            else:
                print(f"\n\n{Fore.RED}Le lien reçu n'est pas valide{Style.RESET_ALL}\n"
                      f"Sur votre téléphone, vous devez cliquer sur \"Continuer\" dès que le bouton apparait\n"
                      f"Ensuite, cliquez sur le lien qui commence par https://{dl_site}/...\n"
                      f"Pour finir, cliquez sur \"Valider\" en haut a droite de l'écran")

            return 'OK'

        # Créer et démarrer le thread du serveur
        server_thread = ServerThread(app)
        server_thread.start()

        try:
            while server_thread.isAlive:
                time.sleep(1)
            server_thread.shutdown()
            # server_thread.join()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            server_thread.shutdown()
            # server_thread.join()
        return lien_dl_site

if __name__ == "__main__":
    wait_for_link("https://dl-protect.link/3164a384?fn=UG90dGVyc3ZpbGxlIFtXRUJSSVBdIC0gRlJFTkNI&rl=a2", "1fichier")
    # Pour tester:
    # curl http://127.0.0.1:5000/get_url
    # curl -d "url=https://1fichier/toto" http://127.0.0.1:5000/upload_url