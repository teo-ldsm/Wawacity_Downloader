import http.client
from config_loader import load


def refresh(config):

    conn = http.client.HTTPConnection(config["SERVER_IP"], int(config["PORT"]))
    conn.request("GET", f"/library/sections/all/refresh?X-Plex-Token={config['TOKEN']}")
    rep = conn.getresponse()

    print(rep.reason)

    return rep.status


if __name__ == '__main__':
    config = load()
    refresh(config)
