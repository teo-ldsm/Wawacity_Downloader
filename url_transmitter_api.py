from flask import Flask, request


def init_api(url):

    app = Flask(__name__)
    app.run(host='0.0.0.0', port=5000)

    @app.route('/get_url')
    def get_url():
        return url

    @app.route('/upload_url', methods=['POST'])
    def upload_url():
        new_url = request.form.get('url')
        print(new_url)
        return 'OK'


if __name__ == '__main__':

    init_api(input("Quel est le lien que vous souhaitez envoyer à l'appli Android"))

