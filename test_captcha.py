from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request


# print("Initialising...")
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.implicitly_wait(10)
# print("Init OK !\n")
#
# driver.get("https://dl-protect.link/80722917?fn=VGhvciA6IExlIE1vbmRlIGRlcyB0w6luw6hicmVzIFtIRExJR0hUIDEwODBwXSAtIE1VTFRJIChUUlVFRlJFTkNIKQ%3D%3D&rl=a2")

app = Flask(__name__)

# url = "https://dl-protect.link/80722917?fn=VGhvciA6IExlIE1vbmRlIGRlcyB0w6luw6hicmVzIFtIRExJR0hUIDEwODBwXSAtIE1VTFRJIChUUlVFRlJFTkNIKQ%3D%3D&rl=a2"
url = "bichoour"

@app.route('/get_url')
def get_url():
    return url


@app.route('/upload_url', methods=['POST'])
def upload_url():
    new_url = request.form.get('new_url')
    # Traitez le nouvel URL de la page web ici
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

